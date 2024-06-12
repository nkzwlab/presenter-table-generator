import argparse

from presenter.yaml import from_yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate presenters timetable in Markdown"
    )
    parser.add_argument("file", help="YAML file to read from")
    parser.add_argument(
        "--no-randomize", help="Switch randomization or not", action="store_true"
    )
    args = parser.parse_args()

    filename = args.file
    randomize = not args.no_randomize

    presenters = from_yaml(filename, randomize=randomize)
    table = presenters.to_table()

    print(table)
