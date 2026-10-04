"""
Modeling Epidemics Assignment

This module contains a single function that generates test cities.
It is used by both the sir test code and the sir test generation
code.

Anne Rogers, April 2026
"""

import random
import sys


import sir
import sir_student

def mk_city(seed, num_people, pct_infected, pct_recovered, num_immunity_levels):
    """
    Generate a city.

    Args:
        seed (int | None): the seed to use for the random number generator
        num_people (int): the number of people to generate for the city
        pct_infected (int): the target percentage of infected people
        pct_recovered (int): the target percentage of recovered people
        num_immunity_levels (int): the number of different immunity levels
          to choose from when generating people.
    """
    assert num_people > 0
    assert pct_infected + pct_recovered <= 100
    assert num_immunity_levels > 0

    immunity_levels = [i/num_immunity_levels for i in range(1, num_immunity_levels + 1)]

    if seed is not None:
        # set the seed to allow for repeatablity.
        random.seed(seed)

    # construct the city
    city = []
    for i in range(num_people):
        r = random.uniform(0.0, 100.0)
        if r < pct_infected:
            ds = "I"
            nd = random.randint(0, sir_student.NUM_INFECTED_DAYS - 1)
            # choose from among the computed immumity levels,
            # excluding the last one
            il = random.choice(immunity_levels[:-1])
        elif r < pct_infected + pct_recovered:
            ds = "R"
            nd = random.randint(0, sir_student.NUM_RECOVERED_DAYS - 1)
            # choose from among the computed immumity levels
            il = random.choice(immunity_levels)
        else:
            ds = "S"
            # 10 is a randomly chosen number
            nd = random.randint(0, 10)
            # choose from among the computed immumity levels
            il = random.choice(immunity_levels)

        # choose a number of days using the computed upper bound.


        assert ds != "I" or nd < sir_student.NUM_INFECTED_DAYS
        # make the person and add them to the city
        city.append( (ds, nd, il) )

    return city


def parse_city_file(filename):
    """
    Read a city represented as person tuples from a file.

    Args:
        filename (string): the name of the file

    Returns (List[Tuple[str, int, float]]: City, or None if the file
        does not exist or cannot be parsed.
    """

    try:
        with open(filename) as f:
            residents = [line.split() for line in f]
    except IOError:
        print("Could not open:", filename, file=sys.stderr)
        return None

    ds_types = ('S', 'I', 'R')

    rv = []
    try:
        for i, res in enumerate(residents):
            ds, nd, imm_level = res

            num_days = int(nd)
            imm_level = float(imm_level)
            if (ds not in ds_types or num_days < 0 or
                not (0 <= imm_level <= 1.0)):
                raise ValueError()
            rv.append((ds, num_days, imm_level))
    except ValueError:
        emsg = ("Error in line {}: person tuples are represented\n"
                "with a disease state {}, a non-negative integer, and a\n"
                "value between 0.0 and 1.0 (inclusive).")
        print(emsg.format(i, ds_types), file=sys.stderr)
        return None
    return rv


def generate_city_str(city, tabs):
    """
    Given a city, generate a string with the contents of the
    city with one person per line.

    Args:
        fp (FilePointer): the output stream
        city (List[Tuple[str, int, float]]): the city to print
        tabs (str): a string a spaces to print at the start of each line

    Returns (str): a string for the city with one person per line.
    """
    s = "["
    longest_line = max([len(str(tuple(p))) for p in city])

    for i, person in enumerate(city):
        if i > 0:
            s += tabs
        s += str(tuple(person)) + ("," if i < len(city) - 1 else "]")
        num_spaces_to_add = (longest_line + 4 ) - len(str(tuple(person)))
        spaces_to_add = " " * num_spaces_to_add
        s += f"{spaces_to_add}# Loc {i}\n"
    return s

def print_city(fp, city, tabs):
    """
    Print the contents of a city with each location on one line

    """
    print(tabs + generate_city_str(city, tabs + " "), file=fp)
