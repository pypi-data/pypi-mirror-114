# This file is not exposed to customer in UI
import time
from typing import Generic, Optional, TypeVar

import attr


class Payload:
    """Base class for module-specific payload."""


P = TypeVar("P", bound=Payload)


@attr.s()
class Event(Generic[P]):
    """Base event for all other Levo events."""

    # Whether the given event should be the last one in a stream.
    is_terminal = False
    # Shortcut to convert events to dictionaries
    asdict = attr.asdict
    payload: Optional[P] = attr.ib(kw_only=True, default=None)


@attr.s(slots=True)
class Initialized(Event, Generic[P]):
    """Denotes the beginning of some process."""

    start_time: float = attr.ib(factory=time.monotonic)


@attr.s(slots=True)
class BeforeTestCaseExecution(Event, Generic[P]):
    """Just before a test case."""


@attr.s(slots=True)
class BeforeTestStepExecution(Event, Generic[P]):
    """Before each step inside a test case."""


@attr.s(slots=True)
class AfterTestStepExecution(Event, Generic[P]):
    """After each step in a test case."""


@attr.s(slots=True)
class AfterTestCaseExecution(Event, Generic[P]):
    """After a test case."""


@attr.s(slots=True)
class Interrupted(Event):
    """If execution was interrupted by Ctrl-C, or a received SIGTERM."""


@attr.s(slots=True)
class InternalError(Event):
    """An error happened during the process.

    Contains meta-information about the occured Python exception.
    """

    is_terminal = True

    message: str = attr.ib()
    exception_type: str = attr.ib()
    exception: Optional[str] = attr.ib(default=None)
    exception_with_traceback: Optional[str] = attr.ib(default=None)


@attr.s(slots=True)
class Finished(Event, Generic[P]):
    """The final event of the run.

    No more events after this point.
    """

    is_terminal = True

    # Total execution time
    running_time: float = attr.ib()
