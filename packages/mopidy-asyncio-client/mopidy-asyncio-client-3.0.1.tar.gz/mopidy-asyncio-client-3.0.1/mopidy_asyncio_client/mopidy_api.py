"""Mopidy's core API.

https://docs.mopidy.com/en/latest/api/core/


Copyright (C) 2016,2017,2019  Ismael Asensio (ismailof@github.com)
Copyright (C) 2020  Jörg (https://github.com/joergrs
Copyright (C) 2021  svinerus (svinerus@gmail.com)
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


#
# _BaseController
#

class _BaseController:
    """Base class for all controllers."""

    def __init__(self, request_handler):
        """Initialize the `_BaseController` class.

        Parameters
        ----------
        request_handler : callable
            The function, which should be called to handle the request.

        Returns
        -------
        None.

        """

        self._request_handler = request_handler

    async def mopidy_request(self, request, **kwargs):
        """Handle the request to Mopidy.

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
        return await self._request_handler(request, **kwargs)


#
# CoreController
#

class CoreController(_BaseController):

    async def get_uri_schemes(self, **options):
        """Get list of URI schemes we can handle"""
        return await self.mopidy_request(
            'core.get_uri_schemes',
            **options)

    async def get_version(self, **options):
        """Get version of the Mopidy core API"""
        return await self.mopidy_request(
            'core.get_version',
            **options)

    async def describe(self, **options):
        """Get all endpoints"""
        return await self.mopidy_request(
            'core.describe',
            **options)


#
# TracklistController
#

class TracklistController(_BaseController):
    """Manages everything related to the list of tracks we will play."""

    #
    # Manipulating
    #

    async def add(self, tracks=None, at_position=None, uris=None, **options):
        """Add tracks to the tracklist.

        If `uris` is given instead of `tracks`, the URIs are looked up in the
        library and the resulting tracks are added to the tracklist.

        If `at_position` is given, the tracks are inserted at the given
        position in the tracklist. If `at_position` is not given, the tracks
        are appended to the end of the tracklist.

        Deprecation
        -----------
        Deprecated since Mopidy version 1.0:
            The 'tracks' argument, use 'uris'.

        Events
        ------
        Triggers the `mopidy.core.CoreListener.tracklist_changed()` event.

        Parameters
        ----------
        tracks : list of `mopidy.models.Track` | None, optional
            Tracks to add.
            The default is `None`.
        at_position : int|None, optional
            Position in tracklist to add tracks.
            The default is `None`.
        uris : list of str | None
            List of URIs for tracks to add.
            The default is `None`.

        Returns
        -------
        list of `mopidy.models.TlTrack`
            The new list of tracks.

        """
        if tracks is not None:
            raise DeprecationWarning(
                "Deprecated since Mopidy version 1.0: "
                "The 'tracks' argument, use 'uris'.")
        return await self.mopidy_request(
            'core.tracklist.add',
            tracks=tracks, at_position=at_position, uris=uris,
            **options)

    async def remove(self, criteria, **options):
        """Remove the matching tracks from the tracklist.

        Uses `filter()` to lookup the tracks to remove.

        Events
        ------
        Triggers the `mopidy.core.CoreListener.tracklist_changed()` event.

        Parameters
        ----------
        criteria : dict of (str, list) pairs
            One or more rules to match by.

        Returns
        -------
        list of `mopidy.models.TlTrack`
            List of tracks that were removed.

        """
        return await self.mopidy_request(
            'core.tracklist.remove',
            criteria=criteria,
            **options)

    async def clear(self, **options):
        """Clear the tracklist.

        Events
        ------
        Triggers the `mopidy.core.CoreListener.tracklist_changed()` event.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.tracklist.clear',
            **options)

    async def move(self, start, end, to_position, **options):
        """Move the tracks in the slice `[start:end]` to `to_position`.

        Events
        ------
        Triggers the `mopidy.core.CoreListener.tracklist_changed()` event.

        Parameters
        ----------
        start : int
            Position of first track to move'.
        end : int
            Position after last track to move.
        to_position : int
            New position for the tracks.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.tracklist.move',
            start=start, end=end, to_position=to_position,
            **options)

    async def shuffle(self, start=None, end=None, **options):
        """Shuffles the entire tracklist.

        If `start` and `end` is given only shuffles the slice `[start:end]`.

        Events
        ------
        Triggers the `mopidy.core.CoreListener.tracklist_changed()` event.

        Parameters
        ----------
        start : int|None, optional
            Position of first track to shuffle.
            The default is `None`.
        end : int|None, optional
            Position after last track to shuffle.
            The default is `None`.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.tracklist.shuffle',
            start=start, end=end,
            **options)

    #
    # Current state
    #

    async def get_tl_tracks(self, **options):
        """Get tracklist as list of `mopidy.models.TlTrack`.

        Returns
        -------
        list of `mopidy.models.TlTrack
            The tracklist.

        """
        return await self.mopidy_request(
            'core.tracklist.get_tl_tracks',
            **options)

    async def index(self, tl_track=None, tlid=None, **options):
        """The position of the given track in the tracklist.

        If neither 'tl_track' nor 'tlid' is given, we return the index of
        the currently playing track.

        Parameters
        ----------
        tl_track: `mopidy.models.TlTrack`|None
            The track to find the index of.
            The default is `None`.
        tlid : int|None
            TLID of the track to find the index of.
            The default is `None`.

        Returns
        -------
        int|None
            The position of the given track in the tracklist.

        """
        return await self.mopidy_request(
            'core.tracklist.index',
            tl_track=tl_track, tlid=tlid,
            **options)

    async def get_version(self, **options):
        """Get the tracklist version.

        Returns
        -------
        int
            Integer which is increased every time the tracklist is changed. Is
            not reset before Mopidy is restarted.

        """
        return await self.mopidy_request(
            'core.tracklist.get_version',
            **options)

    async def get_length(self, **options):
        """Get length of the tracklist.

        Returns
        -------
        int
            The length of the tracklist.

        """
        return await self.mopidy_request(
            'core.tracklist.get_length',
            **options)

    async def get_tracks(self, **options):
        """Get tracklist as list of `mopidy.models.Track`.

        Returns
        -------
        list of `mopidy.models.Track`
            A list of `mopidy.models.Track`

        """
        return await self.mopidy_request(
            'core.tracklist.get_tracks',
            **options)

    async def slice(self, start, end, **options):
        """Returns a slice of the tracklist.

        The slice is limited by the given start and end positions.

        Parameters
        ----------
        start : int
            Position of first track to include in slice.
        end : int
            Position after last track to include in slice

        Returns
        -------
        list of `mopidy.models.TlTrack`
            The requested slice of the tracklist.

        """
        return await self.mopidy_request(
            'core.tracklist.slice',
            start=start, end=end,
            **options)

    async def filter(self, criteria, **options):
        """Filter the tracklist by the given criteria.

        Each rule in the criteria consists of a model field and a list of
        values to compare it against. If the model field matches any of the
        values, it may be returned.

        Only tracks that match all the given criteria are returned.

        Examples::
            # Returns tracks with TLIDs 1, 2, 3, or 4 (tracklist ID)
            filter({'tlid': [1, 2, 3, 4]})

            # Returns track with URIs 'xyz' or 'abc'
            filter({'uri': ['xyz', 'abc']})

            # Returns track with a matching TLIDs (1, 3 or 6) and a
            # matching URI ('xyz' or 'abc')
            filter({'tlid': [1, 3, 6], 'uri': ['xyz', 'abc']})

        Parameters
        ----------
        criteria: dict of (string, list) pairs
            One or more rules to match by.

        Returns
        -------
        list of `mopidy.models.TlTrack`
            The filtered tracklist.

        """
        return await self.mopidy_request(
            'core.tracklist.filter',
            criteria=criteria,
            **options)

    #
    # Future state
    #

    async def get_eot_tlid(self, **options):
        """The TLID of the track that will be played after the current track.

        Not necessarily the same TLID as returned by `get_next_tlid()`.

        Returns
        -------
        int|None
            The TLID of the track, that will be played after the current track.

        """
        return await self.mopidy_request(
            'core.tracklist.get_eot_tlid',
            **options)

    async def get_next_tlid(self, **options):
        """The TLID of the track that will be played if calling
        `mopidy.core.PlaybackController.next()`.

        For normal playback this is the next track in the tracklist. If repeat
        is enabled the next track can loop around the tracklist. When random
        is enabled this should be a random track, all tracks should be played
        once before the tracklist repeats.

        Returns
        -------
        int|None
            The TLID of the next track.

        """
        return await self.mopidy_request(
            'core.tracklist.get_next_tlid',
            **options)

    async def get_previous_tlid(self, **options):
        """Returns the TLID of the track that will be played if calling
        `mopidy.core.PlaybackController.previous()`.

        For normal playback this is the previous track in the tracklist. If
        random and/or consume is enabled it should return the current track
        instead.

        Returns
        -------
        int|None
            The TLID of the previous track.

        """
        return await self.mopidy_request(
            'core.tracklist.get_previous_tlid',
            **options)

    async def eot_track(self, tl_track, **options):
        """The track that will be played after the given track.

        Not necessarily the same track as :meth:`next_track`.

        Deprecation
        -----------
        Deprecated since Mopidy version 3.0:
            Use 'get_eot_tlid()' instead.

        Parameters
        ----------
        tl_track: `mopidy.models.TlTrack`|None
            The reference track.

        Returns
        -------
        `mopidy.models.TlTrack`|None
            The next track.

        """
        raise DeprecationWarning(
            "Deprecated since Mopidy version 3.0: "
            "Use 'get_eot_tlid()' instead.")
        return await self.mopidy_request(
            'core.tracklist.eot_track',
            tl_track=tl_track,
            **options)

    async def next_track(self, tl_track, **options):
        """The track that will be played if calling
        `mopidy.core.PlaybackController.next()`.

        For normal playback this is the next track in the tracklist. If repeat
        is enabled the next track can loop around the tracklist. When random
        is enabled this should be a random track, all tracks should be played
        once before the tracklist repeats.

        Deprecation
        -----------
        Deprecated since Mopidy version 3.0:
            Use 'get_next_tlid()' instead.

        Parameters
        ----------
        tl_track : `mopidy.models.TlTrack`|None
            The reference track.

        Returns
        -------
        `mopidy.models.TlTrack`|None
            The next track.

        """
        raise DeprecationWarning(
            "Deprecated since Mopidy version 3.0: "
            "Use 'get_next_tlid()' instead.")
        return await self.mopidy_request(
            'core.tracklist.next_track',
            tl_track=tl_track,
            **options)

    async def previous_track(self, tl_track, **options):
        """Returns the track that will be played if calling
        `mopidy.core.PlaybackController.previous()`.

        For normal playback this is the previous track in the tracklist. If
        random and/or consume is enabled it should return the current track
        instead.

        Deprecation
        -----------
        Deprecated since Mopidy version 3.0:
            Use 'get_previous_tlid()' instead.

        Parameters
        ----------
        tl_track : `mopidy.models.TlTrack`|None
            The reference track

        Returns
        -------
        `mopidy.models.TlTrack`|None
            The previous track.

        """
        raise DeprecationWarning(
            "Deprecated since Mopidy version 3.0: "
            "Use 'get_previous_tlid()' instead.")
        return await self.mopidy_request(
            'core.tracklist.previous_track',
            tl_track=tl_track,
            **options)

    #
    # Options
    #

    async def get_consume(self, **options):
        """Get consume mode.

        Returns
        -------
        bool
            `True`:
                Tracks are removed from the tracklist when they have been
                played.
            `False`:
                Tracks are not removed from the tracklist.

        """
        return await self.mopidy_request(
            'core.tracklist.get_consume',
            **options)

    async def set_consume(self, value, **options):
        """Set consume mode.

        Parameters
        ----------
        value : bool
            `True`:
                Tracks will be removed from the tracklist when they have been
                played.
            `False`:
                Tracks will not removed from the tracklist.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.tracklist.set_consume',
            value=value,
            **options)

    async def get_random(self, **options):
        """Get random mode.

        Returns
        -------
        bool
            `True`:
                Tracks will be selected at random from the tracklist.
            `False`:
                Tracks will be played in the order of the tracklist.

        """
        return await self.mopidy_request(
            'core.tracklist.get_random',
            **options)

    async def set_random(self, value, **options):
        """Set random mode.

        Parameters
        ----------
        value : bool
            `True`:
                Tracks will be selected at random from the tracklist.
            `False`:
                Tracks will be played in the order of the tracklist.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.tracklist.set_random',
            value=value,
            **options)

    async def get_repeat(self, **options):
        """Get repeat mode.

        Returns
        -------
        bool
            `True`:
                The tracklist will be played repeatedly.
            `False`:
                The tracklist will be played once.

        """
        return await self.mopidy_request(
            'core.tracklist.get_repeat',
            **options)

    async def set_repeat(self, value, **options):
        """Set repeat mode.

        To repeat a single track, set both `repeat` and `single`.

        Parameters
        ----------
        value : bool
            `True`:
                The tracklist is played repeatedly.
            `False`:
                The tracklist is played once.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.tracklist.set_repeat',
            value=value,
            **options)

    async def get_single(self, **options):
        """Get single mode.

        Returns
        -------
        bool
            `True`:
                Playback is stopped after current song, unless in `repeat`
                mode.
            `False`:
                Playback continues after current song.

        """
        return await self.mopidy_request(
            'core.tracklist.get_single',
            **options)

    async def set_single(self, value, **options):
        """Set single mode.

        Parameters
        ----------
        value : bool
            `True`:
                Playback is stopped after current song, unless in `repeat`
                mode.
            `False`:
                Playback continues after current song.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.tracklist.set_single',
            value=value,
            **options)


#
# PlaybackController
#

class PlaybackController(_BaseController):
    """Manages playback state and the current playing track."""

    #
    # Playback control
    #

    async def play(self, tl_track=None, tlid=None, **options):
        """Play the given track, or the currently active track.

        If the given 'tl_track' and 'tlid' is `None`, play the currently
        active track.

        Note that the track must already be in the tracklist.

        Deprecation
        -----------
        Deprecated since Mopidy version 3.0:
            The 'tl_track' argument. Use 'tlid' instead.

        Parameters
        ----------
        tl_track: ''mopidy.models.TlTrack`|None, optional
            Track to play.
            The default is `None`.
        tlid: int|None, optional
            The TLID of the track to play.
            The default is `None`.

        Returns
        -------
        None.

        """
        if tl_track is not None:
            raise DeprecationWarning(
                "Deprecated since Mopidy version 3.0: "
                "The 'tl_track' argument. Use 'tlid' instead.")
        return await self.mopidy_request(
            'core.playback.play',
            tl_track=tl_track, tlid=tlid,
            **options)

    async def next(self, **options):
        """Change to the next track.

        The current playback state will be kept. If it was playing, playing
        will continue. If it was paused, it will still be paused, etc.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.playback.next',
            **options)

    async def previous(self, **options):
        """Change to the previous track.

        The current playback state will be kept. If it was playing, playing
        will continue. If it was paused, it will still be paused, etc.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.playback.previous',
            **options)

    async def stop(self, **options):
        """Stop playing.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.playback.stop',
            **options)

    async def pause(self, **options):
        """Pause playback.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.playback.pause',
            **options)

    async def resume(self, **options):
        """If paused, resume playing the current track.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.playback.resume',
            **options)

    async def seek(self, time_position, **options):
        """Seeks to time position given in milliseconds.

        Parameters
        ----------
        time_position: int
            Time position in milliseconds.

        Returns
        -------
        bool
            `True` if successful, else `False`.

        """
        return await self.mopidy_request(
            'core.playback.seek',
            time_position=time_position,
            **options)

    #
    # Current track
    #

    async def get_current_tl_track(self, **options):
        """Get the currently playing or selected track.

        Returns
        -------
        `mopidy.models.TlTrack`|None
            The currently playing or selected track.

        """
        return await self.mopidy_request(
            'core.playback.get_current_tl_track',
            **options)

    async def get_current_track(self, **options):
        """Get the currently playing or selected track.

        Extracted from :`get_current_tl_track()` for convenience.

        Returns
        -------
        `mopidy.models.Track`|None
            The currently playing or selected track.

        """
        return await self.mopidy_request(
            'core.playback.get_current_track',
            **options)

    # BUG: Does not exist in API documentation, but in mopidy/core/playback.py
    async def get_current_tlid(self, **options):
        """Get the currently playing or selected TLID.

        Extracted from `get_current_tl_track()` for convenience.

        Returns
        -------
        int|None
            The TLID of the currently playing or selected track.

        """
        return await self.mopidy_request(
            'core.playback.get_current_tlid',
            **options)

    async def get_stream_title(self, **options):
        """Get the current stream title.

        Returns
        -------
        str|None
            The current stream title.

        """
        return await self.mopidy_request(
            'core.playback.get_stream_title',
            **options)

    async def get_time_position(self, **options):
        """Get time position in milliseconds.

        Returns
        -------
        int
            The positions in milliseconds.

        """
        return await self.mopidy_request(
            'core.playback.get_time_position',
            **options)

    #
    # Playback states
    #

    async def get_state(self, **options):
        """Get the playback state.

        Returns
        -------
        str
            `"stopped"`, `"playing"`, `"paused"`.

        """
        return await self.mopidy_request(
            'core.playback.get_state',
            **options)

    async def set_state(self, new_state, **options):
        """Set the playback state.

        Must be `PLAYING`, `PAUSED`, or `STOPPED`.

        Possible states and transitions:
        .. digraph:: state_transitions
            "STOPPED" -> "PLAYING" [ label="play" ]
            "STOPPED" -> "PAUSED" [ label="pause" ]
            "PLAYING" -> "STOPPED" [ label="stop" ]
            "PLAYING" -> "PAUSED" [ label="pause" ]
            "PLAYING" -> "PLAYING" [ label="play" ]
            "PAUSED" -> "PLAYING" [ label="resume" ]
            "PAUSED" -> "STOPPED" [ label="stop" ]

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.playback.set_state',
            new_state=new_state,
            **options)


#
# LibraryController
#

class LibraryController(_BaseController):
    """Manages the music library, e.g. searching and browsing for music."""

    async def browse(self, uri, **options):
        """Browse directories and tracks at the given `uri`.

        `uri` is a string which represents some directory belonging to a
        backend. To get the intial root directories for backends pass
        `None` as the URI.

        Returns a list of `mopidy.models.Ref` objects for the directories and
        tracks at the given `uri`.

        The `mopidy.models.Ref` objects representing tracks keep the track's
        original URI. A matching pair of objects can look like this:
            Track(uri='dummy:/foo.mp3', name='foo', artists=..., album=...)
            Ref.track(uri='dummy:/foo.mp3', name='foo')

        The `mopidy.models.Ref` objects representing directories have backend
        specific URIs. These are opaque values, so no one but the backend that
        created them should try and derive any meaning from them. The only
        valid exception to this is checking the scheme, as it is used to route
        browse requests to the correct backend.

        For example, the dummy library's `/bar` directory could be returned
        like this:
            Ref.directory(uri='dummy:directory:/bar', name='bar')

        Parameters
        ----------
        uri : str
            URI to browse.

        Returns
        -------
        list of `mopidy.models.Ref`
            A list of `mopidy.models.Ref`, which can be found at `uri`.

        """
        return await self.mopidy_request(
            'core.library.browse',
            uri=uri,
            **options)

    async def search(self, query, uris=None, exact=False, **options):
        """Search the library for tracks where `field` contains `values`.

        `field` can be one of `uri`, `track_name`, `album`, `artist`,
        `albumartist`, `composer`, `performer`, `track_no`, `genre`, `date`,
        `comment`, or `any`.

        If `uris` is given, the search is limited to results from within the
        URI roots. For example passing `uris=['file:']` will limit the search
        to the local backend.

        Examples:
            # Returns results matching 'a' in any backend
            search({'any': ['a']})

            # Returns results matching artist 'xyz' in any backend
            search({'artist': ['xyz']})

            # Returns results matching 'a' and 'b' and artist 'xyz' in any
            # backend
            search({'any': ['a', 'b'], 'artist': ['xyz']})

            # Returns results matching 'a' if within the given URI roots
            # "file:///media/music" and "spotify:"
            search({'any': ['a']}, uris=['file:///media/music', 'spotify:'])

            # Returns results matching artist 'xyz' and 'abc' in any backend
            search({'artist': ['xyz', 'abc']})

        Parameters
        ----------
        query : dict
            One or more queries to search for.
        uris : list of str|None, optional
            Zero or more URI roots to limit the search to.
            The default is `None`.
        exact : bool, optional
            If the search should use exact matching.
            The default is `False`.

        Returns
        -------
        list of `mopidy.models.SearchResult`
            A list with the search result.

        """
        return await self.mopidy_request(
            'core.library.search',
            query=query, uris=uris, exact=exact,
            **options)

    async def lookup(self, uris, **options):
        """Lookup the given URIs.

        If the URI expands to multiple tracks, the returned list will contain
        them all.

        Parameters
        ----------

        uris : list of str
            Track URIs.

        Returns
        -------
        {uri: list of `mopidy.models.Track`}
            Dictionary with the lookuped uris.

        """
        return await self.mopidy_request(
            'core.library.lookup',
            uris=uris,
            **options)

    async def refresh(self, uri=None, **options):
        """Refresh library.

        Limit to URI and below if an URI is given.

        Parameters
        ----------
        uri : str
            Directory or track URI.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.library.refresh',
            uri=uri,
            **options)

    async def get_images(self, uris, **options):
        """Lookup the images for the given URIs.

        Backends can use this to return image URIs for any URI they know about
        be it tracks, albums, playlists. The lookup result is a dictionary
        mapping the provided URIs to lists of images.

        Unknown URIs or URIs the corresponding backend couldn't find anything
        for will simply return an empty list for that URI.

        Parameters
        ----------
        uris : list of str
            List of URIs to find images for.

        Returns
        -------
        {uri: tuple of `mopidy.models.Image`}
            Dictionary with lookuped images.

        """
        return await self.mopidy_request(
            'core.library.get_images',
            uris=uris,
            **options)

    async def get_distinct(self, field, query=None, **options):
        """List distinct values for a given field from the library.

        This has mainly been added to support the list commands the MPD
        protocol supports in a more sane fashion. Other frontends are not
        recommended to use this method.

        Parameters
        ----------
        field : str
            One of `"track"`, `"artist"`, `"albumartist"`, `"album"`,
            `"composer"`, `"performer"`, `"date"` or `"genre"`.
        query : dict
            Query to use for limiting results, see `.search()` for details
            about the query format.

        Returns
        -------
        set of values corresponding to the requested field type
            A set with the distinct values for the given field.

        """
        return await self.mopidy_request(
            'core.library.get_distinct',
            field=field, query=query,
            **options)


#
# PlaylistsController
#

class PlaylistsController(_BaseController):
    """Manages stored playlists."""

    async def get_uri_schemes(self, **options):
        """Get the list of URI schemes that support playlists.

        Returns
        -------
        list of str
            The list of URI schemes, which support playlists.

        """
        return await self.mopidy_request(
            'core.playlists.get_uri_schemes',
            **options)

    #
    # Fetching
    #

    async def as_list(self, **options):
        """Get a list of the currently available playlists.

        Returns a list of `mopidy.models.Ref` objects referring to the
        playlists. In other words, no information about the playlists' content
        is given.

        Returns
        -------
        list of `mopidy.models.Ref`
            The list of available playlists.

        """
        return await self.mopidy_request(
            'core.playlists.as_list',
            **options)

    async def get_items(self, uri, **options):
        """Get the items in a playlist specified by `uri`.

        Returns a list of `mopidy.models.Ref` objects referring to the
        playlist's items.

        If a playlist with the given `uri` doesn't exist, it returns `None`.

        Returns
        -------
        list of `mopidy.models.Ref` | None
            A list of items in the playlist.

        """
        return await self.mopidy_request(
            'core.playlists.get_items',
            uri=uri,
            **options)

    async def lookup(self, uri, **options):
        """Lookup playlist with given URI.

        Lookup playlist in both the set of playlists and in any other playlist
        sources. Returns `None` if not found.

        Parameters
        ----------
        uri : str
            The playlist URI.

        Returns
        -------
        `mopidy.models.Playlist` | None
            The playlist.

        """
        return await self.mopidy_request(
            'core.playlists.lookup',
            uri=uri,
            **options)

    async def refresh(self, uri_scheme=None, **options):
        """Refresh the playlists in `playlists`.

        If `uri_scheme` is `None`, all backends are asked to refresh. If
        `uri_scheme` is an URI scheme handled by a backend, only that backend
        is asked to refresh. If `uri_scheme` doesn't match any current
        backend, nothing happens.

        Parameters
        ----------
        uri_scheme : str, optional
            Limit to the backend matching the URI scheme.
            The default is `None`.

        Returns
        -------
        None.

        """
        return await self.mopidy_request(
            'core.playlists.refresh',
            uri_scheme=uri_scheme,
            **options)

    #
    # Manipulating
    #

    async def create(self, name, uri_scheme=None, **options):
        """Create a new playlist.

        If `uri_scheme` matches an URI scheme handled by a current backend,
        that backend is asked to create the playlist. If `uri_scheme` is
        `None` or doesn't match a current backend, the first backend is asked
        to create the playlist.

        All new playlists must be created by calling this method, and not by
        creating new instances of `mopidy.models.Playlist`.

        Parameters
        ----------
        name : str
            Name of the new playlist.
        uri_scheme : str, optional
            Use the backend matching the URI scheme.
            The default is `None`.

        Returns
        -------
        `mopidy.models.Playlist`|None
            The new playlist.

        """
        return await self.mopidy_request(
            'core.playlists.create',
            name=name, uri_scheme=uri_scheme,
            **options)

    async def save(self, playlist, **options):
        """Save the playlist.

        For a playlist to be saveable, it must have the `uri` attribute set.
        You must not set the `uri` atribute yourself, but use playlist objects
        returned by :meth:`create` or retrieved from :attr:`playlists`, which
        will always give you saveable playlists.

        The method returns the saved playlist. The return playlist may differ
        from the saved playlist. E.g. if the playlist name was changed, the
        returned playlist may have a different URI. The caller of this method
        must throw away the playlist sent to this method, and use the returned
        playlist instead.

        If the playlist's URI isn't set or doesn't match the URI scheme of a
        current backend, nothing is done and `None` is returned.

        Parameters
        ----------
        playlist : `mopidy.models.Playlist`
            The playlist to be saved.

        Returns
        -------
        `mopidy.models.Playlist`|None
            The saved playlist.

        """
        return await self.mopidy_request(
            'core.playlists.save',
            playlist=playlist,
            **options)

    async def delete(self, uri, **options):
        """Delete playlist identified by the URI.

        If the URI doesn't match the URI schemes handled by the current
        backends, nothing happens.

        Parameters
        ----------
        uri: str
            URI of the playlist to delete.

        Returns
        -------
        bool
            `True` if deleted, `False` otherwise.

        """
        return await self.mopidy_request(
            'core.playlists.delete',
            uri=uri,
            **options)


#
# MixerController
#

class MixerController(_BaseController):
    """Manages volume and muting."""

    async def get_mute(self, **options):
        """Get mute state.

        Returns
        -------
        bool|None
            `True` if muted, `False` unmuted, `None` if unknown.

        """
        return await self.mopidy_request(
            'core.mixer.get_mute',
            **options)

    async def get_volume(self, **options):
        """Get the volume.

        The volume scale is linear.

        Returns
        -------
        int in range [0..100] | None
            The volume or `None` if unknown.

        """
        return await self.mopidy_request(
            'core.mixer.get_volume',
            **options)

    async def set_mute(self, mute, **options):
        """Set mute state.

        Parameters
        ----------
        mute : bool
            `True` to mute, `False` to unmute.

        Returns
        -------
        bool
            `True` if call is successful, otherwise `False`.

        """
        return await self.mopidy_request(
            'core.mixer.set_mute',
            mute=mute,
            **options)

    async def set_volume(self, volume, **options):
        """Set the volume.

        The volume scale is linear.

        Parameters
        ----------
        volume : int in range [0..100]
            The volume.

        Returns
        -------
        bool
            `True` if call is successful, otherwise `False`.

        """
        return await self.mopidy_request(
            'core.mixer.set_volume',
            volume=volume,
            **options)


#
# HistoryController
#

class HistoryController(_BaseController):
    """Keeps record of what tracks have been played."""

    async def get_history(self, **options):
        """Get the track history.

        The timestamps are milliseconds since epoch.

        Returns
        -------
        list of (timestamp, `mopidy.models.Ref`) tuples
            The track history.

        """
        return await self.mopidy_request(
            'core.history.get_history',
            **options)

    async def get_length(self, **options):
        """Get the number of tracks in the history.

        Returns
        -------
        int
            The history length.

        """
        return await self.mopidy_request(
            'core.history.get_length',
            **options)
