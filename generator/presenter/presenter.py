import random
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .config import Config
from format.markdown import Row, HeaderRow, Table
from lib.date import format_duration
from .types import PresentationKind


@dataclass(kw_only=True)
class Program:
    kind: PresentationKind
    title: str
    length: int
    start_time: datetime | None

    @property
    def end_time(self) -> datetime:
        if self.start_time is None:
            raise TypeError("start_time is not set")

        end_time = self.start_time + self.length
        return end_time

    def dict(self) -> dict:
        duration = format_duration(self.start_time, self.end_time)

        return {
            "kind": self.kind,
            "duration": duration,
            "title": self.title,
        }

    def to_row(self, column_order: list[str]) -> str:
        columns = self.dict()
        return Row(columns=columns, column_order=column_order)


@dataclass(kw_only=True)
class Presentation(Program):
    loginname: str
    kg: str
    page_path: str
    title: str = "自分の研究タイトル"
    start_time: datetime | None = None

    column_order = ["kind", "duration", "loginname", "kg", "title"]

    def dict(self):
        duration = format_duration(self.start_time, self.end_time)
        title = f"[{self.title}]({self.page_path})"

        return {
            "kind": self.kind.upper(),
            "duration": duration,
            "loginname": self.loginname,
            "kg": self.kg,
            "title": title,
        }

    @classmethod
    def header_row(cls):
        header = {
            "kind": "種別 / Kind",
            "duration": "発表時間 / Presentation time",
            "loginname": "ログイン名 / Login name",
            "kg": "KG",
            "title": "発表タイトル",
        }

        return HeaderRow(header, cls.column_order)


@dataclass(kw_only=True)
class BreakTime(Program):
    kind: Literal["break"]

    def dict(self) -> dict:
        out = super().dict()
        out["kind"] = "休憩 / Break"
        return out


class Timetable:
    programs: list[Program]

    column_order = ["kind", "duration", "loginname", "kg", "title"]

    def __init__(self, programs: list[Program]):
        self.programs = programs

    @classmethod
    def create(
        cls, presenters: list[Presentation], config: Config, randomize: bool = False
    ):
        if randomize:
            random.shuffle(presenters)

        programs = []
        present = config.start_time
        breaks = config.breaks.copy()
        next_break = breaks.pop(0)

        i = 0

        while i < len(presenters):
            presentation = presenters[i]
            next_end = present + presentation.length

            next_program = None

            # 次のプログラムが存在し、かつ休憩を取るのにいいタイミングであれば休憩を入れる
            if i + 1 < len(presenters) and next_break.is_good_to_toke(
                present, next_end
            ):
                title = next_break.title or ""
                length = next_break.length
                next_program = BreakTime(
                    kind="break", title=title, length=length, start_time=present
                )
                next_break = breaks.pop(0)

            else:
                presentation.start_time = present
                next_program = presentation
                i += 1

            programs.append(next_program)
            present += next_program.length

        return cls(programs)

    def to_table(self):
        header_row = Presentation.header_row()
        presenters = self.programs

        rows = []
        for presenter in presenters:
            row = presenter.to_row(self.column_order)
            rows.append(row)

        table = Table(header_row, rows)

        return table
