import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cmp_to_key
from typing import Literal

from .config import Config, Break as ConfigBreak
from format.markdown import Row, HeaderRow, Table
from lib.date import format_duration
from .time import good_to_toke
from .types import PresentationKind


@dataclass(kw_only=True)
class Program:
    kind: PresentationKind
    title: str
    length: timedelta
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
class FixedProgram(Program):
    after: datetime | None = None
    before: datetime | None = None

    def __post_init__(self):
        if self.after is None and self.before is None:
            raise TypeError("FixedProgram: EIther after or before must be specified")

    def is_good_to_toke(self, present: datetime, next_end: datetime) -> bool:
        return good_to_toke(present, next_end, after=self.after, before=self.before)


@dataclass(kw_only=True)
class Presentation(Program):
    loginname: str
    kg: str
    page_path: str
    title: str = "自分の研究タイトル"
    start_time: datetime | None = None

    column_order = ["kind", "duration", "loginname", "kg", "title"]

    def __post_init__(self):
        if self.title is None:
            self.title = "自分の研究タイトル"

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
class FixedPresentation(FixedProgram, Presentation):
    start_time: datetime | None = None


@dataclass(kw_only=True)
class BreakTime(FixedProgram):
    kind: Literal["break"]

    @staticmethod
    def from_config_break(b: ConfigBreak) -> "BreakTime":
        return BreakTime(
            kind="break",
            title=b.title,
            length=b.length,
            start_time=None,
            after=b.after,
            before=b.before,
        )

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
        a = len(presenters)
        print(presenters)
        fixed_presentations = pop_fixed_presenters(presenters)
        print(presenters)
        b = len(presenters)
        print(a, b)
        break_programs = map(lambda b: BreakTime.from_config_break(b), config.breaks)

        fixed_programs = fixed_presentations + list(break_programs)
        fixed_programs.sort(key=cmp_to_key(compare_fixed_program))
        print(fixed_programs)

        if randomize:
            random.shuffle(presenters)

        programs = []
        present = config.start_time
        i = 0
        next_fixed_program = fixed_programs.pop(0)

        while i < len(presenters):
            presentation = presenters[i]
            next_end = present + presentation.length

            next_program = None
            print(i, next_fixed_program)
            # print(presenters)

            # 次のプログラムが存在し、かつ休憩を取るのにいいタイミングであれば休憩を入れる
            if i + 1 < len(presenters) and next_fixed_program.is_good_to_toke(
                present, next_end
            ):
                next_fixed_program.start_time = present
                next_fixed_program.title = next_fixed_program.title or ""
                next_program = next_fixed_program

                next_fixed_program = fixed_programs.pop(0)

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


def pop_fixed_presenters(presenters: list[Presentation]) -> list[FixedPresentation]:
    fixed_presenters = []

    # 要素を取り除くために pop を使いたいので、 reversed で後ろからループする
    for i, presenter in enumerate(reversed(presenters)):
        idx = len(presenters) - 1 - i
        if isinstance(presenter, FixedProgram):
            print(f"popped presenter {idx} = {presenter}")
            presenters.pop(idx)
            fixed_presenters.append(presenter)

    return fixed_presenters


def compare_fixed_program(a: FixedProgram, b: FixedProgram) -> int:
    def cmp(c, d):
        # どっちか未指定の場合は指定のある方を優先する
        if c is None:
            return 1
        elif d is None:
            return -1

        if c < d:
            return -1
        elif c == d:
            return 0
        elif c > d:
            return 1

    # 全く時間が被らない場合は無条件に前後を決定する
    if None not in [a.before, b.after] and a.before <= b.after:
        return -1
    if None not in [a.after, b.before] and a.after >= b.before:
        return 1

    zero = datetime.fromtimestamp(0)
    inf = datetime.fromtimestamp(2**32 - 1)

    a_must_start = a.before - a.length if a.before is not None else inf
    b_must_start = b.before - b.length if b.before is not None else inf

    # yaml.per_person で after には初期値 config.start_time を入れているが、念の為初期値 zero を入れておく
    a_ends_after = a.after + a.length if a.after is not None else zero
    b_ends_after = b.after + b.length if b.after is not None else zero

    # 一つ目の発表が始まらないといけない時間を二つ目の最短終了時刻が上回る場合、一つ目を優先する
    if a_must_start <= b_ends_after:
        return -1
    if b_must_start <= a_ends_after:
        return 1

    # より早く始められる方を優先する
    if a.after != b.after:
        return cmp(a.after, b.after)
    # より早く終わってほしい方を優先する
    # どっちか未指定の場合は指定のある方を優先する
    if a.before or b.before:
        return cmp(a.before, b.before)

    # あとはもうわからんので等しいことにしておく
    return 0
