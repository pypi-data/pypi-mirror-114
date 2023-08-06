from __future__ import annotations

import abc
import enum

from kupala.requests import Request


class AuthorizationError(Exception):
    """Base error class for all authorization related exceptions."""


class NotAuthorizedError(AuthorizationError):
    """Raised if an user cannot access the resource."""


class Voter(abc.ABC):
    """A voter is a class that decides if an access to the resource is authorized or not."""

    class Decision(enum.Enum):
        ACCESS_GRANTED = 1
        ACCESS_DENIED = 0
        ACCESS_ABSTAIN = -1

    def vote(self, request: Request) -> Voter.Decision:
        raise NotImplementedError()


class AccessChecker:
    """This class does access control checks using votes and returns a boolean value
    where True means that access is granted."""

    def can(self, request: Request, voters: list[Voter]) -> bool:
        pass
