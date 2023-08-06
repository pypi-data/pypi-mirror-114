from __future__ import annotations

from asyncio import run as run_async

from click import group, option, argument, pass_context, Context
from mavsdk.system import System

from .mission import Mission, Waypoint
from .storage import load_mission, store_mission
from .platforms import Px4


@group()
@option("-m", "--mission", "mission_name", default="mission.json", help="Name of mission")
@pass_context
def px4ctl(ctx: Context, mission_name: str) -> None:
    ctx.ensure_object(dict)
    ctx.obj["mission_name"] = mission_name


@px4ctl.command()
@pass_context
def init(ctx: Context) -> None:
    return store_mission(Mission(), ctx.obj["mission_name"])


@px4ctl.command()
@pass_context
def verify(ctx: Context) -> None:
    return print("Valid") if load_mission(ctx.obj["mission_name"]) else print("Invalid")


@px4ctl.command()
@pass_context
def show(ctx: Context) -> None:
    mission = load_mission(ctx.obj["mission_name"])
    print(mission)


@px4ctl.command()
@argument("lat", type=float)
@argument("lon", type=float)
@argument("alt", type=float, default=25)
@pass_context
def add(ctx: Context, lat: float, lon: float, alt: float) -> None:
    mission = load_mission(ctx.obj["mission_name"])
    waypoint = Waypoint(lat=lat, lon=lon, alt=alt)

    return store_mission(mission.add_waypoint(waypoint), ctx.obj["mission_name"])


@px4ctl.command()
@option("-v", "--verbose", is_flag=True, help="Log progress during execution")
@option("--system", "system_addr", type=str, default="udp://:14540", help="URL of PX4 system")
@option("--mavsdk", "server_addr", type=str, default=None, help="URL of mavsdk server")
@option("--mavsdk-port", "server_port", type=int, default=50051, help="Port of mavsdk server")
@pass_context
def run(
    ctx: Context,
    verbose: bool,
    system_addr: str,
    server_addr: str,
    server_port: int,
) -> None:
    mission = load_mission(ctx.obj["mission_name"])

    if mission.empty:
        raise RuntimeError("Mission does not contain any waypoints")

    platform = Px4(
        server_addr=server_addr, server_port=server_port, system_addr=system_addr, verbose=verbose
    )
    run_async(platform.run_mission(mission))


if __name__ == "__main__":
    px4ctl()
