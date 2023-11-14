import random
from dataclasses import dataclass
from typing import Literal

from format.markdown import Row, HeaderRow, Table

PresentationKind = Literal["wip", "term"]


@dataclass
class Presenter:
    loginname: str
    kg: str
    kind: PresentationKind
    title: str = "自分の研究タイトル"

    column_order = ["kind", "loginname", "kg", "title"]

    def dict(self):
        return self.__dict__

    def to_row(self):
        return Row(columns=self.dict(), column_order=self.column_order)

    @classmethod
    def header_row(cls):
        header = {
            "kind": "種別 / Kind",
            "loginname": "ログイン名 / Login name",
            "kg": "KG",
            "title": "発表タイトル",
        }

        return HeaderRow(header, cls.column_order)


class Presenters:
    presenters: list[Presenter]

    def __init__(self, presenters: list[Presenter]):
        self.presenters = presenters

    def to_table(self, randomize=False):
        header_row = Presenter.header_row()
        presenters = self.presenters

        if randomize:
            presenters = self.presenters.copy()
            random.shuffle(presenters)

        rows = []
        for presenter in presenters:
            row = presenter.to_row()
            rows.append(row)

        table = Table(header_row, rows)

        return table
