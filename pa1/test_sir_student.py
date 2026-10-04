'''
Test code for Modeling Epidemics

Emma Nechamkin and Anne Rogers
July 2018

Borja Sotomayor
September 2018, 2020

Anne Rogers
July 2019, July 2021

Hannah Morgan
September 2022, 2023

Anne Rogers
April 2026
'''

import json
import os
import sys
import random

import pytest

import helpers

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

import sir_student   # noqa: E402

# Error messages

RECREATE_MSG = ("\nSee the information for {} - Test {} for " +
                "the steps needed to recreate this test.\n")

LEN_MSG = ("The {} has the wrong length:\n"
           "  Actual length:   {}\n"
           "  Expected length: {}\n")

NONE_MSG = ("The function returned None when a value other than None was expected.\n"
            "Did you forget to include a return statement?\n")

TYPE_MSG = ("The {} has the wrong type:\n"
            "  Actual type:   {}\n"
            "  Expected type: {}\n")

VAL_MSG = ("The {} has the wrong value:\n"
            "  Actual value:   {}\n"
            "  Expected value: {}\n")

EXCEPTION_MSG = ("An unexpected exception {} was "
                 "raised and is causing your code to fail:\n  {}\n"
                 "This behavior is likely due to a bug in your code.\n")

####################### Test helpers #######################

def read_config_file(filename):
    '''
    Load the test cases from a JSON file.

    Args:
      filename (string): the name of the test configuration file.

    Returns: (list[tuple]): a list of pairs, where the first
      value in each pair is the test number and the second
      value is a dictionary containing the test parameters
      and the expected value.
    '''

    try:
        file_path = os.path.join(TEST_DIR, filename)
        with open(file_path) as f:
            tests = json.load(f)

            for t in tests:
                if "city" in t:
                    # convert elements from lists into tuples
                    t["city"] = [tuple(v) for v in t["city"]]
                elif "city_params" in t:
                    # make the city from the specified parameters
                    # if needed.
                    t["city"] = helpers.mk_city(*t["city_params"])

            # The test numbers start at 1
            return list(zip(range(1, len(tests) + 1), tests))
    except IOError:
        pytest.fail(f"Test file ({file_path}) not found\n"
                    f"Are you running the tests from the correct directory?\n")


def run_and_check_modifications(fn, params):
    """
    Call a student function.  Verify that the return value is
    not None and that the function did not modify the city input.
    Also, catch any exceptions that are thrown.

    Args:
      fn: a function that takes a city as its only parameter, calls a
        function from sir_student.py, and returns its result.

    Returns Tuple[(Any | None), (str | None)]: If the called function fails,
      returns None, or modifies the city
      input, then this function will return a pair with None and an
      error message.  Otherwise, it will return a pair with the value
      returned from the called function and None.
    """

    city = params["city"]
    city_copy = city[:]

    # call the supplied function
    try:
        actual = fn(city)
    except Exception as e:
        return None, EXCEPTION_MSG.format(type(e).__name__, e)

    # None check
    if actual is None:
        return None, NONE_MSG

    # Modification check
    if city_copy != city:
        return None, "The function modified the input city, which is not allowed.\n"

    # The student's function passed the basic tests.
    return actual, None


def check_person(tag, actual, expected):
    """
    Do a few standard checks on a person.

    Args:
        tag (str): information about the value to include in the error message
        actual (Any): the actual value computed using the student's function
        expected (Tuple[str, int, float]): the expected value

    Returns (None | string): returns None if the test succeeded and an
      error message if the test failed
    """
    # Do this check again, because this function
    # is used to verify the contents of cities
    # as well as the return value from compute_next_state_for_person.
    if actual is None:
        return tag + " is None, when a tuple is expected."

    # Check the type of the actual value
    if not isinstance(actual, tuple):
        return TYPE_MSG.format(tag, type(actual), "tuple")

    # Check length
    if len(actual) != len(expected):
        return LEN_MSG.format(tag, len(actual), len(expected))

    # Check element types
    actual_disease_state, actual_num_days, actual_immunity_level = actual
    expected_disease_state, expected_num_days, expected_immunity_level = expected
    if ((not isinstance(actual_disease_state, type(expected_disease_state))) or
        (not isinstance(actual_num_days, type(expected_num_days))) or
        (not isinstance(actual_immunity_level, type(expected_immunity_level)))):
        a_type_str = (f"tuple[{type(actual_disease_state)},"
                      f" {type(actual_num_days)},"
                      f" {type(actual_immunity_level)}]")
        e_type_str = (f"tuple[{type(expected_disease_state)},"
                      f" {type(expected_num_days)},"
                      f" {type(expected_immunity_level)}]")
        return TYPE_MSG.format(tag, a_type_str, e_type_str)

    # Check the element values
    if (actual_disease_state != expected_disease_state or
        actual_num_days != expected_num_days or
        actual_immunity_level != pytest.approx(expected_immunity_level)):
        return VAL_MSG.format(tag, actual, expected)

    # Test passed
    return None


def check_city(actual, expected):
    """
    Check a city.

    Args:
        actual (tuple or list): the actual value
        expected (typle or list): the expected value

    Returns (None | string): returns None if the test succeeded
      and an error message if the test failed
    """
    # Check the type
    if not isinstance(actual, list):
        return TYPE_MSG.format("city", "list", type(actual))

    # Check length
    if len(actual) != len(expected):
        return LEN_MSG.format("city", len(actual), len(expected))

    # Check the individual elements of the list
    for i, actual_person in enumerate(actual):
        expected_person = expected[i]
        err_msg = check_person(f"person at location {i} in the city",
                               actual_person,
                               expected_person)
        if err_msg:
            return err_msg

    # Test passed
    return None


def check_scalar_result(tag, actual, expected):
    """
    Verify that the actual (scalar) value return from a function
    matches the expected value.

    Args:
        tag (str): information about the value to include in error messages
        actual (Any): actual value.
        expected (Any): expected value

    Returns (None | string): returns None if the test succeeded and an error message
      if the test failed
    """
    # Check the type
    if not isinstance(actual, type(expected)):
        return TYPE_MSG.format(tag, type(expected), type(actual))

    # Check the value.
    if actual != expected:
        return VAL_MSG.format(tag, actual, expected)

    # Test passed
    return None


####################### Task test functions #######################

# Task 1
@pytest.mark.parametrize(
    "test_params",
    read_config_file("has_an_infected_neighbor.json"))
def test_has_an_infected_neighbor(test_params):
    """
    Test for has_an_infected_neighbor

    Inputs:
      test_params (int, dictionary): the test number and the test
      parameters dictionary:
        city, index of a location in the city,
        the expected result
    """
    test_num, params = test_params
    task_name = "Task 1: Has an infected neighbor"
    rmsg = RECREATE_MSG.format(task_name, test_num)

    # Run the student's function and do some basic checks
    loc = params["location"]
    def test_fn(cc):
        return sir_student.has_an_infected_neighbor(cc, loc)

    actual, err_msg = \
        run_and_check_modifications(test_fn, params)
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Check the result
    err_msg = check_scalar_result("return value", actual, params["expected"])
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Test passed
    return None



# Task 2
@pytest.mark.parametrize(
    "test_params",
    read_config_file("compute_next_state_for_person.json"))
def test_compute_next_state_for_person(test_params):
    """
    Test for compute_next_state_for_person

    Inputs:
      test_params (int, dictionary): the test number and the test
      parameters dictionary:
        city, index of a location in the city,
        the expected result, purpose of the test
    """
    test_num, params = test_params
    task_name = "Task 2: Compute next state for person"
    rmsg = RECREATE_MSG.format(task_name, test_num)

    # Run the student's function and do some basic checks
    loc = params["location"]
    infectivity_threshold = params["infectivity_threshold"]
    def test_fn(cc):
        return sir_student.compute_next_state_for_person(cc,
                                                         loc,
                                                         infectivity_threshold)
    actual, err_msg = run_and_check_modifications(test_fn, params)
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Check the result
    expected = tuple(params["expected"])
    err_msg = check_person("returned person", actual, expected)
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Test passed
    return None


# Task 3
@pytest.mark.parametrize(
    "test_params",
    read_config_file("simulate_one_day.json"))
def test_simulate_one_day(test_params):
    """
    Test for simulate_day

    Inputs:
      test_params (int, dictionary): the test number and the test
      parameters dictionary:
        city, infectivity_threshold, and the expected result
    """
    test_num, params = test_params
    task_name = "Task 3: Simulate one day"
    rmsg = RECREATE_MSG.format(task_name, test_num)

    # Run the student's function and do some basic checks
    infectivity_threshold = params["infectivity_threshold"]
    def test_fn(cc):
        return sir_student.simulate_one_day(cc, infectivity_threshold)
    actual, err_msg = run_and_check_modifications(test_fn, params)
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Convert the elements of the expected result from lists to tuples
    expected = [tuple(v) for v in params["expected"]]

    # Check the result
    err_msg = check_city(actual, expected)
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Test passed
    return None


def helper_run_sim(test_params, task_name):
    """
    Helper for testing run_simulation

    Inputs:
      params (int, dictionary): the test number and the test
      task_name (str): the name of the task
    """
    test_num, params = test_params
    rmsg = RECREATE_MSG.format(task_name, test_num)

    infectivity_threshold = params["infectivity_threshold"]
    max_days = params["max_days"]
    # 0.0 is the default value for vax_info
    vax_info = params.get("vax_info", None)
    infectivity_adjustment = params.get("infectivity_adjustment", 0.0)
    if infectivity_adjustment > 0.0:
        assert "seed" in params
        random.seed(params["seed"])

    def test_fn(cc):
        return sir_student.run_simulation(cc,  infectivity_threshold,
                                          max_days, vax_info,
                                          infectivity_adjustment)
    actual_city, err_msg = run_and_check_modifications(test_fn, params)
    if err_msg:
        return err_msg + rmsg

    # fix the type of the elements
    expected_city = [tuple(v) for v in params["expected"]]
    err_msg = check_city(actual_city, expected_city)
    if err_msg:
        return err_msg + rmsg

    # Test passed
    return None


# Task 4
@pytest.mark.parametrize(
    "test_params",
    read_config_file("vaccinate_city.json"))
def test_vaccinate_city(test_params):
    """
    Test for vaccinate_city

    Inputs:
      test_params (int, dictionary): the test number and the test
      parameters dictionary:
        city, vax_info, the expected result, purpose of the test
    """
    test_num, params = test_params
    task_name = "Task 4: Vaccinate City"
    rmsg = RECREATE_MSG.format(task_name, test_num)

    # Run the student's function and do some basic checks
    vax_info = params["vax_info"]
    print("vax_info:", vax_info)
    def test_fn(cc):
        return sir_student.vaccinate_city(cc, *vax_info)
    actual, err_msg = run_and_check_modifications(test_fn, params)
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Convert the elements of the expected result from lists to tuples
    expected = [tuple(v) for v in params["expected"]]

    # Check the result
    err_msg = check_city(actual, expected)
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # Test passed
    return None


# Task 5a
@pytest.mark.parametrize(
    "test_params",
    read_config_file("task_5a.json"))
def test_task5a(test_params):
    """
    Helper for most basic version of run_simulation

    Inputs:
      test_params (int, dictionary): the test number and the test
      parameters dictionary:
        city, infectivity_threshold,  maximum number of days,
        expected result
    """
    task_name = "Task 5a"

    err_msg = helper_run_sim(test_params, task_name)
    if err_msg:
        pytest.fail(err_msg)

    # test passed
    return None


# Task 5b
@pytest.mark.parametrize(
    "test_params",
    read_config_file("task_5b.json"))
def test_task5b(test_params):
    """
    Test for run_simulation w/ vaccination

    Inputs:
      test_params (int, dictionary): the test number and the test
      parameters dictionary:
        city, infectivity_threshold,  maximum number of days,
        expected result
    """
    task_name = "Task 5b"
    err_msg = helper_run_sim(test_params, task_name)
    if err_msg:
        pytest.fail(err_msg)

    # Test passed
    return None


# Task 5c
@pytest.mark.parametrize(
    "test_params",
    read_config_file("task_5c.json"))
def test_task5c(test_params):
    """
    Test run_simulation w/ vaccination and adjustments to the
    infectivity.

    Inputs:
      test_params (int, dictionary): the test number and the test
      parameters dictionary:
        city, infectivity_threshold,  maximum number of days,
        expected result

    """
    task_name = "Task 5c: final version of run simulation"
    err_msg = helper_run_sim(test_params, task_name)
    if err_msg:
        pytest.fail(err_msg)

    # test passed
    return None
