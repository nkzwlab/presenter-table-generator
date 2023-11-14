from dataclasses import dataclass
from typing import Literal

from format.markdown import Row, HeaderRow

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
