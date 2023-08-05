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

# pylint: disable=superfluous-parens

"""Bionic utils for synchronization"""

import asyncio
from asyncio.futures import Future
import logging
from typing import Dict, List
from . import models

dummy = object()


class _DataPromise(asyncio.Future):
    """Custom future for handle chunked and standart data"""
    ...  # Just placeholder


class _ChunkedData(bytearray):
    total_chunks: int
    chunks_received: int
    data_hash: bytes


class UndefinedTaskException(Exception):
    """Undefined task"""
    ...


def _create_chunkeddata() -> _ChunkedData:
    chunked_data = _ChunkedData()
    chunked_data.total_chunks = 0
    chunked_data.chunks_received = 0
    chunked_data.data_hash = b""
    return chunked_data


class NamedQueue:
    """A named queue where each element has its own id

    Provides the ability to asynchronously control the receipt
    and transmission of data. Requires an identifier for each data block
    """

    def __init__(self):
        self._tasks = {}
        self._chunked_tasks = {}
        self._loop = asyncio.get_event_loop()

    def _create_datapromise(self) -> _DataPromise:
        """Create DataPromise"""
        return _DataPromise(loop=self._loop)

    def register(self, uid: bytes):
        """Register an item to the queue.

        It is needed in order to prevent possible errors due to the
        fact that the data will arrive earlier than they may be waited
        """
        fut = self._create_datapromise()
        self._tasks[uid] = fut

    def register_chunked(self, uid: bytes, chunks: int, data_hash: bytes):
        """Register an item to chunked queue.

        This is to correctly accept and join data chunks
        """
        store = _create_chunkeddata()
        store.total_chunks = chunks
        store.data_hash = data_hash

        self._chunked_tasks[uid] = store

    def commit(self, uid: bytes, data: bytes):
        """Commit to unfinished task. All coroutines waiting for
        task finish will be awakened. If task uid isn`t in tasks,
        UndefinedTaskException will be raised.
        """
        fut = self._tasks.get(uid, None)
        if not fut:
            return False
            # raise UndefinedTaskException

        if not fut.done():
            fut.set_result(data)
        del self._tasks[uid]
        return True

    def commit_chunk(self, uid: bytes, data: bytes):
        """Commit to an unfinished chunk task. If number
        of chunks received equals number of all chunks,
        True will be returned.
        """
        store = self._chunked_tasks.get(uid, dummy)
        if store is dummy:
            return False
            # raise UndefinedTaskException

        self._chunked_tasks[uid] += data
        store.chunks_received += 1

        if store.chunks_received == store.total_chunks:
            return True

        return store.chunks_received

    def get_chunked_data(self, uid):
        """Get data from finished chunked task"""
        store = self._chunked_tasks.get(uid, None)
        if not store:
            return False

        if store.chunks_received == store.total_chunks:
            data = bytes(store)
            del self._chunked_tasks[uid]
            if models.hash_data(data) != store.data_hash:
                return None
            return data

        return False

    def clear(self):
        """Reset the internal tasks store to empty state"""
        self._tasks = {}

    def waiters_count(self) -> int:
        """Return waiters count"""
        return len(self._tasks)

    async def wait(self, uid: bytes) -> bytes:
        """Block until the task is not finished."""

        if uid not in self._tasks:
            raise UndefinedTaskException

        fut = self._tasks[uid]
        return await fut


class ConnectionManager:
    """Manage connections"""
    _connection_futures: Dict[str, Future] = {}
    _noset_conns: List = []

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._logger = logging.getLogger("ConnectionManager")

    def __call__(self, label) -> Future:
        if label not in self._connection_futures:
            fut = self._loop.create_future()
            self._connection_futures[label] = fut
        return self._connection_futures[label]

    def get_state(self, label) -> bool:
        """Returns True if connection available, False if else"""
        if not (fut := self._connection_futures.get(label, None)):
            return False
        return fut.done()

    def get_rstate(self, connection) -> bool:
        """Returns True if connection associated with label, False if else"""
        return connection in [
            fut.result() for fut in self._connection_futures.values() if fut.done()]

    def register(self, connection) -> bool:
        """Register connection"""
        if connection not in self._noset_conns:
            self._noset_conns.append(connection)

            def kickme_cb():
                if connection.label:
                    self.revoke(connection.label)
                if connection in self._noset_conns:
                    self._noset_conns.remove(connection)

            connection.kickout_me = kickme_cb
            return True
        return False

    def assign_label(self, connection, label) -> bool:
        """Assign label to connection"""
        if connection not in self._noset_conns:
            self._logger.fatal(
                "Failed to assing label for unregistered connection")
            return False

        if not (fut := self._connection_futures.get(label, False)):
            fut = self._loop.create_future()
            self._connection_futures[label] = fut
        if not fut.done():
            self._noset_conns.remove(connection)
            fut.set_result(connection)
            connection.label = label
            return True
        return False

    def revoke(self, label) -> bool:
        """Revoke label from connection"""
        if not (self._connection_futures.get(label, False) and
                self._connection_futures[label].done()):
            return False
        self._connection_futures[label] = self._loop.create_future()
        return True


class ConnectionLock:
    """Lock for sync connections"""

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._fut = self._loop.create_future()

    def __await__(self):
        """Async wait"""
        return self._fut.__await__()

    def get_state(self):
        """Returns True if locked, False if unlocked"""
        return self._fut.done()

    def lock(self):
        """Lock connection"""
        if self._fut.done():
            return False
        self._fut.set_result(True)
        return True

    def unlock(self):
        """Unlock connection"""
        if not self._fut.done():
            return False
        self._fut = self._loop.create_future()
        return True
