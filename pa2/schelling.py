"""
CS121: Schelling Model of Housing Segregation -- command-line interface

Program for simulating a variant of Schelling's model of
housing segregation.  This program takes five parameters:

    filename -- name of a file containing a sample NxN city grid

    r - The radius of the neighborhood: a home at Location (k, l) is in
        the neighborhood of the home at Location (i,j) if 0 <= k < N and
        0 <= l < N.

    target_score: the target value for a homeower's score.

    max_steps - the maximum number of steps to simulate.

Sample: uv run python3 schelling.py --city_file=tests/a20-sample-writeup.txt
    --r=1 --target_score=0.70 --max_steps=1

The sample command is shown on two lines, but should be entered on
a single line at the Linux command-line.
"""

import click
import os
import sys
import utility

# Handle the fact that the student code for do_simulation may not
# be in the same directory as this file.
sys.path.insert(0, os.getcwd())

from schelling_student import do_simulation


@click.command(name="schelling")
@click.option("-c", "--city-file", type=click.Path(exists=True))
@click.option("-r", "--radius", type=int, default=1, help="Neighborhood radius")
@click.option(
    "-t", "--target-score", type=float, default=0.70, help="Target homeowner score"
)
@click.option("-n", "--num-steps", type=int, default=1)
def cmd(city_file, radius, target_score, num_steps):
    """
    Put it all together: do the simulation and process the results.
    """
    if city_file is None:
        print("No parameters specified...just loading the code")
        return

    city = utility.load_city_file(city_file)
    for_sale = utility.find_homes_for_sale(city)

    if len(city) < 20:
        print("Initial state of city:")
        for row in city:
            print(row)
        print()

    num_relocations = do_simulation(city, for_sale, radius, target_score, num_steps)

    if len(city) < 20:
        print("Final state of the city:")
        for row in city:
            print(row)
        print()

    print(f"Total number of relocations done: {num_relocations}")


if __name__ == "__main__":
    cmd()
