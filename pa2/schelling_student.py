"""
CS121: Schelling Model of Housing Segregation -- student code
"""

import math
import utility

MAROON = "M"
BLUE = "B"
FOR_SALE = "F"

ACCEPTABLE_DIFFERENTIAL = 0.10

### Your helper functions can go here OR you can put them after
### do_simulation.  Do not put some before and some after!


def do_simulation(city, homes_for_sale, R, target_score, max_steps):
    """
    Do the full simulation.

    Args:
        city (List[List[str]]): the city to simulate
        homes_for_sale (List[Tuple[int, int]]): a list of locations with homes for sale
        R (int): neighborhood parameter
        target_score (float): the target score for a homeowner
        max_steps (int): maximum number of steps to perform

    Modifies:
        city - updates the city as homeowners relocate
        homes_for_sale - updates the list of homes for sale
          as homeowners relocate and free up their previous homes.

    Returns (int): The number of relocations completed.
    """
