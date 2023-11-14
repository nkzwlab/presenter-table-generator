import sys

from presenter import yaml

if __name__ == "__main__":
    filename = sys.argv[1]
    presenters = yaml.from_yaml(filename)

    for presenter in presenters:
        row = presenter.to_row()
        print(row)
