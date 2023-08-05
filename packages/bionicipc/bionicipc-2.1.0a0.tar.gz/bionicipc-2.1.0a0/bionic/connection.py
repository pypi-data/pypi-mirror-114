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

"""Abstractions for representing asyncio stream as Bionic Connection"""

import os
import zlib
import struct
import asyncio

import warnings
import logging

from typing import Callable, Union

from . import models, errors, utils
from .sync import NamedQueue

logger = logging.getLogger("Connection")


async def fallback_cb(connection: 'Connection', data: Union[models.Respond, models.Call]):
    """Dummy fallback cb"""
    warnings.warn(
        "Fell in fallback_cb, please set callback for connection")
    return errors.INTERNAL_SERVER_ERROR


class Connection:
    """Bionic connection

    High level abstraction for asyncio socket stream. Designed for
    Bionic models. Uses a string that is separated from the data with
    a space to identify calls and returns. Takes asyncio.StreamReader
    and asyncio.StreamWriter, obtained from asyncio server callback.
    After initialization it starts infinite stream listening (listen_loop).
    """
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter
    _queue: NamedQueue = NamedQueue()
    _ok_waiting: dict = {}
    callback = fallback_cb
    closed: bool = False
    kickout_me: Callable = lambda *_: None
    label: str = "NOSET"

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        logger.debug("Initiated a new connection")
        self._reader = reader
        self._writer = writer
        asyncio.ensure_future(self.listen_loop())

    def set_callback(self, func: Callable):
        """Set callback for connection"""
        self.callback = func or fallback_cb

    async def _communicate(self, data: bytes, register: bool = True, uid: bytes = None) -> bytes:
        """Internal method for low-level communicate with other side
        of the connection. Generates uid if not provided. Auto register
        request to queue, if need.
        """
        if uid and len(uid) != 8:
            raise TypeError("bad uid")
        uid = uid or os.urandom(8)
        if register:
            logger.debug("Registering %s in queue", str(uid))
            self._queue.register(uid)
        if len(data) > models.MAX_CHUNK_SIZE:
            total_chunks = utils.calc_chunks(data, models.MAX_CHUNK_SIZE)
            logger.debug(
                "Preparing transmission of chunked data (%i chunks) with uid %s",
                total_chunks, uid.hex())
            flags = models.TransactionFlags.SERVICE_TRANSACTION |\
                models.TransactionFlags.CHUNKED_DATA
            data_hash = models.hash_data(data)
            rawreq = models.create_raw_request(
                uid, flags, total_chunks, 0, data_hash)
            fut = asyncio.Future()
            self._ok_waiting[uid] = fut
            logger.debug("Sending indicator of starting chunked transmission")
            self._writer.write(rawreq)
            await self._writer.drain()
            logger.warning("Waiting for ok for %s", uid.hex())
            if not await fut:
                del self._ok_waiting[uid]
                logger.fatal(
                    "Failed to send chunked data with uid %s", uid.hex())
                return None
            del self._ok_waiting[uid]
            data_flags = models.TransactionFlags.DATA_TRANSACTION |\
                models.TransactionFlags.CHUNKED_DATA
            logger.debug("Starting data transmission.")
            for num, chunk in enumerate(utils.chunked_iter(data, models.MAX_CHUNK_SIZE)):
                logger.debug("sending %i", num)
                rreq = models.create_raw_request(
                    uid, data_flags, total_chunks, num+1, chunk)
                self._writer.write(rreq)
            fut = asyncio.Future()
            self._ok_waiting[uid] = fut
            await self._writer.drain()
            if not await fut:
                del self._ok_waiting[uid]
                logger.fatal(
                    "Failed to send chunked data with uid %s", uid.hex())
                return None
            del self._ok_waiting[uid]
        else:
            logger.debug("Preparing for send %s", uid.hex())
            flags = models.TransactionFlags.DATA_TRANSACTION
            d_req = models.create_raw_request(
                uid, flags, 0, 0, data)
            self._writer.write(d_req)
            await self._writer.drain()
        return uid

    async def _raise_internal_error(self, error: tuple, uid: bytes = models.NULL_UID):
        await self._communicate(
            models.create_respond(models.Error(*error)).get_raw_data(), register=False, uid=uid)

    async def _send_ok(self, uid: bytes = models.NULL_UID):
        """Send OK indicator"""
        logger.debug("Sending ok for %s", uid.hex())
        self._writer.write(
            models.create_raw_request(
                uid, models.TransactionFlags.SERVICE_TRANSACTION |
                models.TransactionFlags.OK_INDICATOR, 0, 0, b""))
        await self._writer.drain()

    def get_wait_tasks(self) -> int:
        """Get socket i/o waiters

        Returns waiters count as integer.
        """
        return self._queue.waiters_count()

    async def _requests_handler(
            self, uid: bytes,
            flags: int, chunks_count: int,
            curr_chunk: int, data: bytes):
        service_transaction = flags & models.TransactionFlags.SERVICE_TRANSACTION
        chunked = flags & models.TransactionFlags.CHUNKED_DATA
        ok_indicator = flags & models.TransactionFlags.OK_INDICATOR
        data_transaction = flags & models.TransactionFlags.DATA_TRANSACTION
        if service_transaction and ok_indicator:
            logger.debug("Received ok for %s", uid.hex())
            okfut = self._ok_waiting.get(uid, None)
            if uid:
                okfut.set_result(True)
            else:
                logger.debug("No one waiting for %s ok", uid.hex())
            return

        if service_transaction and chunked:
            if not curr_chunk == 0:
                logger.warning("Protocol fields error.")
                await self._raise_internal_error(errors.PROTOCOL_FIELDS_ERROR, uid)
                return
            logger.debug(
                "Registering start of chunked transaction (%i chunks) for %s",
                chunks_count, uid.hex())
            self._queue.register_chunked(uid, chunks_count, data)
            await self._send_ok(uid)
            return

        if chunked and data_transaction:
            logger.debug("Received chunk %i/%i of %s",
                         curr_chunk, chunks_count, uid.hex())
            try:
                comm = self._queue.commit_chunk(uid, data)
                if not comm:
                    logger.warning(
                        "Unregistered chunk transaction for %s", uid.hex())
                    await self._raise_internal_error(
                        errors.UNREGISTERED_CHUNK_TRANSACTION)
                    return
                if comm is True:
                    data = self._queue.get_chunked_data(uid)
                    if not data:
                        logger.error(
                            "Corrupted data received for %s. Buffers cleared.", uid.hex())
                    logger.debug("Chunked task %s done.", uid.hex())
                    await self._send_ok(uid)
                else:
                    return
            except errors.NonChunkedDataAssign:
                await self._raise_internal_error(
                    errors.NONCHUNKED_DATA_ASSIGN, uid)
                return

        if data_transaction:
            logger.debug(
                "Default data transaction received for %s", uid.hex())
            if not self._queue.commit(uid, data):
                logger.debug("%s not in queue, calling cb", uid.hex())
                try:
                    pdata = models.parse_data(data)
                except errors.ParseError:
                    await self._raise_internal_error(errors.TRANSACTION_PARSE_ERROR, uid)
                    return
                call = False
                if isinstance(pdata, models.Call):
                    call = True
                try:
                    ret = await self.callback(self, pdata)
                except Exception:  # pylint: disable=broad-except
                    logger.exception("Error while executing callback")
                    await self._raise_internal_error(errors.INTERNAL_SERVER_ERROR, uid)
                    return
                if not ret:
                    if call:
                        logger.error(
                            "Callback must return smth, because %s is call.", uid)
                        await self._raise_internal_error(errors.INTERNAL_SERVER_ERROR, uid)
                        return
                    await self._communicate(b"ok", register=False, uid=uid)
                else:
                    await self._communicate(
                        models.create_respond(ret).get_raw_data(), register=False, uid=uid)

    async def listen_loop(self):
        """Infinite listen loop

        Used by all internal tasks to obtain any data from other side of
        the connection. Uses NamedQueue to synchronize data distribution.
        """
        while True:
            try:
                data_raw = await self._reader.readuntil(models.BIONIC_POSTMAGIC)
            except (asyncio.IncompleteReadError, ConnectionResetError):
                logger.debug("Read failed, closing connection!")
                self._writer.close()
                await self._writer.wait_closed()
                self.closed = True
                self.kickout_me()
                return
            logger.debug("Received data. Parsing...")
            if data_raw[0:4] != models.BIONIC_MAGIC:
                logger.warning("Invalid magic number")
                await self._raise_internal_error(errors.DATA_CORRUPTED_ERROR)
                continue

            uid = data_raw[4:12]
            if uid == models.NULL_UID:
                # Temporary ignoring of NULL_UID transactions. Should be fixed soon
                continue
            to_unpack = data_raw[12:32]
            flags, chunks_count, curr_chunk, data_len, data_crc = struct.unpack(
                "BIIHI", to_unpack)

            data = data_raw[32:32+data_len]

            if data_raw[32+data_len:32+data_len+4] != models.BIONIC_POSTMAGIC:
                logger.warning("Invalid data.")
                await self._raise_internal_error(errors.DATA_CORRUPTED_ERROR)
                continue

            if not zlib.crc32(data) == data_crc:
                logger.debug("Invalid data CRC for %s, skipping...", uid.hex())
                await self._raise_internal_error(errors.DATA_CORRUPTED_ERROR)
                continue

            asyncio.ensure_future(self._requests_handler(
                uid, flags, chunks_count, curr_chunk, data))

    async def wait_data(self, uid: str) -> bytes:
        """Block until the uid data is received

        Waiting for listen_loop to get data that matches the given
        uid. Returns bytes on completion.
        """
        logger.debug("Waiting for %s", uid)
        return await self._queue.wait(uid)

    async def send_call(self, call: models.Call) -> models.Respond:
        """Send Bionic call to other side of the connection

        Sends the other side of the connection a Bionic call, and
        blocks it until it receives a reply. Can raise the response
        parsing exception.
        """
        logger.debug("Sending call")
        uid = await self._communicate(call.get_raw_data())
        return models.parse_data(await self.wait_data(uid))

    async def send_notification(self, notification: models.Notification) -> bool:
        """Send Bionic notification to other side of the connection

        Sends the other side of the connection a Bionic notification, and
        blocks it until it receives a reply. Can raise the response
        parsing exception.
        """
        logger.debug("Sending notification")
        uid = await self._communicate(notification.get_raw_data())
        if (await self.wait_data(uid)) == b"ok":
            return True
        logger.warning("Notification failed!")
        return False


def create_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> Connection:
    """Create Connection from asyncio StreamReader and StreamWriter
    """
    return Connection(reader, writer)
