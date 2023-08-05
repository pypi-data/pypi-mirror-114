# Copyright 2020-2021 h3xcode
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# cuz bug with unsubscriptable Union in Python 3.9
# pylint: disable=unsubscriptable-object

"""
Internal file for define metainformation

Do not import information from this file, import it from bionic __init__ instead.
"""

__author__ = "h3xcode"
__copyright__ = "Copyright 2021, Bionic IPC"
__credits__ = []
__license__ = "Apache 2.0"
__version__ = "2.1.0a0"
__maintainer__ = "h3xcode"
__email__ = "me@h3xco.de"
__status__ = "Development"

supported_versions = [(2, 0)]


def get_version() -> str:
    """Get the maximum version of the Bionic protocol supported by the current library"""
    return ".".join([str(i) for i in supported_versions[-1]])


def check_version(ver: str) -> bool:
    """Checking whether the current library supports the Bionic protocol version"""
    return tuple(map(int, ver.split("."))) in supported_versions
