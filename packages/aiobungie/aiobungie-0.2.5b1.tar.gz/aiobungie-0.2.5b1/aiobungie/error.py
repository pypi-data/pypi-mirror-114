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

"""aiobungie Exceptions."""

from __future__ import annotations

__all__: Sequence[str] = [
    "PlayerNotFound",
    "HashError",
    "ActivityNotFound",
    "CharacterTypeError",
    "JsonError",
    "ClanNotFound",
    "CharacterNotFound",
    "NotFound",
    "HTTPException",
    "UserNotFound",
    "ComponentError",
]

from typing import Sequence, final


@final
class PlayerNotFound(Exception):
    """Raised when a `aiobungie.objects.Player` is not found."""


@final
class HashError(Exception):
    """Raised when `aiobungie.objects.Activity.hash` used for modes that are not raids."""


@final
class ActivityNotFound(Exception):
    """Raised when a `aiobungie.objects.Activity` not found."""


@final
class CharacterTypeError(Exception):
    """Raised on a character type error."""


@final
class JsonError(Exception):
    """Raised when an HTTP request did not return a json response."""


@final
class CharacterNotFound(Exception):
    """Raised when a `aiobungie.objects.Character` not found."""


@final
class HTTPException(Exception):
    """Exception for handling `aiobungie.http.HTTPClient` requests errors."""


@final
class ClanNotFound(Exception):
    """Raised when a `aiobungie.objects.Clan` not found."""


@final
class NotFound(Exception):
    """Raised when an unknown request was not found."""


@final
class UserNotFound(Exception):
    """Raised when a `aiobungie.objects.User` not found."""


@final
class ComponentError(Exception):
    """Raised when someone uses the wrong `aiobungie.internal.enums.Component.`"""
