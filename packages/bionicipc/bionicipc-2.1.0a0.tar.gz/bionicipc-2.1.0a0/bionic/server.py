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

"""Module with high-level server abstractions for Bionic IPC"""

import asyncio
import logging

from typing import Callable, Dict, Union

from . import models, utils, get_version
from .connection import create_connection
from .errors import recognize_error
from .sync import ConnectionManager
from . import errors

logger = logging.getLogger("BionicServer")


class BionicServer:
    """Bionic server"""
    _conn_manager: ConnectionManager = ConnectionManager()
    callback_func: callable = None
    _call_handlers: Dict[str, Callable] = {}
    _notify_handlers: Dict[str, Callable] = {}

    def __init__(self):
        logger.info("Initializing BionicIPC v%s", get_version())
        self._loop = asyncio.get_event_loop()

    def set_callback(self, func: callable):
        """Set callback for connection"""
        self.callback_func = func

    async def _pre_cb(self, connection, data):
        if data.method == "__bionic.reg_me" and isinstance(data.params, dict) \
                and connection.label == "NOSET":
            if label := data.params.get("label", False):
                if self._conn_manager.get_state(label):
                    return errors.LABEL_COLLISION_ERROR
                self._conn_manager.assign_label(connection, label)
                connection.label = label
                return models.Result(label)
        if not self._conn_manager.get_state(connection.label):
            return errors.UNREGISTERED_CLIENT_ERROR
        if data.method in self._call_handlers and isinstance(data, models.Call):
            return await self._call_handlers[data.method](connection, data)
        if data.method in self._notify_handlers and isinstance(data, models.Notification):
            return await self._notify_handlers[data.method](connection, data)
        return await self.callback_func(connection, data)

    async def _internal_callback(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Connection listener"""
        logger.info(
            "New connection from %s:%i!", *writer.get_extra_info("peername"))
        # if self._connection_lock.get_state():
        #     writer.close()
        #     await writer.wait_closed()
        #     return None
        conn = create_connection(reader, writer)
        logger.warning("Connection established with %s:%i",
                       *writer.get_extra_info("peername"))
        conn.set_callback(self._pre_cb)
        self._conn_manager.register(conn)

    async def wait_connection(self, label):
        """Wait for connection"""
        return await self._conn_manager(label)

    async def send_call(self, label: str, method: str, params: Union[list, dict],
                        raise_on_error: bool = False, return_only_result: bool = False):
        """Wrapper for Connection.send_call()"""
        try:
            conn = await self._conn_manager(label)
            result = await conn.send_call(
                models.Call(
                    get_version(),
                    method,
                    params
                )
            )
            utils.raise_if_flag(recognize_error(result.error), raise_on_error)
            return result.result if return_only_result else result
        except ConnectionResetError:
            logger.warning(
                "Looks like no connection. Pausing transactions...")
            self._conn_manager.revoke(label)
            await self._conn_manager(label)
            return await self.send_call(label, method, params, raise_on_error, return_only_result)

    async def send_notification(self, label: str, method: str, params: Union[list, dict]):
        """Wrapper for Connection.send_notification()"""
        try:
            conn = await self._conn_manager(label)
            return await conn.send_notification(
                models.Notification(
                    get_version(),
                    method,
                    params
                )
            )
        except ConnectionResetError:
            logger.warning(
                "Looks like no connection. Pausing all transactions...")
            self._conn_manager.revoke(label)
            await self._conn_manager(label)
            return await self.send_notification(label, method, params)

    def add_call_handler(self, method: str, func: Callable):
        """Add handler to call handlers list

        func will be called if Call received with
        required method."""
        self._call_handlers[method] = func

    def add_notification_handler(self, method: str, func: Callable):
        """Add handler to notification handlers list

        func will be called if Notification received with
        required method."""
        self._notify_handlers[method] = func

    def call_handler(self, method):
        """Wrapper for call handlers

        Shorthand for add_call_handler

        Example:
            @server.call_handler("example")
            async def example_call_handler(conn, data):
                return models.Result("hello world")
        """
        def _funcreceiver(func):
            self.add_call_handler(method, func)
            return func

        return _funcreceiver

    def notification_handler(self, method):
        """Wrapper for call handlers

        Shorthand for add_call_handler

        Example:
            @server.notification_handler("example")
            async def example_notification_handler(conn, data):
                print("Hello world!") # notification handler should return None
        """
        def _funcreceiver(func):
            self.add_notification_handler(method, func)
            return func

        return _funcreceiver

    def start_server(self, host: str = "127.0.0.1", port: int = 8122):
        """Start listening"""
        logger.info("Listening %s on %i", host, port)
        return asyncio.start_server(self._internal_callback, host, port)
