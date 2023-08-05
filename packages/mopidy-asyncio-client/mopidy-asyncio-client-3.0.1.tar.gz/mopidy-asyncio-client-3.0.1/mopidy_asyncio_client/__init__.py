"""Async Mopidy Client via JSON/RPC Websocket interface.

Fork of https://github.com/ismailof/mopidy-json-client by ismailof
Fork of https://github.com/SvineruS/mopidy-async-client by svinerus


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

__author__ = 'Stephan Helma'
__credits__ = ['Ismael Asensio', 'Jörg RS', 'SvineruS']
__license__ = 'GPLv3+'
__version__ = '3.0.1'

from .client import MopidyClient
__all__ = ['MopidyClient']
