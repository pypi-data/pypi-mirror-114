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

"""Basic implementation for a Bungie a activity."""


from __future__ import annotations

__all__: Sequence[str] = ("Activity",)

from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence

from aiobungie.internal import time

from ..internal.enums import GameMode, MembershipType

if TYPE_CHECKING:
    from datetime import datetime

import abc

import attr

# NOTE: This is still being worked on.


@attr.s(hash=True, repr=True, slots=True, weakref_slot=False, eq=True, kw_only=True)
class PartialActivity(abc.ABC):
    """A partial interface for any bungie activity"""

    @property
    @abc.abstractmethod
    def is_completed(self) -> str:
        """Returns `Ok` if the activity is completed and 'No' if not."""

    @property
    @abc.abstractmethod
    def hash(self) -> int:
        """The activity's hash."""

    @property
    @abc.abstractmethod
    def mode(self) -> GameMode:
        """Activity's game mode."""

    @property
    @abc.abstractmethod
    def duration(self) -> str:
        """A string of The activity's duration, Example format `7m 42s`"""

    @property
    @abc.abstractmethod
    def players_count(self) -> int:
        """Character's total player count"""

    @property
    @abc.abstractmethod
    def when(self) -> Optional[datetime]:
        """A UTC datetime object of when was the activivy started."""

    @property
    @abc.abstractmethod
    def kills(self) -> int:
        """Activity's total kills."""

    @property
    @abc.abstractmethod
    def deaths(self) -> int:
        """Activity's total deaths."""

    @property
    @abc.abstractmethod
    def assists(self) -> int:
        """Activity's total assists."""

    @property
    @abc.abstractmethod
    def kd(self) -> int:
        """Activity's kill/death ration."""


@attr.s(hash=True, repr=True, slots=True, weakref_slot=False, eq=True, kw_only=True)
class Activity(PartialActivity):
    """Represents a Bungie Activity object.

    An activity can be one of `aiobungie.internal.enums.GameMode`.

    Attributes
    -----------
    mode: `aiobungie.internal.enums.GameMode`
            The activity mode or type.
    is_completed: `builtins.str`
            Check if the activity was completed or no.
    hash: `builtins.int`
            The activity's hash.
    duration: `builtins.str`
            A string of The activity's duration, Example format `7m 42s`
    kills: `builtins.int`
            Activity's Total kills
    deaths: `builtins.int`
            Activity's total deaths.
    assists: `builtins.int`
            Activity's Total assists
    kd: `builtins.int`
            Activity's kd ration.
    member_type: `aiobungie.internal.enums.MembershipType`
            The activity member's membership type.
    players_count: `builtins.int`
            Total players in the activity.
    when: typing.Optional[datetime.datetime]
            When did the activity occurred in UTC datetime.
    """

    is_completed: str = attr.ib(repr=True, hash=False, eq=False)

    hash: int = attr.ib(hash=True, repr=False, eq=False)

    mode: GameMode = attr.ib(hash=False, repr=True)

    kills: int = attr.ib(repr=False, eq=False, hash=False)

    deaths: int = attr.ib(repr=False, eq=False, hash=False)

    when: Optional[datetime] = attr.ib(repr=True, eq=False, hash=False)

    assists: int = attr.ib(repr=False, eq=False, hash=False)

    duration: str = attr.ib(repr=True, eq=False, hash=False)

    player_count: int = attr.ib(repr=False, eq=False, hash=False)

    member_type: MembershipType = attr.ib(repr=False, eq=False, hash=False)

    kd: int = attr.ib(repr=True, eq=False, hash=False)

    def as_dict(self) -> Dict[str, Any]:
        """Returns a dict object of the Activity,
        This function is useful if you're binding to other REST apis.
        """
        return dict(
            is_completed=self.is_completed,
            mode=self.mode,
            duration=self.duration,
            player_cout=self.player_count,
            when=time.Time.clean_date(str(self.when)),
            kills=self.kills,
            deaths=self.deaths,
            assists=self.assists,
            kd=self.kd,
            member_type=MembershipType(str(self.member_type)),
        )
