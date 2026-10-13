"""
Schelling Model of Housing Segregation Assignment

Utility code for managing city grids and locations.
"""

import csv
import os
import sys

from functools import cmp_to_key

ALLOWED_VALUES = ("B", "M", "F")


def load_city_file(filename, allowed=ALLOWED_VALUES):
    """
    Read a city grid from a text file and return the corresponding
    in-memory representation.

    Args:
        filename: (str) the name of the city file to read

    Returns: (List[List[str]] | None) the city grid contained in the
      specified file or None, if the specified file does not exist
      or has the wrong format.
    """
    if not os.path.isfile(filename):
        print(f"Bad city file name: {filename}", file=sys.stderr)
        return None

    with open(filename) as f:
        city = []
        i = 0
        for line in f:
            row = [s.strip() for s in line.strip().split()]
            if i == 0 and len(row) == 1:
                # old format with N in the file
                continue
            if i == 0:
                N = len(row)
            if not check_row(N, row, i, allowed):
                print(
                    (
                        f"Format error in line {i}: row has an "
                        f"entry other than {'/'.join(allowed)}"
                    ),
                    file=sys.stderr,
                )
                return None
            city.append(row)
            i = i + 1

        if not city:
            print("File is empty", file=sys.stderr)
            return None

        return city


def find_homes_for_sale(city):
    """
    Find locations of the unoccupied homes in the city.

    Inputs:
        city (List[List[str]]): a city

    Returns (List[Tuple(int, int)]): a list with the unoccupied locations represented
    as pairs.
    """
    unoccupied_locations = []

    for i, row in enumerate(city):
        for j, home in enumerate(row):
            if home == "F":
                unoccupied_locations.append((i, j))

    return unoccupied_locations


def load_for_sale_file(filename):
    """
    Read a list of homes for sale from a text file and return the
    corresponding in-memory representation.

    Args:
        filename: (str) the name of file with a list of homes for sale.

    Returns: (List[Tuple[int, int]] | None): a list of homes for sale, in the order
      they appear in the file. Returns None if the specified file does not
      exist or has the wrong format.
    """
    if not os.path.isfile(filename):
        print(f"Bad homes-for-sale file name: {filename}", file=sys.stderr)
        return None

    with open(filename) as f:
        reader = csv.reader(f, delimiter=",")
        result = []
        i = 0
        for i, row in enumerate(reader):
            if i == 0 and len(row) == 1:
                # old format with N in the file
                continue

            if len(row) != 2:
                print(
                    f"Format error in line {i}: row has more/fewer than two values.",
                    file=sys.stderr,
                )
                return None
            row, col = row
            result.append((int(row), int(col)))
    return result


def print_city(city):
    """
    Print a text representation of a city.

    Inputs:
        city: (list of lists of strings)
    """
    for row in city:
        print(" ".join(row))


def check_row(N, row, line_num, allowed=ALLOWED_VALUES, print_error=True):
    """
    Check the format of a row.

    Args:
        N: (int) the expected length of the row
        row: (List[str]) a row from the file
        line_num: (int) the row's line number in the file

    Returns (bool): True if the row has the correct length
      and contains only allowed strings, False otherwise.
    """
    if len(row) != N:
        if print_error:
            print(
                f"Format error in line {line_num}: row is wrong length", file=sys.stderr
            )
        return False

    bad_vals = set(row) - set(allowed)
    if bad_vals != set():
        if print_error:
            print(
                (
                    "Format error in line {line_num}: invalid value included"
                    f" in the row: {bad_vals}"
                ),
                file=sys.stderr,
            )
        return False
    return True


def is_city(city):
    """
    Verify that city is a list of length N where each element is also
    a list of length N.  For smaller cities, check that the rows contain
    the allowed values.

    Inputs:
        city: (list of lists of strings)

    Returns (bool): True if the city argument contains a valid
      city, False otherwise.
    """
    max_small_city = 20

    if not isinstance(city, list):
        return False

    if not city:
        return False

    N = len(city)
    for idx, row in enumerate(city):
        if N <= max_small_city:
            # do full check for small cities
            if not check_row(N, row, idx):
                return False
        else:
            if not isinstance(row, list) or len(row) != N:
                return False
    return True


def find_mismatch(city0, city1):
    """
    Find the first location (in row-major order) where two N x N cities
    differ or None, if the cities are the same.

    Inputs:
        city0: (List[List[str]]): first city
        city1: (List[List[str]]): second city

    Returns (Tuple[int, int] | None): a location (int, int), if the
      cities different and None if they are the same.
    """
    assert is_city(city0), "City0 is not a valid city"

    assert is_city(city1), "City1 is not a valid city"

    assert len(city0) == len(city1), "Cities are not the same shape."

    assert len(city0[0]) == len(city1[0]), "Cities are not the same shape."

    for i, row in enumerate(city0):
        for j, home0 in enumerate(row):
            # strip unsatisfied indicator from values if necessary
            home0 = home0 if "U" not in home0 else home0[1]
            home1 = city1[i][j] if "U" not in city1[i][j] else city1[i][j][1]
            if home0 != home1:
                return (i, j)
    return None


def sort_locations_by_differential(locs, differentials, return_both=False):
    """
    Given a list of score locations and their corresponding
    differentials, generate a list of locations sorted in decreasing
    order by differential.  Locations are used to break ties:
    locations earlier in a row-major order traversal come earlier in
    the ordering.

    Args:
        locs (List[Tuple[int, int]]): the list of locations to sort
        differential (List[float]): the differentials for the
          corresponding locations
        return_both (bool):


    """

    def cmp_diff_and_loc(t1, t2):
        """
        Compare two differential-and-location tuples.

        Args:
            t1 (Tuple[float, Tuple[int, int]]): the first differential and loc tuple
            t2 (Tuple[float, Tuple[int, int]]): the second differential and loc tuple

        Returns (int): returns a value:
          - less than zero, if t1 comes before t2 in the ordering,
          - zero, if t1 and t2 are the same tuple, and
          - greater than zero, if t1 comes after t2 in the ordering

        """
        score1, loc1 = t1
        score2, loc2 = t2

        if score1 > score2:
            return -1
        elif score1 == score2:
            if loc1 < loc2:
                return -1
            elif loc1 == loc2:
                return 0
        return 1

    lst = zip(differentials, locs)
    sorted_lst = sorted(lst, key=cmp_to_key(cmp_diff_and_loc))
    sorted_locs = [loc for _, loc in sorted_lst]
    sorted_diffs = [diff for diff, _ in sorted_lst]

    if return_both:
        return sorted_locs, sorted_diffs
    else:
        return sorted_locs


def write_city_file(filename, city):
    f = open(filename, "w")
    for row in city:
        print(" ".join(row), file=f)
    f.close()


def write_for_sale_file(filename, for_sale):
    f = open(filename, "w")
    for loc in for_sale:
        print(",".join([str(x) for x in loc]), file=f)
    f.close()
