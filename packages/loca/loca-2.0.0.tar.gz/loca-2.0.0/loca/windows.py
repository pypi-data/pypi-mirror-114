# Local locations for Windows
# Copyright (C) 2005-2010  ActiveState Software Inc.
# Copyright (C) 2013  Matěj Cepl
# Copyright (C) 2013, 2014  Sridhar Ratnakumar
# Copyright (C) 2014  Caleb P. Burns
# Copyright (C) 2016  Yen Chi Hsuan
# Copyright (C) 2020  Kevin McClusky
# Copyright (C) 2020  Ofek Lev
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

from ctypes import create_string_buffer, create_unicode_buffer
from contextlib import suppress
from functools import partial
from os import environ
from pathlib import Path
from typing import Any, Callable, List

__doc__ = 'Local locations for Windows'
__all__ = ['user_data', 'shared_data']

REG_PATH = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
CSIDL_ENUM = {'CSIDL_APPDATA': 26,
              'CSIDL_COMMON_APPDATA': 35,
              'CSIDL_LOCAL_APPDATA': 28}
CSIDL_DIRECTORY = {'CSIDL_APPDATA': 'AppData',
                   'CSIDL_COMMON_APPDATA': 'Common AppData',
                   'CSIDL_LOCAL_APPDATA': 'Local AppData'}
CSIDL_ENVIRON = {'CSIDL_APPDATA': 'APPDATA',
                 'CSIDL_COMMON_APPDATA': 'ALLUSERSPROFILE',
                 'CSIDL_LOCAL_APPDATA': 'LOCALAPPDATA'}


def via_ctypes(windll: Any, csidl: str) -> str:
    """Get CSIDL via ctypes."""
    folder = create_unicode_buffer(1024)
    windll.shell32.SHGetFolderPathW(None, CSIDL_ENUM[csidl], None, 0, folder)

    # Downgrade to short path name if have highbit chars:
    # http://bugs.activestate.com/show_bug.cgi?id=85099
    if any(ord(c) > 255 for c in folder):
        short_path = create_unicode_buffer(1024)
        if windll.kernel32.GetShortPathNameW(folder.value, short_path, 1024):
            return short_path.value
    return folder.value


def via_jna(jna: Any, csidl: str) -> str:
    """Get CSIDL via Java native access."""
    win32 = jna.platform.win32
    buf_size = win32.WinDef.MAX_PATH * 2

    folder = create_string_buffer(buf_size)
    win32.Shell32.INSTANCE.SHGetFolderPath(
        None, getattr(win32.ShlObj, csidl), None,
        win32.ShlObj.SHGFP_TYPE_CURRENT, folder)

    # Downgrade to short path name if have highbit chars:
    # http://bugs.activestate.com/show_bug.cgi?id=85099
    if any(ord(c) > 255 for c in folder):
        short_path = create_string_buffer(buf_size)
        get_short_path_name = win32.Kernel32.INSTANCE.GetShortPathName
        if get_short_path_name(folder.value.decode(), short_path, buf_size):
            return short_path.value.decode()
    return folder.value.decode()


def from_registry(winreg: Any, csidl: str) -> str:
    """Get CSIDL from Windows registry.

    The correct answer is not guaranteed for all CSIDL names.
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    return winreg.QueryValueEx(key, CSIDL_DIRECTORY[csidl])[0]


def from_environ(csidl: str) -> str:
    """Get CSIDL from environment variable."""
    return environ[CSIDL_ENVIRON[csidl]]


def csidl_converter() -> Callable[[str], str]:
    """Return the most preferable CSIDL converter that is available."""
    with suppress(ImportError):
        from ctypes import windll  # type: ignore
        return partial(via_ctypes, windll)
    with suppress(ImportError):
        from com.sun import jna  # type: ignore
        return partial(via_jna, jna)
    with suppress(ImportError):
        import winreg
        return partial(from_registry, winreg)
    return from_environ


windows_directory = csidl_converter()


def user_data(roaming: bool) -> Path:
    r"""Return user-specific data directory.

    This is typically `C:\Users\<username>\AppData\Roaming` with roaming
    and `C:\Users\<username>\AppData\Local` without from Windows Vista.
    Roaming directories are synchronized across different machines:
    http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx
    """
    csidl = 'CSIDL_APPDATA' if roaming else 'CSIDL_LOCAL_APPDATA'
    return Path(windows_directory(csidl))


def shared_data() -> List[Path]:
    r"""Return user-shared data directory.

    This is broken on Windows Vista and it is typically `C:\ProgramData`
    from Windows 7 onwards.
    """
    return [Path(windows_directory("CSIDL_COMMON_APPDATA"))]
