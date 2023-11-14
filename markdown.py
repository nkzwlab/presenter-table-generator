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
        else:
            # Validate if the all columns actually exists in dict
            for column in column_order:
                if column not in self.columns:
                    raise KeyError(f"Column {column} does not exist in dict")

        row_str = ""

        for column in column_order:
            value = self.columns[column]
            row_str += f"| {value} "

        row_str += "|"

        return row_str


class HeaderRow(Row):
    def __init__(self, column_names: list[str]):
        self.columns = {column: column.capitalize() for column in column_names}

        self.column_order = column_names


class Table:
    header_row: HeaderRow
    rows: list[Row]

    def __init__(self, header_row: HeaderRow, rows: list[Row] | None = None):
        self.header_row = header_row

        if rows is None:
            self.rows = []
        else:
            self.rows = rows
