import sys

from format.markdown import Table
from presenter import yaml
from presenter.presenter import Presenter

if __name__ == "__main__":
    filename = sys.argv[1]
    presenters = yaml.from_yaml(filename)

    header_row = Presenter.header_row()

    rows = []
    for presenter in presenters:
        row = presenter.to_row()
        rows.append(row)

    table = Table(header_row, rows)
    print(table)
