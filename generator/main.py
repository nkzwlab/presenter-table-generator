import sys

from presenter.yaml import from_yaml

if __name__ == "__main__":
    filename = sys.argv[1]
    presenters = from_yaml(filename, randomize=True)
    table = presenters.to_table()

    print(table)
