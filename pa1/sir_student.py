"""
Programming Assignment #1: Modeling Epidemics - student code
CAPP 30121
Autumn 2026

This file contains the functions needed to simulate infection
transmission in a city.
"""

import random

# Defined constants: do not change these values!
NUM_INFECTED_DAYS = 3
NUM_RECOVERED_DAYS = 5
ANTIBODY_BOOST = 0.15


# Task 1
def has_an_infected_neighbor(city, location):
    """
    Determine whether or not a person at a location has an infected
    neighbor in a city with walls.

    Args:
        city (List[Tuple[str, int, float]]): the state of all
          the people in the city being simulated
        location (int): the location of the person to check

    Returns (bool): True, if the person at the specified
      location in the city has an infected neighbor, False
      otherwise.
    """
    assert 0 <= location < len(city), (
        "The location must be valid for the specified city."
    )

    disease_state, _, _ = city[location]
    assert disease_state == "S", (
        "The person at the specified location must be susceptible."
    )

    result = False

    ### Your code to set the value of result goes here

    return result


# Task 2
def compute_next_state_for_person(city, location, infectivity_threshold):
    """
    Compute the next state for the person at location in the
    city based on their current state and the infectivity threshold
    of the disease.

    Args:
        city (List[Tuple[str, int, float]]): the city
        location (int): the location of interest
        infectivity_threshold (float): the threshold used to help
          determine whether a susceptible person gets infected.

    Returns (Tuple[str, int, float]): the person's disease state,
      number of days in that state, and the immunity level of
      the person after one day has passed.
    """
    # validate some of the inputs
    assert 0 <= location < len(city), (
        "The location must be valid for the specified city."
    )
    assert 0.0 <= infectivity_threshold <= 1.0, (
        "The infectivity threshold must be a value between 0.0 and 1.0 inclusive"
    )
    ### Your code goes here
    ### Replace None with an appropriate return value

    return None


# Task 3
def simulate_one_day(city, infectivity_threshold):
    """
    Compute the state of a city after one day, given the specified
    infectivity threshold of the disease.

    Args:
        city (List[Tuple[str, int, float]]): the city
        infectivity_threshold (float): the threshold used to help determine
          whether a person gets infected.

    Returns (List[Tuple[str, int, float]]): the state of the city after a
      day has passed
    """
    assert 0 <= infectivity_threshold <= 1, (
        "The infectivity threshold must be a value between 0.0 and 1.0 inclusive"
    )
    ### Your code goes here
    ### Replace None with an appropriate return value

    return None


# Task 4
def vaccinate_city(city, vax_threshold, vax_boost):
    """
    Construct a new city where eligible people have been vaccinated and
    everyone else stays the same.

    Args:
        city (List[Tuple[str, int, float]]): the city

    Returns (Tuple[str, int, float]): the city with newly vaccinated
      people.
    """
    assert 0 <= vax_threshold <= 1.0, (
        "The vaccination threshold must be a value between 0.0 and 1.0 inclusive."
    )
    assert 0 <= vax_boost <= 1.0, (
        "The vaccination boost must be a value between 0.0 and 1.0 inclusive."
    )

    ### Your code goes here
    ### Replace None with an appropriate return value

    return None


# Tasks 5a, b, and c.
def run_simulation(city,
                   infectivity_threshold,
                   max_days,
                   vax_info=None,
                   infectivity_adjustment=0.0):
    """
    Run a simulation.

    Args:
        city (List[Tuple[str, int, float]]): the city
        infectivity_threshold (float): the threshold used to determine
          whether a person gets infected.
        max_days (int): the maximum number of days to simulate
        vax_info (None | Tuple(float, float)): None or a tuple with
          the immunity threshold for triggering vaccination of a
          susceptible person and the immunity
          boost gained by getting vaccinated (default: None)
        infectivity_adjustment (float): adjustment to infectivity will be
          chosen from the range -infectivity_adjustment to
          infectivity_adjustment (inclusive) (default: 0.0)

    Returns (List[Tuple[str, int, float]]): the final state for the city.
    """
    assert len(city) > 0, "The city must have at least one person."
    assert 0.0 <= infectivity_threshold <= 1.0, (
        "The infectivity threshold must be a value between 0.0 and 1.0 inclusive"
    )
    assert max_days >= 1, "The value of max_days must be at least one."
    assert 0.0 <= infectivity_adjustment <= 1.0, (
        "The infectivity adjust must be a value between 0.0 and 1.0 inclusive"
    )

    ### Your code goes here
    ### Replace None with an appropriate return value

    return None



