"""An async client talking to a remote instance of Mopidy via a websocket.

It uses the JSON/RPC interface provided by Mopidy.

See https://docs.mopidy.com/en/latest/api/http/


Copyright (C) 2016,2017  Ismael Asensio (ismailof@github.com)
Copyright (C) 2020  Jörg (https://github.com/joergrs
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
import logging
from collections import defaultdict

import websockets

from . import mopidy_api
from .messages import RequestMessage, ResponseMessage

logger = logging.getLogger('mopidy_asyncio_client')


class MopidyClient:
    """Interface to a remotely running Mopidy instance."""

    def __init__(self, host='localhost', port=6680,
                 loop=None, parse_results=False,
                 reconnect_attempts=5, reconnect_timeout=20):
        """Initialize the `MopidyClient` class.

        Parameters
        ----------
        host : str, optional
            The host name or IP address, where the remote Mopidy can be found.
            The default is `"localhost"`.
        port : type, optional
            The port number, on which the remote Mopidy instance is listening.
            The default is `6680`.
        loop : TYPE, optional
            The event loop to be used. If `None`, `asyncio`'s event loop is
            used.
            The default is `None`.
        parse_results : bool, optional
            If the result should be parsed by Mopidy. If `True`, `mopidy` has
            to be installed locally.
            The default is `False`.
        reconnect_attempts : int|None, optional
            How often it should be tried to connect. If `None`, try forever.
            The default is `5`.
        reconnect_timeout : int, optional
            The time in seconds to wait between connection attempts.
            The default is `20`.

        Returns
        -------
        None.

        """

        # Listener
        self.eventhandler = MopidyEventHandler()

        # Controllers
        self.core = mopidy_api.CoreController(self._request)
        self.playback = mopidy_api.PlaybackController(self._request)
        self.mixer = mopidy_api.MixerController(self._request)
        self.tracklist = mopidy_api.TracklistController(self._request)
        self.playlists = mopidy_api.PlaylistsController(self._request)
        self.library = mopidy_api.LibraryController(self._request)
        self.history = mopidy_api.HistoryController(self._request)

        # Websocket URI
        self.ws_uri = f'ws://{host}:{port}/mopidy/ws'

        # Special loop?
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        # Websocket
        self.websocket = None
        self._request_queue = []
        self._consumer_task = None

        # Reconnect control
        self._reconnect_attempts = reconnect_attempts
        self._reconnect_timeout = reconnect_timeout

        # Parser for response message
        self.response_parser = ResponseMessage(
            on_msg_event=self._dispatch_event,
            on_msg_result=self._dispatch_result,
            parse_results=parse_results)

        # Build string for __str__()
        identity = ['Remote Mopidy (']
        identity.append(host)
        if port != 6680:
            identity.extend((':', port))
        identity.append(')')
        # Save it
        self._str = ''.join(identity)

        # Build string for __repr__()
        self._repr = (
            f'{self.__class__.__name__}('
            f'host={repr(host)}, '
            f'port={repr(port)}, '
            f'loop={repr(loop)}, '
            f'parse_results={repr(parse_results)}, '
            f'reconnect_attempts={repr(self._reconnect_attempts)}, '
            f'reconnect_timeout={repr(self._reconnect_timeout)}'
            f')')

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._repr

    #
    # Event handler public proxy functions
    #

    def bind(self, event, callback):
        """Bind a callback to an event."""
        self.eventhandler.bind(event, callback)

    def unbind(self, event, callback):
        """Remove a callback from an event."""
        self.eventhandler.unbind(event, callback)

    def clear(self):
        """Remove all callbacks."""
        self.eventhandler.clear()

    #
    # Connection public functions
    #

    async def connect(self):
        """Connect to remote Mopidy instance.

        If it fails, try to reconnect.

        Returns
        -------
        None.

        """
        try:
            await self._connect()
        except OSError:
            await self._reconnect()

    async def _connect(self):
        """Connect to remote Mopidy instance via websockets.

        Raises
        ------
        RuntimeWarning
            If already connected to the remote Mopidy.

        Returns
        -------
        None.

        """
        if self.is_connected():
            raise RuntimeWarning(
                f"Connection to {self.ws_uri} is already open.")

        self.websocket = await websockets.connect(
            self.ws_uri, loop=self._loop)

        self._consumer_task = self._loop.create_task(self._ws_consumer())

        logger.info("Connected to %s", self.ws_uri)

    async def disconnect(self):
        """Disconnect from remote Mopidy instance."""
        if self.is_connected():
            await self.websocket.close()
            logger.info("Connection to %s closed", self.ws_uri)
        else:
            logger.info("Connection to %s is already closed", self.ws_uri)
        if self._consumer_task is not None:
            self._consumer_task.cancel()
        self._request_queue.clear()
        self._consumer_task = None
        self.websocket = None

    def is_connected(self):
        """Are we connected to the remote Mopidy instance?

        Returns
        -------
        bool
            `True`, if connected to the remote Mopidy instance.

        """
        return self.websocket and self.websocket.open

    async def _reconnect(self):
        """Reconnect to the remote Mopidy instance.

        Depending on the value of `self._reconnect_attempts`, this can take
        one of the two following forms:
            `None`:
                Try to reconnect forever.
            int:
                Try to reconnect for the given number of times.

        It will alsways wait `self._reconnect_timeout` seconds between the
        reconnection attempts.

        Raises
        ------
        Exception
            If `self._reconnect_attempts` is not none, the exceptions raised
            during the last connection attempt is re-raised.

        Returns
        -------
        None.

        """

        async def _reconnect_():
            """Try to connect for a maximum of '_reconnect_attempts'."""
            await self.disconnect()
            for i in range(self._reconnect_attempts):
                logger.info(
                    "Try to reconnect to %s. Attempt %s of %s.",
                    self.ws_uri, i, self._reconnect_attempts)
                try:
                    await self._connect()
                except OSError:
                    if i < self._reconnect_attempts - 1:
                        logger.info(
                            "Reconnect to %s failed. Next attempt in %s sec.",
                            self.ws_uri, self._reconnect_timeout)
                        await asyncio.sleep(self._reconnect_timeout)
                    else:
                        raise   # Re-raise very last failed attempt
                else:
                    return

        async def _reconnect_forever_():
            """Try to connect forever."""
            await self.disconnect()
            while True:
                logger.info("Try to reconnect to %s.", self.ws_uri)
                try:
                    await self._connect()
                except OSError:
                    logger.info(
                        "Reconnect to %s failed. Next attempt in %s sec.",
                        self.ws_uri, self._reconnect_timeout)
                    await asyncio.sleep(self._reconnect_timeout)
                else:
                    return

        # Because this `Task` will be closed, we create a new one
        if self._reconnect_attempts is None:
            await _reconnect_forever_()
        else:
            await _reconnect_()

    #
    # websocket requests
    #

    async def _request(self, request, **kwargs):
        """Send a request to the remote Mopidy instance.

        Parameters
        ----------
        request : str
            One of Mopidy's core API requests.
            (https://docs.mopidy.com/en/latest/api/core/#core-api)
        **kwargs
            Keyword arguments to be sent with the request as data.

        Returns
        -------
        any
            The data returned by Mopidy in response to the request.

        """
        if not self.is_connected():
            await self._reconnect()

        request = RequestMessage(request, **kwargs)
        self._request_queue.append(request)

        logger.debug("Send request %s.", request)
        while True:
            if self.websocket is None:
                # Try to connect ...
                await self._reconnect()
                # ... and try to again
                continue

            try:
                # Send request ...
                await self.websocket.send(request.to_json())
            except websockets.ConnectionClosed:
                # Try to reconnect
                await self._reconnect()
                continue
            except Exception as ex:
                # Log exceptions ...
                logger.exception(ex)
                # ... and proceed without raising an error
                return '{}'
            else:
                break

        try:
            # ... and return the data returned
            return await request.wait_for_result()
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for request %s", request)
            return '{}'

    async def _ws_consumer(self):
        try:
            async for message in self.websocket:
                try:
                    await self.response_parser.parse_json_message(message)
                except Exception as ex:
                    logger.exception(ex)
        except websockets.ConnectionClosed:
            await self._reconnect()

    async def _dispatch_result(self, id_msg, result):
        for request in self._request_queue:
            if request.id_msg == id_msg:
                self._loop.create_task(request.unlock(result))
                self._request_queue.remove(request)
                return

    async def _dispatch_event(self, event, event_data):
        # noinspection PyProtectedMember
        self._loop.create_task(self.eventhandler._on_event(event, event_data))

    #
    # Support for asyncio's `with:` blocks
    #

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


class MopidyEventHandler:
    """Handler for Mopidy events.

    See:
        https://docs.mopidy.com/en/latest/api/core/#core-events

    """

    EVENTS = (
        'mute_changed',             # The mute state has changed
        '*',                        # All events ('on_event')
        'options_changed',          # An option has changed
        'playback_state_changed',   # The playback state has changed
        'playlist_changed',         # A playlist has changed
        'playlist_deleted',         # A playlist has deleted
        'playlists_loaded',         # The playlists have loaded or refreshed
        'seeked',                   # The time position has changed
        'stream_title_changed',     # The currently playing stream title has changed
        'track_playback_ended',     # The playback of a track has ended
        'track_playback_paused',    # The playback of a track has paused
        'track_playback_resumed',   # The playback of a track has resumed
        'track_playback_started',   # The playback of a track has started
        'tracklist_changed',        # The tracklist has changed
        'volume_changed',           # The volume has changed
        'audio_message'     # extra event for gstreamer plugins like spectrum
    )

    def __init__(self):
        """Initialize the `MopidyEventHandler` class."""
        self.clear()

    async def _on_event(self, event, event_data):
        """Act on an event."""
        logger.debug("Event %s happened.", event)
        for callback in self.bindings[event]:
            await callback(event_data)
        for callback in self.bindings['*']:
            await callback(event, event_data)

    def bind(self, event, callback):
        """Bind a callback to an event."""
        if event not in self.EVENTS:
            raise ValueError(
                f"Cannot bind '{callback}' to event '{event}', "
                f"because that event is not known.")
        if callback not in self.bindings[event]:
            self.bindings[event].append(callback)

    def unbind(self, event, callback):
        """Remove a callback from an event."""
        try:
            index = self.bindings[event].index(callback)
        except KeyError:
            raise ValueError(
                f"No callback has been registered for the event '{event}'.")
        except ValueError:
            raise ValueError(
                f"Callback '{callback}' has not been registered "
                f"for the event '{event}'.")
        self.bindings[event].pop(index)

    def clear(self):
        """Remove all callbacks."""
        self.bindings = defaultdict(list)
