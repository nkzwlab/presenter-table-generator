from dataclasses import dataclass
from datetime import datetime, timedelta

from .types import PresentationKind


class Break:
    before: datetime | None
    after: datetime | None
    length: timedelta
    title: str | None

    def __init__(
        self,
        length: timedelta,
        before: datetime | None = None,
        after: datetime | None = None,
        title: str | None = None,
    ):
        if before is None and after is None:
            raise TypeError("Either before or after must be specified")

        self.before = before
        self.after = after
        self.length = length
        self.title = title

    def is_good_to_toke(self, present: datetime, next_end: datetime) -> bool:
        good = True

        if self.after is not None:
            good = good and self.after < present

        if self.before is not None:
            good = good and present < self.before <= next_end

        return good

    @property
    def start(self) -> datetime:
        return self.after or self.before


def sort_breaks(breaks: list[Break]) -> list[Break]:
    def key(brek: Break):
        return brek.start

    new = sorted(breaks, key=key)
    return new


@dataclass
class Config:
    page_root: str | None
    start_time: datetime
    presentation_time: dict[str, timedelta] | timedelta
    breaks: list[Break] | None

    def __post_init__(self, **kwargs):
        breaks = kwargs.get("breaks")
        if breaks is not None:
            self.breaks = sort_breaks(breaks)

    def presentation_length(self, kind: PresentationKind | None = None) -> timedelta:
        if isinstance(self.presentation_time, dict):
            length = self.presentation_time.get(kind)
            if length is None:
                raise KeyError(f"Presentation length for {kind} is not set")

            return length
        elif isinstance(self.presentation_time, timedelta):
            return self.presentation_time
        else:
            raise TypeError("Presentation length is not set")
