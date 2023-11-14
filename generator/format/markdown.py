class Row:
    columns: dict[str, str]
    column_order: list[str] | None

    def __init__(self, columns: dict[str, str], column_order: list[str] | None):
        self.columns = columns
        self.column_order = column_order

    def __str__(self):
        column_order = self.column_order
        if column_order is None:
            column_order = self.columns.keys()

        row_str = ""

        for column in column_order:
            value = self.columns.get(column, "")
            row_str += f"| {value} "

        row_str += "|"

        return row_str


class HeaderRow(Row):
    def __init__(
        self, column_names: list[str] | dict[str, str], column_order: list[str] | None
    ):
        if isinstance(column_names, list):
            self.columns = {column: column.capitalize() for column in column_names}
            self.column_order = column_order or column_names

        elif isinstance(column_names, dict):
            self.columns = column_names
            self.column_order = column_order or column_names.keys()


class SeparatorRow(Row):
    def __init__(self, length: int):
        self.columns = {str(i): "---" for i in range(length)}
        self.column_order = [str(i) for i in range(length)]


class Table:
    header_row: HeaderRow
    separator_row: SeparatorRow
    rows: list[Row]

    def __init__(self, header_row: HeaderRow, rows: list[Row] | None = None):
        self.header_row = header_row
        self.separator_row = SeparatorRow(len(header_row.column_order))

        if rows is None:
            self.rows = []
        else:
            self.rows = rows

    def __str__(self):
        rows = [self.header_row, self.separator_row] + self.rows
        rows_str = [str(row) for row in rows]
        return "\n".join(rows_str)
