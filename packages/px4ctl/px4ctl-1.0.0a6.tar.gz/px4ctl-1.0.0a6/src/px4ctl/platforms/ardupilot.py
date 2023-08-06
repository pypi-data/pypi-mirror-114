from __future__ import annotations

import asyncio
import logging
from typing import NewType, List, Optional, TYPE_CHECKING

from dronekit import connect, Vehicle, Command, VehicleMode
from pymavlink.mavutil import mavlink

if TYPE_CHECKING:
    from dronekit import MessageFactory

from ..mission import Geofence, FenceType, Mission, Waypoint
from .platform import Platform, PlatformResult, MissionSuccess

ReadyVehicle = NewType("ReadyVehicle", Vehicle)
RunningVehicle = NewType("RunningVehicle", ReadyVehicle)


def _mk_command(waypoint: Waypoint) -> Command:
    return Command(
        0,
        0,
        0,
        mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavlink.MAV_CMD_NAV_WAYPOINT,
        0,
        0,
        0,
        0,
        0,
        0,
        waypoint.lat,
        waypoint.lon,
        waypoint.alt,
    )


def _mk_msgs(factory: MessageFactory, fence: Geofence) -> List[object]:
    if fence.fence_type is FenceType.EXCLUSIVE:
        return [
            factory.mav_cmd_nav_fence_polygon_vertex_exclusion_encode(
                len(fence.vertices),
                1,
                0,
                0,
                vertex.lat,
                vertex.lon,
                0,
            )
            for vertex in fence.vertices
        ]
    elif fence.fence_type is FenceType.INCLUSIVE:
        return [
            factory.mav_cmd_nav_fence_polygon_vertex_inclusion_encode(
                len(fence.vertices),
                1,
                0,
                0,
                vertex.lat,
                vertex.lon,
                0,
            )
            for vertex in fence.vertices
        ]
    else:
        raise TypeError("Unknown fence type")


async def upload(drone: Vehicle, mission: Mission) -> ReadyVehicle:
    waypoint_cmds = [_mk_command(waypoint) for waypoint in mission.waypoints]
    fence_msgs = [_mk_msgs(drone.message_factory, geofence) for geofence in mission.geofences]

    drone.commands.add(
        Command(
            0,
            0,
            0,
            mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            10,
        )
    )

    for cmd in waypoint_cmds:
        drone.commands.add(cmd)

    drone.commands.upload()

    for msg_list in fence_msgs:
        for msg in msg_list:
            drone.send_mavlink(msg)

    return ReadyVehicle(drone)


async def start(drone: ReadyVehicle, initial_alt: float = 10) -> RunningVehicle:
    while not drone.is_armable:
        await asyncio.sleep(0.1)

    drone.mode = VehicleMode("GUIDED")
    drone.armed = True

    while not drone.armed:
        await asyncio.sleep(0.1)

    drone.simple_takeoff(initial_alt)

    threshold_alt = 0.95 * initial_alt

    while drone.location.global_relative_frame.alt < threshold_alt:
        await asyncio.sleep(0.1)

    return RunningVehicle(drone)


async def finished(drone: RunningVehicle, mission: Mission) -> PlatformResult:
    drone.commands.next = 0
    drone.mode = VehicleMode("AUTO")

    while drone.commands.next != len(mission.waypoints):
        await asyncio.sleep(0.1)

    drone.mode = VehicleMode("RTL")

    return MissionSuccess()


class Ardupilot(Platform):
    def __init__(self, *, system_addr: str, verbose: bool = False):
        self.system_addr = system_addr
        self.verbose = verbose

    async def run_mission(self, mission: Mission, timeout: Optional[int] = None) -> PlatformResult:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)

        drone = connect(self.system_addr, wait_ready=True)
        logger.debug("Connected to drone")

        ready_drone = await upload(drone, mission)
        logger.debug("Uploaded mission to drone")

        running_drone = await start(ready_drone)
        logger.debug("Started mission")

        result = await finished(running_drone, mission)
        logger.debug("Finshed mission")

        return result
