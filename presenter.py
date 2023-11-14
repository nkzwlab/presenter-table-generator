from dataclasses import dataclass
from typing import Literal

from .markdown import Row, HeaderRow


@dataclass
class Presenter:
    loginname: str
    kg: str
    title: str = "自分の研究タイトル"
    kind: Literal["wip", "term"]

    column_order = ["kind", "loginname", "kg", "title"]

    def dict(self):
        return self.__dict__

    def to_row(self):
        return Row(columns=self.dict(), column_order=self.column_order)

    @staticmethod
    def header_row(cls):
        return HeaderRow(cls.column_order)
