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

"""
Bionic is pretty simple library and protocol for IPC-like
inter-process communications.
"""


from . import meta

__author__ = meta.__author__
__copyright__ = meta.__copyright__
__credits__ = meta.__credits__
__license__ = meta.__license__
__version__ = meta.__version__
__maintainer__ = meta.__maintainer__
__email__ = meta.__email__
__status__ = meta.__status__
get_version = meta.get_version

WATCHDOG_SLEEP = 1
