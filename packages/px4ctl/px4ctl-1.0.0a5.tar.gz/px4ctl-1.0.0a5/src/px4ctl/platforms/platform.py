from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union, Optional

from ..mission import Mission


class MissionSuccess:
    pass


class MissionFailure:
    pass


PlatformResult = Union[MissionSuccess, MissionFailure]


class Platform(ABC):
    @abstractmethod
    async def run_mission(self, mission: Mission, timeout: Optional[int] = None) -> PlatformResult:
        raise NotImplementedError()


class PlatformError(Exception):
    pass
