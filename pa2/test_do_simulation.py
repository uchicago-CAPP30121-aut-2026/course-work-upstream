"""
CAPP 30121: Schelling Model of Housing Segregation

Test code for do_simulation
"""

import json
import os
import sys
import pytest

BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

# Handle the fact that the grading code may not
# be in the same directory as schelling.py
sys.path.insert(0, os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)

from schelling_student import do_simulation, FOR_SALE  # noqa: E402
import utility  # noqa: E402

LEN_MSG = "The {} has the wrong length:\n  Actual length:   {}\n  Expected length: {}\n"

NONE_MSG = (
    "The function returned None when a value other than None was expected.\n"
    "Did you forget to include a return statement?\n"
)

TYPE_MSG = "The {} has the wrong type:\n  Actual type:   {}\n  Expected type: {}\n"

VAL_MSG = "The {} has the wrong value:\n  Actual value:   {}\n  Expected value: {}\n"

EXCEPTION_MSG = (
    "An unexpected exception {} was "
    "raised and is causing your code to fail:\n  {}\n"
    "This behavior is likely due to a bug in your code.\n"
)


def read_config_file(filename):
    """
    Load the test cases from a JSON file.

    Args:
      filename (string): the name of the test configuration file.

    Returns: (list[tuple]): a list of pairs, where the first
      value in each pair is the test number and the second
      value is a dictionary containing the test parameters
      and the expected value.
    """

    try:
        file_path = os.path.join(TEST_DIR, filename)
        with open(file_path) as f:
            tests = json.load(f)
            # The test numbers start at 1
            return list(zip(range(1, len(tests) + 1), tests))
    except IOError:
        pytest.fail(
            f"Test file ({file_path}) not found\n"
            f"Are you running the tests from the correct directory?\n"
        )


def count_homeowners(city):
    """
    Count the number of occupied homes:

    Args:
        city: (List[List[str]]) the city grid

    Returns (int): the number of occupied homes in the city.
    """
    num_homeowners = 0
    for row in city:
        for home in row:
            if home != FOR_SALE:
                num_homeowners += 1
    return num_homeowners


def check_city(actual_city, params):
    """
    Check the actual city against the expected city.

    Args:
        actual (List[List[str]]): the city returned from do_simulation
        params (Dict[str, Any]): the test parameters

    Returns (None | str): None if the check succeeded and an
      and an error message if the check failed
    """
    # Load the expected city
    expected_city_filename = params["expected_city_filename"]
    expected_city = utility.load_city_file(expected_city_filename)
    if expected_city is None:
        err_msg = (
            "Could not load the expected city.  Are you running the"
            "tests in your pa2 directory?"
        )
        return err_msg

    if actual_city != expected_city:
        # City is incorrect: first check for missing/added homewonwers
        expected_num_homeowners = count_homeowners(expected_city)
        actual_num_homeowners = count_homeowners(actual_city)
        if actual_num_homeowners != expected_num_homeowners:
            if actual_num_homeowners < expected_num_homeowners:
                err_msg = "Homeowners are fleeing the city!\n"
            else:
                assert actual_num_homeowners != expected_num_homeowners
                err_msg = "The city is gaining homeowners.\n"
            err_msg += (
                f"  Actual number of homeowners: {actual_num_homeowners}\n"
                f"  Expected number of homeowners: {expected_num_homeowners}\n"
            )
            return err_msg

        # Look for a mismatch.
        mismatch = utility.find_mismatch(actual_city, expected_city)
        if mismatch:
            (i, j) = mismatch
            actual_ho = actual_city[i][j]
            expected_ho = expected_city[i][j]
            err_msg = (
                "The actual and expected homeowners do not"
                f" match at location ({mismatch})\n"
                f"  Actual homeowner at Location ({mismatch}): '{actual_ho}'\n"
                f"  Expected homeowner at Location ({mismatch}): '{expected_ho}'\n"
            )
            return err_msg

    return None


def check_for_sale_list(actual, params):
    """
    Check a for sale list

    Args:
        actual (List[Tuple(int, int)]): the actual list of homes for sale
        params (Dict[str, Any]): the test paramers

    Returns (None | string): returns None if the checks succeeded
      and an error message if the check failed
    """
    expected_for_sale_filename = params["expected_for_sale_filename"]
    expected = utility.load_for_sale_file(expected_for_sale_filename)

    # Check the type
    if not isinstance(actual, list):
        return TYPE_MSG.format("for-sale list", "list", type(actual))

    # Check length
    if len(actual) != len(expected):
        return LEN_MSG.format("for-sale list", len(actual), len(expected))

    # Check the individual elements of the list
    for i, actual_loc in enumerate(actual):
        expected_loc = expected[i]
        if actual_loc != expected_loc:
            return (
                f"The for-sale list has the wrong value at index {i}:\n"
                f"  Actual location at index {i}:   {actual_loc}\n"
                f"  Expected location at index {i}: {expected_loc}\n"
            )

    # Test passed
    return None


def helper_test_do_simulation(test_params):
    """Do one simulation with the specified parameters

    Compare the number of relocations, the state of the city, and the
    state of the for-sale list after the simulation with the expected
    values.

    Args:
        test_params (Tuple[int, Dict[str, Any]]: a tuple
          with the test number and the test parameters

    Returns (None | str): None if the test succeeds and
      an error message if the test fails
    """

    # Set up the test

    test_num, params = test_params
    city_filename = os.path.join(params["city_filename"])
    R = params["R"]
    target_score = params["target_score"]
    max_num_steps = params["max_num_steps"]

    recreate_msg = (f"\nSee the information for do_simulation - Test {test_num} for " +
                    "the steps needed to recreate this test.\n")

    # Read the city from a file
    actual_city = utility.load_city_file(city_filename)
    if actual_city is None:
        err_msg = (
            "Could not load the city file.  Are you running these\n"
            "tests from your pa2 directory?\n"
        )
        return err_msg + recreate_msg

    # Set up the initial for sale list
    if "initial_for_sale" not in params:
        for_sale = utility.find_homes_for_sale(actual_city)
    else:
        for_sale = [tuple(t) for t in params["initial_for_sale"]]

    # call the student's function
    try:
        actual_num_relocations = do_simulation(
            actual_city, for_sale, R, target_score, max_num_steps
        )
    except Exception as e:
        return EXCEPTION_MSG.format(type(e).__name__, e) + recreate_msg

    # Check the return value
    expected_num_relocations = params["expected_num_relocations"]
    if actual_num_relocations != expected_num_relocations:
        err_msg = (
            "Actual and expected number of relocations do not match:\n"
            f"  Actual number of relocations: {actual_num_relocations}\n"
            f"  Expected number of relocations: {expected_num_relocations}\n"
        )
        return err_msg + recreate_msg

    # Check the city
    err_msg = check_city(actual_city, params)
    if err_msg:
        return err_msg + recreate_msg

    # Check the for-sale list
    err_msg = check_for_sale_list(for_sale, params)
    if err_msg:
        return err_msg + recreate_msg

    # Test passed
    return None


@pytest.mark.timeout(60)
@pytest.mark.parametrize("params", read_config_file("test_do_simulation_small.json"))
def test_do_simulation_small(params):
    err_msg = helper_test_do_simulation(params)
    if err_msg:
        pytest.fail(err_msg)


@pytest.mark.timeout(60)
@pytest.mark.parametrize("params", read_config_file("test_do_simulation_medium.json"))
def test_do_simulation_medium(params):
    err_msg = helper_test_do_simulation(params)
    if err_msg:
        pytest.fail(err_msg)


@pytest.mark.timeout(60)
@pytest.mark.parametrize("params", read_config_file("test_do_simulation_large.json"))
def test_do_simulation_large(params):
    err_msg = helper_test_do_simulation(params)
    if err_msg:
        pytest.fail(err_msg)
        
