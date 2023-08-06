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

"""Character entities related to Bungie Characters."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, TypedDict

from ..internal import Image
from ..internal.enums import Class, Gender, MembershipType, Race, Stat


class CharacterData(TypedDict):
    membershipId: int
    membershipType: MembershipType
    characterId: int
    dateLastPlayed: datetime
    minutesPlayedTotal: int
    light: int
    stats: Stat
    raceType: Race
    classType: Class
    genderType: Gender
    emblemPath: Image
    emblemBackgroundPath: Image
    emblemHash: int
    baseCharacterLevel: int
    titleRecordHash: Optional[int]


class CharacterImpl(CharacterData, total=False):
    pass
