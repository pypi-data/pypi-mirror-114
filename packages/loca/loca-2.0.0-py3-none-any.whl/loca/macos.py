# Local locations for macos
# Copyright (C) 2005-2010  ActiveState Software Inc.
# Copyright (C) 2013  Matěj Cepl
# Copyright (C) 2013, 2014  Sridhar Ratnakumar
# Copyright (C) 2015  Rex Kerr
# Copyright (C) 2016, 2017  Jeff Rouse
# Copyright (C) 2021  Nguyễn Gia Phong
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
from typing import List

__doc__ = 'Local locations for macOS'
__all__ = ['user_data', 'user_config', 'user_cache',
           'shared_data', 'shared_config']


def user_data() -> Path:
    """Return `~/Library/Application Support`."""
    return Path.home() / 'Library' / 'Application Support'


def user_config() -> Path:
    """Return `~/Library/Preferences`."""
    return Path.home() / 'Library' / 'Preferences'


def user_cache() -> Path:
    """Return `~/Library/Caches`."""
    return Path.home() / 'Library' / 'Caches'


def shared_data() -> List[Path]:
    """Return `/Library/Application Support`."""
    return [Path('/Library/Application Support')]


def shared_config() -> List[Path]:
    """Return `/Library/Preferences`."""
    return [Path('/Library/Preferences')]
