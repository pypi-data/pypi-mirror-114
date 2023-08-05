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

"""Working with errors"""

from typing import Union

from . import utils

_builtin_errors = {
    "INTERNAL_SERVER_ERROR": (-32500, "Internal server error"),
    "TRANSACTION_PARSE_ERROR": (-32408, "Parse error"),
    "DATA_CORRUPTED_ERROR": (-32409, "Data corrupted"),
    "NONCHUNKED_DATA_ASSIGN": (-32410, "Cannot attach data to a non-chunk task"),
    "UNREGISTERED_CHUNK_TRANSACTION": (-32411, "Unregistered chunked transaction"),
    "PROTOCOL_FIELDS_ERROR": (-32412, "Error in transaction fields"),
    "UNREGISTERED_CLIENT_ERROR": (-32413, "Unregistered client"),
    "LABEL_COLLISION_ERROR": (-32414, "Label collision")
}

INTERNAL_SERVER_ERROR = _builtin_errors["INTERNAL_SERVER_ERROR"]
TRANSACTION_PARSE_ERROR = _builtin_errors["TRANSACTION_PARSE_ERROR"]
DATA_CORRUPTED_ERROR = _builtin_errors["DATA_CORRUPTED_ERROR"]
NONCHUNKED_DATA_ASSIGN = _builtin_errors["NONCHUNKED_DATA_ASSIGN"]
UNREGISTERED_CHUNK_TRANSACTION = _builtin_errors["UNREGISTERED_CHUNK_TRANSACTION"]
PROTOCOL_FIELDS_ERROR = _builtin_errors["PROTOCOL_FIELDS_ERROR"]
UNREGISTERED_CLIENT_ERROR = _builtin_errors["UNREGISTERED_CLIENT_ERROR"]
LABEL_COLLISION_ERROR = _builtin_errors["LABEL_COLLISION_ERROR"]


class ParseError(Exception):
    """Exception for errors during parsing of raw data"""

    def __init__(self):
        super().__init__("Invalid data")


class NoRespondError(Exception):
    """Creating respond error"""

    def __init__(self):
        super().__init__("Invalid respond")


class BionicError(Exception):
    """Base class for Bionic errors"""

    def __init__(self, msg=""):
        super().__init__(msg or self.__doc__)


class InternalServerError(BionicError):
    """Internal server error. Similiar to HTTP 500"""

    def __init__(self):
        super().__init__(
            "An internal error occurred while processing a request "
            "on the server that cannot be handled on the server or client")


class TransactionParseError(BionicError):
    """Data parsing error"""

    def __init__(self):
        super().__init__(
            "A transaction parsing error occurred on the server while processing a request")


class NonChunkedDataAssign(BionicError):
    """Attempt to assign chunked data to non-chunked task"""
    ...


class UnregisteredClientError(BionicError):
    """Unregistered client"""
    ...


class LabelCollisionError(BionicError):
    """Label collision"""
    ...


class GenericBionicError(BionicError):
    """Any other error"""

    def __init__(self, error):
        self.error_code, self.error_message = None, None
        if isinstance(error, int):
            super().__init__("Error %i occured with no description" % (error))
            self.error_code = error
        elif isinstance(error, (tuple, list)):
            super().__init__("[Error %i]: %s" % error)
            self.error_code, self.error_message = error


getobj = utils.make_getobj(__name__)


def recognize_error(error: Union[tuple, int]):
    """Generate error object from tuple or int"""
    cls_ = getobj(utils.convert_builtin_to_class(utils.reverse_get(
        _builtin_errors, error) or utils.deep_err_search(_builtin_errors, error)))
    if cls_:
        return cls_
    return None
