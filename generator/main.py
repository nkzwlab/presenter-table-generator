import sys

from presenter.yaml import from_yaml

if __name__ == "__main__":
    filename = sys.argv[1]
    presenters = from_yaml(filename)
    table = presenters.to_table(randomize=True)

    print(table)
