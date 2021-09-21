# GPLv3 License
#
# Copyright (C) 2020 Ubisoft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Utility functions that may require os/platform specific adjustments
"""

import subprocess
import os
from pathlib import Path
import sys


def open_folder(path):
    """
    Open a path or an URL with the application specified by the os
    """
    if sys.platform == "darwin":
        subprocess.check_call(["open", "--", path])
    elif sys.platform == "linux":
        subprocess.check_call(["xdg-open", path])
    elif sys.platform == "win32":
        subprocess.Popen(f'explorer "{Path(path)}"')


def delete_folder(dir_path):
    if os.path.exists(dir_path):
        files_in_directory = os.listdir(dir_path)
        # filtered_files = [file for file in files_in_directory if file.endswith(".png") or file.endswith(".wav")]

        for file in files_in_directory:
            path_to_file = os.path.join(dir_path, file)
            try:
                os.remove(path_to_file)
            except Exception:
                # _logger.exception(f"\n*** File locked (by system?): {path_to_file}")
                print(f"\n*** File locked (by system?): {path_to_file}")
        try:
            os.rmdir(dir_path)
        except Exception:
            print("Cannot delete Dir: ", dir_path)


def internet_on():
    """Check if a web url can be reached.
    Return True if the url is found, False otherwise.
    *** Warning: On Mac OS False is always returned if the certifi Python lib is not installed.
    The returned value has then be forced to True. ***
    See: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    """
    # Mac specific:
    if sys.platform == "darwin":
        return True

    import urllib.request
    import urllib.error

    for timeout in [1, 5, 10, 15]:
        try:
            urllib.request.urlopen("https://google.com", timeout=timeout)
            return True
        except urllib.error.URLError:
            pass
    return False


def module_can_be_imported(name):
    """Check if the specified module already exists in the current Python environment
    To get a submodule: eg: module_can_be_imported("stampinfo.otio")
    """
    modules_list = []
    try:
        __import__(name, fromlist=modules_list)
        return True
    except ModuleNotFoundError:
        return False
