# Local locations
# Copyright (C) 2021  Nguyễn Gia Phong
#
# This file is part of loca.
#
# Loca is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Loca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with loca.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from dataclasses import dataclass, replace
from enum import Enum, auto
from functools import lru_cache, partial
from pathlib import Path
from platform import java_ver, system
from typing import Callable, Dict, List, Tuple, Union

__doc__ = 'Local locations'
__version__ = '2.0.0'
__all__ = ['Loca']

# java_ver falls back to the provided value if not on Jython.
SYSTEM = java_ver(osinfo=(system(), '', ''))[-1][0]
if SYSTEM == 'Windows':
    from .windows import user_data as appdata, shared_data
elif SYSTEM == 'Darwin':
    from .macos import (user_data, user_config, user_cache,
                        shared_data, shared_config)
    user_state = user_data
else:
    from .xdg import (user_data, user_state, user_config, user_cache,
                      shared_data, shared_config)

UserDir = Callable[[], Path]
SharedDirs = Callable[[], List[Path]]


class Dir(Enum):
    DATA = auto()
    STATE = auto()
    CONFIG = auto()
    CACHE = auto()


@lru_cache
def routines(roaming: bool) -> Dict[Dir, Tuple[UserDir, SharedDirs]]:
    """Return callables returning local locations."""
    if SYSTEM == 'Windows':
        roaming_data = partial(appdata, roaming)
        local_data = partial(appdata, False)
        return {Dir.DATA: (roaming_data, shared_data),
                Dir.STATE: (local_data, list),
                Dir.CONFIG: (roaming_data, shared_data),
                Dir.CACHE: (local_data, list)}
    return {Dir.DATA: (user_data, shared_data),
            Dir.STATE: (user_state, list),
            Dir.CONFIG: (user_config, shared_config),
            Dir.CACHE: (user_cache, list)}


@dataclass
class Loca:
    """Local locations.

    Supported kinds of `directory` are defined in the Dir enum.
    System-wide (`syswide`) directories are shared among all users,
    as opposed to user-specific ones.

    On Windows, `roaming` directories are synchronized across devices:
    http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx
    The behavior is only affected for data and configuration directory
    on this platform.

    However, intended usage of Loca does not involve manually
    specifying the above parameters, but calling the properties,
    e.g. `Loca().shared.config()`.
    """
    directory: Dir = Dir.DATA
    syswide: bool = False
    roaming: bool = False

    def __call__(self) -> Union[Path, List[Path]]:
        return routines(self.roaming)[self.directory][self.syswide]()

    @property
    def user(self) -> Loca:
        return replace(self, syswide=False)

    @property
    def shared(self) -> Loca:
        return replace(self, syswide=True)

    @property
    def data(self) -> Loca:
        return replace(self, directory=Dir.DATA)

    @property
    def state(self) -> Loca:
        return replace(self, directory=Dir.STATE)

    @property
    def config(self) -> Loca:
        return replace(self, directory=Dir.CONFIG)

    @property
    def cache(self) -> Loca:
        return replace(self, directory=Dir.CACHE)
