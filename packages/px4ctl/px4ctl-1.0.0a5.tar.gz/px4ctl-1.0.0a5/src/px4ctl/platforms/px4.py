from __future__ import annotations

import asyncio
import math
from logging import getLogger, INFO, WARN
from typing import NewType, Optional

from mavsdk.mission import MissionItem, MissionPlan
from mavsdk.geofence import Polygon, Point
from mavsdk.system import System
from mavsdk.telemetry import LandedState, VelocityBody

from ..commands import cmd
from ..mission import Mission, Waypoint, Geofence, FenceType
from .platform import Platform, PlatformError, PlatformResult, MissionSuccess, MissionFailure

ConnectedSystem = NewType("ConnectedSystem", System)
ReadySystem = NewType("ReadySystem", ConnectedSystem)
RunningSystem = NewType("RunningSystem", ReadySystem)


def _mk_item(waypoint: Waypoint) -> MissionItem:
    return MissionItem(
        waypoint.lat,
        waypoint.lon,
        waypoint.alt,
        5,
        True,
        math.nan,
        math.nan,
        MissionItem.CameraAction.NONE,
        math.nan,
        math.nan,
    )


def _conv_fence_type(fence_type: FenceType) -> Polygon.FenceType:
    if fence_type is FenceType.EXCLUSIVE:
        return Polygon.FenceType.EXCLUSION
    elif fence_type is FenceType.INCLUSIVE:
        return Polygon.FenceType.INCLUSION
    else:
        raise ValueError(f"unknown fence type {fence_type}")


def _mk_fence(geofence: Geofence) -> Polygon:
    points = [Point(vertex.lat, vertex.lon) for vertex in geofence.vertices]
    fence_type = _conv_fence_type(geofence.fence_type)

    return Polygon(points, fence_type)


async def connect(drone: System, address: Optional[str]) -> ConnectedSystem:
    await drone.connect(system_address=address)

    async for state in drone.core.connection_state():
        if state.is_connected:
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            break

    return ConnectedSystem(drone)


async def upload(drone: ConnectedSystem, mission: Mission) -> ReadySystem:
    mission_items = [_mk_item(waypoint) for waypoint in mission.waypoints]
    mission_plan = MissionPlan(mission_items)
    geofences = [_mk_fence(geofence) for geofence in mission.geofences]

    await cmd(lambda: drone.mission.upload_mission(mission_plan))

    if len(geofences) > 0:
        await cmd(lambda: drone.geofence.upload_geofence(geofences))

    await cmd(lambda: drone.param.set_param_float("NAV_ACC_RAD", mission.acceptance_radius))

    return ReadySystem(drone)


async def start(drone: ReadySystem) -> RunningSystem:
    await cmd(lambda: drone.action.arm())
    await cmd(lambda: drone.mission.start_mission())

    return RunningSystem(drone)


async def stationary(drone: RunningSystem) -> None:
    async for odometry in drone.telemetry.odometry():
        if odometry.velocity_body == VelocityBody(0, 0, 0):
            return

    raise PlatformError("Odometry stream terminated unexpectedly")


async def finished(drone: RunningSystem) -> None:
    while not await drone.mission.is_mission_finished():
        await asyncio.sleep(0.05)


async def timed_out(drone: RunningSystem, duration: int) -> None:
    async for time in drone.telemetry.unix_epoch_time():
        start_time = time
        break

    async for time in drone.telemetry.unix_epoch_time():
        if time - start_time >= duration:
            break


async def landed(drone: RunningSystem) -> None:
    await cmd(lambda: drone.action.land())

    async for state in drone.telemetry.landed_state():
        if state is LandedState.ON_GROUND:
            break

        await asyncio.sleep(0.05)


_Timeout = Optional[int]


async def completed(drone: RunningSystem, timeout: _Timeout, land: bool = False) -> PlatformResult:
    finished_task = asyncio.create_task(finished(drone))
    termination_tasks = [finished_task, asyncio.create_task(stationary(drone))]

    if timeout is not None:
        termination_tasks.append(asyncio.create_task(timed_out(drone, timeout)))

    done, pending = await asyncio.wait(termination_tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    await cmd(lambda: drone.mission.clear_mission())

    if land:
        await landed(drone)

    if not finished_task in done:
        return MissionFailure()

    return MissionSuccess()


class Px4(Platform):
    def __init__(
        self,
        *,
        server_addr: Optional[str] = None,
        server_port: Optional[int] = None,
        system_addr: Optional[str] = None,
        verbose: bool = False,
    ):
        if server_addr is not None and system_addr is not None:
            raise ValueError("cannot specify server address and system address together")

        self.logger = getLogger("px4ctl")
        self.logger.setLevel(INFO if verbose else WARN)
        self.system_addr = system_addr

        if server_port is not None:
            self.drone = System(mavsdk_server_address=server_addr, port=server_port)
        else:
            self.drone = System(mavsdk_server_address=server_addr)

    async def run_mission(self, mission: Mission, timeout: _Timeout = None) -> PlatformResult:
        connected_drone = await connect(self.drone, self.system_addr)
        self.logger.info("Connected to drone")

        ready_drone = await upload(connected_drone, mission)
        self.logger.info("Uploaded mission")

        running_drone = await start(ready_drone)
        self.logger.info("Started mission")

        result = await completed(running_drone, timeout, land=False)
        self.logger.info(f"Finished mission -- Success: {isinstance(result, MissionSuccess)}")

        return result
