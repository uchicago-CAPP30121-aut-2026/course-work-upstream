"""
Programming Assignment #1: Modeling Epidemics
CAPP 30121
Autumn 2026

This program simulates infection transmission in a city.

This file contains the command-line interface for the program.
This program takes seven parameters:

- the name of a file containing a city (required)
- the infectivity threshold to use in the simulation
  (optional with a default of 0.5)
- the number of days to simulate (optional with default of 1)
- the vaccination threshold (optional with a default of None)
- the vaccination boost (optional with a default of None)
- the infectivity adjustment (optional with a default of 0.0)

Here is a sample use of the program:

$ uv run python3 sir.py sample_cities/city_a.txt --infectivity-threshold 0.5
    --num-days 4 --random-seed 14003 --vax-threshold 0.75 --vax-boost 0.25
    --infectivity-adjustment 0.1

The sample command is shown on three lines, but should be entered on
a single line at the Linux command-line.
"""

import click
import random
import sys

import helpers
import sir_student

@click.command()
@click.argument("filename", type=str)
@click.option("--infectivity-threshold", default=0.5, type=float)
@click.option("--num-days", default=1, type=int)
@click.option("--random-seed", default=None, type=int)
@click.option("--vax-threshold", default=None, type=float)
@click.option("--vax-boost", default=None, type=float)
@click.option("--infectivity-adjustment", default=0.0, type=float)
def cmd(filename, infectivity_threshold, random_seed, num_days,
        vax_threshold, vax_boost, infectivity_adjustment):
    """
    Process the command-line arguments and do the work.
    """
    if not (vax_boost is None and vax_threshold is None):
        if (vax_boost is None or vax_threshold is None):
            print("Either both vax threshold and vax boost need to be specified,"
                  " or neither.", file=sys.stderr)
            sys.exit(-2)
        vax_info = (vax_threshold, vax_boost)
    else:
        vax_info = None

    if random_seed:
        random.seed(random_seed)

    city = helpers.parse_city_file(filename)
    if not city:
        return -1

    print("Running simulation ...")
    final_city = sir_student.run_simulation(city,
                                            infectivity_threshold,
                                            num_days,
                                            vax_info,
                                            infectivity_adjustment)

    print("Final City:")
    helpers.print_city(sys.stdout, final_city, "  ")

    return 0

if __name__ == "__main__":
    cmd()
