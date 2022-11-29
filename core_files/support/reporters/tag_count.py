import argparse
from pathlib import Path
import os
import glob
import ntpath
from prettytable import PrettyTable

AUTOMATED_TAG = '@Automation'
NOT_YET_AUTOMATED_TAG = '@Automation_TBD'
MANUAL_TAG = '@Manual'


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', help='Example: $ tag_count.py --f CoinInfo.feature | Insert the feature file.', required=False)
    parser.add_argument('--all', action='store_true', help='Example: True | Add this option IF you want to run the script for all feature files.')
    parser.set_defaults(all=False)
    args = parser.parse_args()
    feature_file = args.f
    all = args.all
    t = PrettyTable(['FEATURE FILE', 'AUTOMATED TESTS', 'NOT YET AUTOMATED', 'MANUAL TESTS'])
    if all:
        to_print = open_all(t)
    else:
        to_print = open_one(t, feature_file)

    if to_print:
        print(to_print.get_string(sortby='FEATURE FILE'))


def get_relative_path(path):
    root = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
    return os.path.join(root, path)


def get_config_filepath():
    return get_relative_path('features/')


def open_all(t: PrettyTable):
    for filename in glob.glob(get_config_filepath() + '*.feature'):
        with open(os.path.join(os.getcwd(), filename), 'r') as file:
            data = file.read()
            wordslist = list(data.split())
            manual = wordslist.count(MANUAL_TAG)
            automated = wordslist.count(AUTOMATED_TAG)
            todo = wordslist.count(NOT_YET_AUTOMATED_TAG)
            t.add_row([ntpath.basename(filename), automated, todo, manual])
    return t


def open_one(t: PrettyTable, filename):
    with open(os.path.join(get_config_filepath(), filename), 'r') as file:
        data = file.read()
        wordslist = list(data.split())
        manual = wordslist.count(MANUAL_TAG)
        automated = wordslist.count(AUTOMATED_TAG)
        todo = wordslist.count(NOT_YET_AUTOMATED_TAG)
        t.add_row([ntpath.basename(filename), automated, todo, manual])
    return t


if __name__ == '__main__':
    run()