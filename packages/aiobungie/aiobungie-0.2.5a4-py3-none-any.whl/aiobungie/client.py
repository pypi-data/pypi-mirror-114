# MIT License
#
# Copyright (c) 2020 - Present nxtlo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""The base aiobungie Client that your should inherit from / use."""


from __future__ import annotations

__all__: Sequence[str] = [
    "Client",
]

import asyncio
from typing import TYPE_CHECKING, Any, Coroutine, Optional, Sequence, Union

from . import error, objects
from .http import HTTPClient
from .internal import Manifest, deprecated
from .internal.enums import Class, Component, GameMode, MembershipType, Vendor


class Client:
    """Represents a client that connects to the Bungie API

    Attributes
    -----------
    key: `builtins.str`
        Your Bungie's API key or Token from the developer's portal.
    loop: `asyncio.AbstractEventLoop`
        asyncio event loop.
    """

    __slots__: Sequence[str] = ("key", "loop", "http")

    key: str
    """You Bungie API Key"""

    loop: asyncio.AbstractEventLoop
    """An optional asyncio loop, Default is None."""

    http: HTTPClient
    """The http client connector to make the request."""

    def __init__(self, key: str, *, loop: asyncio.AbstractEventLoop = None) -> None:
        self.loop: asyncio.AbstractEventLoop = (
            asyncio.get_event_loop() if not loop else loop
        )
        self.key: str = key

        if not self.key:
            raise ValueError("Missing the API key!")
        self.http: HTTPClient = HTTPClient(key=key)
        super().__init__()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def run(self, future: Coroutine[Any, None, None]) -> None:
        """Runs a Coro function until its complete.
        This is equivalent to asyncio.get_event_loop().run_until_complete(...)

        Parameters
        ----------
        future: `typing.Coroutine[typing.Any, typing.Any, typing.Any]`
            Your coro function.

        Example
        -------
        ```py
        async def main() -> None:
            player = await client.fetch_player("Fate")
            print(player.name)

        client.run(main())
        ```
        """
        try:
            if not self.loop.is_running():
                self.loop.run_until_complete(future)
        except asyncio.CancelledError:
            raise

    async def from_path(self, path: str) -> Any:
        return await self.http.static_search(path)

    async def fetch_manifest(self) -> Optional[Manifest]:
        resp = await self.http.fetch_manifest()
        return Manifest(self.key, resp)

    async def fetch_user(self, name: str, *, position: int = 0) -> objects.User:
        """Fetches a Bungie user by their name.

        Parameters
        ----------
        name: `builtins.str`
            The user name.
        position: `builtins.int`
            The user position/index in the list to return,
            Will returns the first one if not specified.

        Raises
        ------
        `aiobungie.error.UserNotFound`
            The user wasa not found.
        """
        data = await self.http.fetch_user(name=name)
        return objects.User(data=data, position=position)

    async def fetch_user_from_id(self, id: int) -> objects.User:
        """Fetches a Bungie user by their id.

        Parameters
        ----------
        id: `builtins.int`
            The user id.
        position: `builtins.int`
            The user position/index in the list to return,
            Will returns the first one if not specified.

        Raises
        ------
        `aiobungie.error.UserNotFound`
            The user wasa not found.
        """
        payload = await self.http.fetch_user_from_id(id)
        return objects.User(data=payload)

    async def fetch_profile(
        self,
        memberid: int,
        type: MembershipType,
        /,
        component: Component,
        *,
        character: Optional[Class] = None,
    ) -> objects.Profile:
        data = await self.http.fetch_profile(memberid, type, component=component)
        return objects.Profile(data=data, component=component, character=character)

    async def fetch_player(
        self, name: str, type: MembershipType, *, position: int = None
    ) -> objects.Player:
        """Fetches a Destiny2 Player.

        Parameters
        -----------
        name: `builtins.str`
            The Player's Name
        type: `aiobungie.internal.enums.MembershipType`
            The player's membership type, e,g. XBOX, STEAM, PSN
        position: `builtins.int`
            Which player position to return, first player will return if None.

        Returns
        --------
        `aiobungie.objects.Player`
            a Destiny Player object
        """
        resp = await self.http.fetch_player(name, type)
        return objects.Player(data=resp, position=position)

    async def fetch_character(
        self, memberid: int, type: MembershipType, character: Class
    ) -> objects.Character:
        """Fetches a Destiny 2 character.

        Parameters
        ----------
        memberid: `builtins.int`
            A valid bungie member id.
        character: `aiobungie.internal.enums.Class`
            The Destiny character to retrieve.
        type: `aiobungie.internal.enums.MembershipType`
            The member's membership type.

        Returns
        -------
        `aiobungie.objects.Character`
            a Bungie character object.

        Raises
        ------
        `aiobungie.error.CharacterNotFound`
            raised if the Character was not found.
        """
        resp = await self.http.fetch_character(
            memberid=memberid, type=type, character=character
        )
        return objects.Character(char=character, data=resp)

    async def fetch_vendor_sales(
        self,
    ) -> Any:
        """Fetch vendor sales."""
        return await self.http.fetch_vendor_sales()

    @deprecated
    async def fetch_activity(
        self,
        userid: int,
        charid: int,
        mode: GameMode,
        memtype: MembershipType,
        *,
        page: Optional[int] = 1,
        limit: Optional[int] = 1,
    ) -> objects.Activity:
        """Fetches a Destiny 2 activity for the specified user id and character.

        Parameters
        ----------
        userid: `builtins.int`
            The user id that starts with `4611`.
        charaid: `builtins.int`
            The id of the character to retrieve.
        mode: `aiobungie.internal.enums.GameMode`
            This parameter filters the game mode, Nightfall, Strike, Iron Banner, etc.
        memtype: `aiobungie.internal.enums.MembershipType`
            The Member ship type, if nothing was passed than it will return all.
        page: typing.Optional[builtins.int]
            The page number
        limit: typing.Optional[builtins.int]
            Limit the returned result.

        Returns
        -------
        `aiobungie.objects.Activity`
            A bungie Activity object.

        Raises
        ------
        `AttributeError`
            Using `aiobungie.objects.Activity.hash` for non raid activies.
        `aiobungie.error.ActivityNotFound`
            Any other errors occures during the response.
        """
        resp = await self.http.fetch_activity(
            userid, charid, mode, memtype=memtype, page=page, limit=limit
        )
        try:
            return objects.Activity(data=resp)

        except AttributeError:
            raise error.HashError(
                ".hash method is only used for raids, please remove it and use .raw_hash() instead"
            )
        except TypeError:
            raise error.ActivityNotFound(
                "Error has been occurred during getting your data, maybe the page is out of index or not found?\n"
            )

    async def fetch_app(self, appid: int, /) -> objects.Application:
        """Fetches a Bungie Application.

        Parameters
        -----------
        appid: `builtins.int`
            The application id.

        Returns
        --------
        `aiobungie.objects.Application`
            a Bungie application object.
        """
        resp = await self.http.fetch_app(appid)
        return objects.Application(resp)

    async def fetch_clan_from_id(self, id: int, /) -> objects.Clan:
        """Fetches a Bungie Clan by its id.

        Parameters
        -----------
        id: `builtins.int`
            The clan id.

        Returns
        --------
        `aiobungie.objects.Clan`
            A Bungie clan object
        """
        resp = objects.Clan(data=(await self.http.fetch_clan_from_id(id)))
        return resp

    async def fetch_clan(self, name: str, /, type: int = 1) -> objects.Clan:
        """Fetches a Clan by its name and returns the first result.

        Parameters
        ----------
        name: `builtins.str`
            The clan name
        type `builtins.int`
            The group type, Default is one.

        Returns
        -------
        `aiobungie.objects.Clan`
            A bungie clan object.
        """
        resp = await self.http.fetch_clan(name, type)
        return objects.Clan(data=resp)
