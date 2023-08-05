# mopidy-asyncio-client

Async Mopidy client using JSON/RPC Websocket interface.

`mopidy_async_client.MopidyClient()` generates a Python interface
which maps the [Mopidy core API](https://docs.mopidy.com/en/latest/api/core/)
methods and events. For the connection it uses the
[websocket_client](https://pypi.org/project/websocket-client/) package.
The major version of `mopidy-asyncio-client` follows the major
Mopidy version number, so `mopidy-asyncio-client v3.y.z` supports
API version 3.x.

By default, the client tries to connect for a couple of times, if the
websocket connection is lost (the default is 5 times). However this can be
configured and also set to try forever.

Callback functions can be bound to all events sent by Mopidy.

Forked from
- [mopidy-async-client](https://github.com/SvineruS/mopidy-async-client)
- [mopidy-json-client](https://github.com/ismailof/mopidy-json-client)


## Usage

`mopidy-asyncio-client` provides the main class `MopidyClient`,
which manages the connection to and communication with a remote (or local)
Mopidy server. Use the `bind()` method to subscribe to Mopidy events:

```python3
import asyncio
import logging

from mopidy_asyncio_client import MopidyClient


logging.basicConfig()
logging.getLogger('mopidy_asyncio_client').setLevel(logging.DEBUG)


async def playback_started_handler(data):
    """Callback function, called when the playback started."""
    print(data)


async def all_events_handler(event, data):
    """Callback function; catch-all function."""
    print(event, data)


async def main_context_manager():

    async with MopidyClient(host='some_ip') as mopidy:

        mopidy.bind('track_playback_started', playback_started_handler)
        mopidy.bind('*', all_events_handler)

        # Your program's logic:
        await mopidy.playback.play()
        while True:
            await asyncio.sleep(1)


async def main_plain():

    mopidy = await MopidyClient().connect()

    mopidy.bind('track_playback_started', playback_started_handler)
    mopidy.bind('*', all_events_handler)

    # Your program's logic:
    await mopidy.playback.play()
    while True:
        await asyncio.sleep(1)

    await mopidy.disconnect()  # close connection implicit


# Either ...
asyncio.run(main_context_manager())
# ... or
asyncio.run(main_plain())
```


### Parse results

You can specify `parse_results=True` as a parameter to `MopidyClient()` and
get Mopidy objects instead of JSON dictionaries returned. To get this to work,
you need to install `mopidy` locally, so that `mopidy.models` can be imported.

```python3
>>> async with MopidyClient() as mopidy:
...     res = await mopidy.tracklist.get_tracks()
...     print(res)

[{'__model__': 'Track',
  'uri': 'file:///home/xxx/Music/audio.ogg',
  'name': 'audio.ogg',
  'date': '2021-01-01',
  'length': 123456}]

>>> async with MopidyClient(parse_results=True) as mopidy:
...     res = await mopidy.tracklist.get_tracks()
...     print(res)

[Track(
    date='2021-01-01',
    length=123456,
    name='audio.ogg',
    uri='file:///home/xxx/Music/audio.ogg')]
```


## Installation

`pip install mopidy-asyncio-client`

and for upgrading an existing installation:

`pip install --upgrade mopidy-asyncio-client`


## Change from `mopidy-async-client` to `mopidy-asyncio-client`

Here are the most important changes to help you upgrading from
`mopidy-async-client`. A list with all changes can be found in
[CHANGES.md](file://CHANGES.md).

### Incompatible changes

If you upgrade from `mopidy-async-client`, please watch out for these
incompatible changes:
- The package name changed to `mopidy-asyncio-client`, so the import
  statements have to be updated.
- `mopidy-async-client.MopidyClient()` is called with a `url` parameter.
  This parameter is replaced by the new keyword arguments
  `hostname='localhost'` and `port=6680`. The uri is then built automatically.
- `mopidy-async-client.MopidyClient` has a `listener` property. This property
  was renamed to the (more appropriate) `eventhandler` property, but at the
  same time `MopidyClient` has gained the following three methods to deal with
  callback functions:
    - `bind()`
    - `unbind()`
    - `clear()`

  These have the same signatures as the old methods. To update simply replace
  `MopidyClient().listener.bind|unbind|clear` with
  `MopidyClient().bind|unbind|clear`.
- Deprecated method arguments or methods now raise a `DeprecationWarning`. The
  following functions are effected:
    - `TracklistController.add(tracks)`: Use the `uris` parameter.
    - `TracklistController.eot_track()`: Use the `get_eot_tlid()` method.
    - `TracklistController.next_track()`: Use the `get_next_tlid()` method.
    - `TracklistController.previous_track()`: Use the `get_previous_track()`
      method.
    - `PlaybackController.play(tl_track)`: Use the `tlid` parameter.
- `MopidyListener` was renamed to (the more appropriate) `MopidyEventHandler`.
  But since it is not exposed, you should not notice it.

### Important changes

- `MopidyClient()` now understands the `reconnect_attempts=None` keyword
  parameter; this results in infinite connection attempts.
- The major version number of `mopidy-asyncio-client` follows the major
  version number of Mopidy.

### Bugs fixed

- `MopidyListener.clear()` did not reset the `bindings` property to
  `collections.defaultdict(list)`, but to `{}`. Fixed.
- When `ResponseMessage` parsed a JSON/RPC message, it did not check, if
  the parameter `on_msg_result` (property `_on_result`) is set. Fixed.
- Use module `logger` instead of `logging` (3 stray occurrences) throughout.
- Downgrade timeout errors, if a request is not answered in time. (It used to
  log an exception.)

### License

The license was changed from
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) to
[GPLv3](http://www.gnu.org/licenses/gpl-3.0.html).


## Project resources

- PyPi: https://pypi.org/project/mopidy-asyncio-client/
- Source code: https://gitlab.com/sphh/mopidy-asyncio-client/
- Issue tracker: https://gitlab.com/sphh/mopidy-asyncio-client/-/issues/


## References

- [Mopidy Core API](https://mopidy.readthedocs.org/en/latest/api/core)
- [websocket_client](https://github.com/liris/websocket_client)
- [mopidy-json-client](https://github.com/ismailof/mopidy-json-client)
- [mopidy-async-client](https://github.com/SvineruS/mopidy-async-client)


## Copyright of this file

Copyright (C) 2016,2017  Ismael Asensio (ismailof@github.com)<br/>
Copyright (C) 2020  svinerus (svinerus@gmail.com)<br/>
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


#### Reasons for this fork

I needed unlimited connection attemps for
[mopidris](https://gitlab.com/sphh/mopidris), a gateway between the
[MPRIS D-Bus Interface Specification](https://specifications.freedesktop.org/mpris-spec/latest/)
and a remotely (or locally) running Mopidy instance. `mopidy-async-client` is
limited to a set number of connection attempts, after which it bails out, so I
made a [pull request](https://github.com/SvineruS/mopidy-async-client/pull/1)
against it, which uses a traditional `while:` loop to get infinite connection
attempts. Unfortunately this was declined by the author with the argument,
that a `while:` loop does not look nice and that he does not like `while:`
loops. Instead the [author](https://github.com/SvineruS) decided to set the
maximum number of attempts to `sys.maxsize`. True, this is as close to
infinite as we can get, but why has Guido given us a `while:` loop, if we
do not use it? (And frankly, this attitude reminds me remarkably to the
nonchalant approach leading to the infamous
[Y2K bug](https://en.wikipedia.org/wiki/Year_2000_problem).) BTW for this
approach the code needs not be changed, because it was already possible to
give a maximum number of attempts to connect.

Since there were other issues, I was not too happy with (see
[CHANGES.md](file://CHANGES.md)), I bit the bullet, took the plunge and forked
it. I am not too happy about it, because I believe that there are already too
many (dead) forks of modules with very similar functionality around. I would
be happy, if these two forks will be combined in the future.
