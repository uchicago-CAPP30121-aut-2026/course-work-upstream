"""
Drawing Treemaps for FDIC data.

IMPORTANT: You do not need to understand how this code works to use the
Deposit Tree class.

usage: fdic.py [-h] [-i INPUT_FILENAME] [-o OUTPUT_FILENAME]

options:
  -h, --help            show this help message and exit
  -i, --input_filename INPUT_FILENAME
                        input filename
  -o, --output_filename OUTPUT_FILENAME
                        output filename

Sample uses:

  $ uv run fdic.py -i data/CPA.csv

  $ uv run fdic.py -i data/CPA.csv -o cpa.png
"""

#####################################
# DO NOT MODIFY THE CODE IN THIS FILE
#####################################

import argparse
import sys
import csv
import treenode

# get the student's code from the current directory
sys.path.insert(0, ".")
import treemap

ROOT = -1
STATE = 0
COUNTY = 1
CITY = 2
CLASS = 3
BRANCH = 4

LOW_LEVEL = CLASS

INSTITUTION_NAME_FIELD = 0
COUNTY_FIELD = 1
STATE_FIELD = 2
DEPOSITS_FIELD = 3
CITY_FIELD = 4
BRANCH_NAME_FIELD = 6
CLASS_FIELD = 7


def translate_level_to_key(fields, level):
    """
    given level of node in Deposit_Tree,
    get the attribute of this branch that should
    label the node at this level
    """
    if level == 0:
        return fields[STATE_FIELD]
    elif level == 1:
        return fields[COUNTY_FIELD]
    elif level == 2:
        return fields[CITY_FIELD]
    elif level == 3:
        return fields[CLASS_FIELD]
    elif level == 4:
        return fields[BRANCH_NAME_FIELD]
    else:
        print("Levels of hierarchy for branches only go up to 4")
        sys.exit(0)


def add(t, fields, level):
    """
    add branch b to tree t
    """

    kids = t.get_children_as_dict()
    key = translate_level_to_key(fields, level + 1)
    if level == LOW_LEVEL:
        code = fields[CLASS_FIELD]
        label = fields[BRANCH_NAME_FIELD]
        kids[key] = treenode.TreeNode(code, label, int(fields[DEPOSITS_FIELD]))
    else:
        if key not in kids:
            t = treenode.TreeNode("", key, 0)
            kids[key] = t
        t = kids[key]
        add(t, fields, level + 1)


def load_from_file(filename):
    """
    create a new dposit tree from given file filename
    """
    t = treenode.TreeNode("", "", 0)
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        for fields in reader:
            add(t, fields, 0)

    return t


def parse_args(args):
    """
    Parse the arguments
    """
    parser = argparse.ArgumentParser(description="Drawing treemaps.")
    parser.add_argument(
        "-i",
        "--input_filename",
        nargs=1,
        help="input filename",
        type=str,
        default=["data/CPA.csv"],
    )
    parser.add_argument(
        "-o",
        "--output_filename",
        nargs=1,
        help="output filename",
        type=str,
        default=[None],
    )

    try:
        return parser.parse_args(args[1:])
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parse_args(sys.argv)
        t = load_from_file(args.input_filename[0])
        treemap.draw_treemap(t, output_filename=args.output_filename[0])
    else:
        print("doing nothing besides loading the code...")
