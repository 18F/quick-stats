"""Language statistics for a Github Org"""
from collections import Counter
import sys

from github import Github


def org_repo_langs(token, org_name):
    """Iterator of language stats per repo"""
    client = Github(token)
    for repo in client.get_organization(org_name).get_repos():
        stats = repo.get_languages()
        if stats:
            yield stats


def print_counter(counter, heading):
    """Pretty print stats from a counter"""
    total = sum(counter.values())
    print(heading)
    for language, count in counter.most_common(10):
        print("\t{}: {}/{} = {}".format(language, count, total, count/total))


def print_counters(lines, by_majority):
    print_counter(lines, "By line")
    print_counter(by_majority, "By majority")


def summarize_stats(stats):
    """Prints a summary of the org repo statistics"""
    lines, by_majority = Counter(), Counter()
    processed = 0
    for stat in stats:
        for lang, count in stat.items():
            lines[lang] += count
        majority = Counter(stat).most_common()[0][0]
        by_majority[majority] += 1
        processed += 1
        if processed % 10 == 0:
            print(processed)
            print_counters(lines, by_majority)

    print_counters(lines, by_majority)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python langstats.py TOKEN ORGNAME")
        print("Create a token at https://github.com/settings/tokens")
    else:
        stats = org_repo_langs(sys.argv[1], sys.argv[2])
        summarize_stats(stats)
