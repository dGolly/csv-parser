import argparse
import csv
from tabulate import tabulate
from utils import filter_data, aggregate_data, parse_cond


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--where')
    parser.add_argument('--aggregate')

    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if args.where:
        data = filter_data(data, args.where)

    if args.aggregate:
        result = aggregate_data(data, args.aggregate)
        col, _, op = parse_cond(args.aggregate, {'=': None})
        headers = [f"{op}({col})"]
        print(tabulate([[result]], headers=headers, tablefmt='grid'))
    else:
        if data:
            headers = data[0].keys()
            rows = [list(row.values()) for row in data]
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        else:
            print("Нечего отображать!")


if __name__ == '__main__':
    main()
