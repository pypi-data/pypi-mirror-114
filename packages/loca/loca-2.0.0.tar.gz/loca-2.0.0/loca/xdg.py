# Local locations following XDG specification
# Copyright (C) 2005-2010  ActiveState Software Inc.
# Copyright (C) 2013  Eddy Petrișor
# Copyright (C) 2013  Matěj Cepl
# Copyright (C) 2013-2014  Sridhar Ratnakumar
# Copyright (C) 2015  Carl George
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

from os import getenv, pathsep
from pathlib import Path
from typing import List

__doc__ = 'Local locations following XDG specification'
__all__ = ['user_data', 'user_state', 'user_config', 'user_cache',
           'shared_data', 'shared_config']


def user_data() -> Path:
    """Return `$XDG_DATA_HOME`, falling back to `~/.local/share`."""
    directory = getenv('XDG_DATA_HOME')
    if directory: return Path(directory)
    return Path.home() / '.local' / 'share'


def user_state() -> Path:
    """Return `$XDG_STATE_HOME`, falling back to `~/.local/state`."""
    directory = getenv('XDG_STATE_HOME')
    if directory: return Path(directory)
    return Path.home() / '.local' / 'state'


def user_config() -> Path:
    """Return `$XDG_CONFIG_HOME`, falling back to `~/.config`."""
    directory = getenv('XDG_CONFIG_HOME')
    if directory: return Path(directory)
    return Path.home() / '.config'


def user_cache() -> Path:
    """Return `$XDG_CACHE_HOME`, falling back to `~/.cache`."""
    directory = getenv('XDG_CACHE_HOME')
    if directory: return Path(directory)
    return Path.home() / '.cache'


def shared_data() -> List[Path]:
    """Return `$XDG_DATA_DIRS`, falling back to `/usr/{local,}/share`."""
    dirs = getenv('XDG_DATA_DIRS')
    if dirs: return [Path(d) for d in dirs.split(pathsep)]
    return [Path('/usr/local/share'), Path('/usr/share')]


def shared_config() -> List[Path]:
    """Return `$XDG_CONFIG_DIRS`, falling back to `/etc/xdg`."""
    dirs = getenv('XDG_CONFIG_DIRS')
    if dirs: return [Path(d) for d in dirs.split(pathsep)]
    return [Path('/etc/xdg')]
