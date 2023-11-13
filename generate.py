import argparse
import csv


CSV_FIELDNAMES = ["Name", "Group", "Title", "Type"]


class Presenters():
    def __init__(self, presenters: list[dict[str, str]]):
        self.presenters = presenters

    def generate_table(self) -> str:
        return self.presenters


def argument_parser():
    parser = argparse.ArgumentParser(
        description="Generate presenters table for MarkDown")

    parser.add_argument("input_file", help="input csv file")

    return parser


def main():
    # Parse arguments
    parser = argument_parser()
    args = parser.parse_args()

    # Parse input CSV File
    csv_file = args.input_file
    reader = None
    presenter_list = []

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f, )

        for row in reader:
            presenter_list.append(row)

    presenters = Presenters(presenter_list)

    markdown = presenters.generate_table()

    print(markdown)


if __name__ == "__main__":
    main()
