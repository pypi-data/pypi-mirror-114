"""Request and response message handling.


Copyright (C) 2016,2017  Ismael Asensio (ismailof@github.com)
Copyright (C) 2020,2021  svinerus (svinerus@gmail.com)
Copyright (C) 2021  Stephan Helma

This file is part of mopidy-asyncio-client.

mopidy-asyncio-client is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

mopidy-asyncio-client is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with mopidy-asyncio-client. If not, see <https://www.gnu.org/licenses/>.

"""

import asyncio
import json
from itertools import count


class RequestMessage:
    """The request message and its handling."""

    msg_counter = count()

    def __init__(self, request, timeout=20, **kwargs):
        """Initialize the `RequestMessage` class.

        Parameters
        ----------
        request : str
            One of Mopidy's core API requests.
            (https://docs.mopidy.com/en/latest/api/core/#core-api)
        timeout : int, optional
            How long to wait for Mopidy's reply (in seconds).
            The default is 20.
        **kwargs
            Keyword arguments to be sent with the request as data.

        Returns
        -------
        None.

        """
        # Increase the counter across all instances of `RequestMessage`
        self.id_msg = next(self.msg_counter)

        self.request = request
        self.params = kwargs

        self._timeout = timeout
        self._on_result_event = asyncio.Event()
        self._result = None

    async def unlock(self, result):
        """Unlock task and store result."""
        self._result = result
        self._on_result_event.set()

    async def wait_for_result(self):
        """Wait for and return result."""
        await asyncio.wait_for(
            self._on_result_event.wait(),
            self._timeout)
        return self._result

    def to_json(self):
        """Convert the request to a JSON string."""
        return json.dumps({
            'jsonrpc': '2.0',
            'id': self.id_msg,
            'method': self.request,
            'params': self.params})

#    def __str__(self):
    def __repr__(self):
        return (
            f'<RequestMessage('
            f'request={self.request}, '
            f'{", ".join([f"{k}={repr(v)}" for k, v in self.params.items()])} '
            f'id:{self.id_msg}>')


class ResponseMessage:
    """Handling of the response message."""

    def __init__(self,
                 on_msg_event=None, on_msg_result=None,
                 parse_results=False):
        """Initialize the `ResponseMessage` class.

        Parameters
        ----------
        on_msg_event : callable|None, optional
            The function, which should be called, if an event is handled. The
            function will be called as
            `on_msg_event(event=event, event_data=msg_data)`.
            The default is `None`.
        on_msg_result : callable|None, optional
            The function, which should be called, if a rpc response is
            handled. The function will be called as
            `on_msg_result(id_msg=msg_id, result=data)`.
            The default is `None`.
        parse_results : bool, optional
            If `True`, the result should be parsed by a local `mopidy`
            installation.
            The default is `False`.

        Raises
        ------
        ImportError
            If `parse_results` is requested, but a local installation of
            `mopidy` cannot be found.

        Returns
        -------
        None.

        """
        self._on_event = on_msg_event
        self._on_result = on_msg_result

        if parse_results:
            try:
                from mopidy import models
            except ImportError as e:
                raise ImportError(
                    f"If you want to parse results "
                    f"you have to install mopidy locally: "
                    f"{e}")
            else:
                self._decoder = models.model_json_decoder
        else:
            self._decoder = None

    async def parse_json_message(self, message):
        """Parse a JSON message and act on it."""
        msg_data = json.loads(message, object_hook=self._decoder)

        if 'jsonrpc' in msg_data:
            await self._jsonrpc_message(msg_data)
        if 'event' in msg_data:
            await self._event_message(msg_data)

    async def _jsonrpc_message(self, msg_data):
        """Act on a rpc response."""
        if self._on_result is None:
            return

        if msg_data['jsonrpc'] != '2.0':
            raise TypeError(
                f"Wrong JSON-RPC version: {msg_data['jsonrpc']}. "
                f"Need version 2.0.")
        if 'id' not in msg_data:
            raise ValueError('JSON-RPC message has no id')

        msg_id = msg_data.get('id')
        error_data = msg_data.get('error')
        result_data = msg_data.get('result')

        if error_data:
            await self._on_result(id_msg=msg_id, result=error_data)
        else:
            await self._on_result(id_msg=msg_id, result=result_data)

    async def _event_message(self, msg_data):
        """Act on an event."""
        if self._on_event is None:
            return

        event = msg_data.pop('event')
        await self._on_event(event=event, event_data=msg_data)
