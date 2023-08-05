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

"""A set of classes and functions for representing raw data as Bionic models"""

import zlib
import struct
import hashlib
from typing import Union, Optional
from abc import abstractmethod

import orjson
from . import get_version, errors

BIONIC_MAGIC = b"\xBB\x11\xF0\x0F"
BIONIC_POSTMAGIC = b"\xBB\xEE\xFF\xBB"
NULL_UID = b"\x00" * 8
MAX_CHUNK_SIZE = 61440


def hash_data(data: bytes) -> bytes:
    """Hash data"""
    return hashlib.sha256(data).digest()


class TransactionFlags:  # pylint: disable=too-few-public-methods
    """Transaction flags"""
    SERVICE_TRANSACTION = 1 << 0
    CHUNKED_DATA = 1 << 1
    OK_INDICATOR = 1 << 2
    DATA_TRANSACTION = 1 << 3


class BaseModel:
    """Base Bionic data model"""

    def __repr__(self):
        return str(self.get_data())

    @abstractmethod
    def get_data(self):
        """Must return JSON-parsable representation of the model"""
        ...

    def get_raw_data(self) -> bytes:
        """Get raw data from model"""
        return orjson.dumps(self.get_data())


class Error(BaseModel):
    """Bionic errors"""
    error_code: int
    error_message: str

    def __init__(self, error_code: int = -32000, error_message: str = "Unexcepted error"):
        self.error_code = error_code
        self.error_message = error_message

    def get_data(self) -> dict:
        """Get data from model for upper models"""
        return {
            "error_code": self.error_code,
            "error_message": self.error_message
        }


class Result(BaseModel):
    """Bionic result. It can take either only named
    arguments or only positional arguments."""
    result: Union[dict, list, str, int, None]

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and len(kwargs) > 0:
            raise TypeError("Only positioned or only named params is allowed")

        if len(args) == 1:
            self.result = args[0]
        elif len(args) > 1:
            self.result = args
        elif len(kwargs) > 0:
            self.result = kwargs
        else:
            self.result = None

    def get_data(self) -> Union[dict, list, str, int, None]:
        """Get data from model for upper models"""
        return self.result


class Respond(BaseModel):
    """Bionic respond for calls. Can be sent via Bionic connection"""
    bionic: str
    result: Result
    error: Error

    def __init__(self, bionic: str, result: Optional[Result], error: Optional[Error]):
        self.bionic = bionic or get_version()
        self.result = result
        self.error = error

    def get_data(self) -> dict:
        """Get data from model for upper models"""
        return {
            "bionic": self.bionic,
            "result": self.result.get_data() if self.result else None,
            "error": self.error.get_data() if self.error else None,
        }

    def get_error(self) -> tuple:
        """Get error"""
        if not self.error:
            return None
        return (self.error.error_code, self.error.error_message)


class Call(BaseModel):
    """Bionic call. Can be sent via Bionic connection"""
    bionic: str
    method: str
    params: Union[list, dict]

    def __init__(self, bionic: str, method: str, params: Union[list, dict]):
        self.bionic = bionic
        self.method = method
        self.params = params

    def get_data(self) -> dict:
        """Get data from model for upper models"""
        return {
            "bionic": self.bionic,
            "method": self.method,
            "params": self.params,
            "type": "call"
        }


class Notification(BaseModel):
    """Bionic notification. Can be sent via Bionic connection"""
    bionic: str
    method: str
    params: Union[list, dict]

    def __init__(self, bionic: str, method: str, params: Union[list, dict]):
        self.bionic = bionic
        self.method = method
        self.params = params

    def get_data(self) -> str:
        """Get data from model for upper models"""
        return {
            "bionic": self.bionic,
            "method": self.method,
            "params": self.params,
            "type": "notification"
        }


def parse_data(data: bytes) -> Union[Respond, Call, Notification]:
    """Get model from raw data"""
    dummy_obj = object()
    try:
        data_p = orjson.loads(data)
        if not data_p.get("result", dummy_obj) == dummy_obj:
            if data_p.get("result", None):
                data_p["result"] = Result(**data_p["result"]) if isinstance(
                    data_p["result"], dict) else (
                    Result(*data_p["result"]) if isinstance(
                        data_p["result"], list) else Result(data_p["result"]))
            if data_p.get("error", None):
                data_p["error"] = Error(**data_p["error"])
            return Respond(**data_p)
        if data_p.get("type") == "call":
            data_p.pop("type")
            return Call(**data_p)
        if data_p.get("type") == "notification":
            data_p.pop("type")
            return Notification(**data_p)
        raise errors.ParseError
    except Exception:
        raise errors.ParseError from None


def create_respond(data: Union[Result, Error, tuple]):
    """Create respond from Result or Error"""
    if isinstance(data, Result):
        return Respond(bionic=get_version(), result=data, error=None)
    if isinstance(data, Error):
        return Respond(bionic=get_version(), result=None, error=data)
    if isinstance(data, tuple):
        return create_respond(Error(*data))
    raise errors.NoRespondError


def create_raw_request(uid: bytes = NULL_UID, flags: int = 0,
                       chunks_count: int = 1, current_chunk: int = 1,
                       data: bytes = b"") -> bytes:
    """Create raw bionic packet"""
    return BIONIC_MAGIC + uid + struct.pack("BIIHI",
                                            flags, chunks_count, current_chunk,
                                            len(data), zlib.crc32(data)) + data + BIONIC_POSTMAGIC
