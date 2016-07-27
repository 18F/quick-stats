"""Hours statistics from Tock exports"""
from collections import Counter
from csv import DictReader
import sys


def file_to_counter(filename):
    """Read CSV, convert it to a counter of hours by project"""
    counter = Counter()
    with open(filename) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            counter[row['Project']] += float(row['Number of Hours'])
    return counter


def merge_counters(counters):
    totals = Counter()
    for counter in counters:
        for key, value in counter.items():
            totals[key] += value
    return totals


def print_totals(totals):
    total = sum(totals.values())
    for project, amount in totals.most_common(20):
        print("{}: {}/{} = {}".format(project, amount, total, amount/total))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python tockstats.py FILE.csv [FILE2.csv ...]")
    else:
        counters = [file_to_counter(f) for f in sys.argv[1:]]
        print_totals(merge_counters(counters))
