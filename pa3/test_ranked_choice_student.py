import copy
import json
import pytest
import os

import ranked_choice
import ranked_choice_student

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")


RECREATE_MSG = (
    "\nSee the information for {} - Test {} for "
    + "the steps needed to recreate this test.\n"
)

EXCEPTION_MSG = (
    "An unexpected exception {} was "
    "raised and is causing your code to fail:\n  {}\n"
    "This behavior is likely due to a bug in your code.\n"
)

LEN_MSG = "The {} has the wrong length:\n  Actual length:   {}\n  Expected length: {}\n"

NONE_MSG = (
    "The function returned None.\nDid you forget to include a return statement?\n"
)

TYPE_MSG = "The {} has the wrong type:\n  Actual type:   {}\n  Expected type: {}\n"


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


def check_vote_tally(actual, expected, viable_candidates):
    """
    Verify that actual represents the expected vote tally.  Handles
    that case where one or both of the dictionaries may not include
    candidates who did not earn any votes.

    Args:
        actual (Dict[str, Any): the actual vote tally dictionary to check
        expected (Dict[str, Any]): the expected result

    Returns (None | str): None, if the actual and expected values
      are the same and an error message if they are different.
    """
    if not isinstance(actual, dict):
        err_msg = TYPE_MSG.format("The vote tally", type(actual), "Dict[str, int]")
        return err_msg

    # Check the values for the viable candidates
    for cand in viable_candidates:
        if actual.get(cand, 0) == expected.get(cand, 0):
            # this key is good
            continue
        if cand not in actual:
            assert cand in expected
            return f"  The vote tally is missing the key: {repr(cand)}\n"
        elif actual[cand] != expected.get(cand, 0):
            return (
                f"  The vote tally for {repr(cand)} is not correct:\n"
                f"    Actual value: {actual[cand]}\n"
                f"    Expected value: {expected.get(cand, 0)}\n"
            )

    # Look for extra keys in actual
    extra_keys = set(actual.keys()) - set(viable_candidates)
    if len(extra_keys) > 0:
        return f"  The vote tally has extra key(s): {sorted(extra_keys)}"

    return None


def check_key(key, actual, expected, viable_candidates=None):
    """
    Check that value of an individual key in the actual dictionary
    matches the corresponding value in the expected dictionary.
    """
    # check individual fields
    if key not in actual:
        return f"  The key {repr(key)} is missing from the dictionary.\n"

    if key == "vote_tally":
        assert "viable_candidates" in expected
        return check_vote_tally(
            actual["vote_tally"], expected["vote_tally"], expected["viable_candidates"]
        )
    elif not isinstance(actual[key], type(expected[key])):
        return (
            f"  The type of the actual value for the key {repr(key)}\n"
            "  does not match the type of the expected value:\n"
            f"    actual type: {type(actual[key])}\n"
            f"    expected type: {type(expected[key])}\n"
        )
    elif actual[key] != expected[key]:
        return (
            f"  The actual value for the key {repr(key)} does not match\n"
            "  the expected value:\n"
            f"    actual value: {repr(actual[key])}\n"
            f"    expected value: {repr(expected[key])}\n"
        )

    # check passed
    return None


def check_results_dict(actual, expected):
    """
    Verify that the actual value represents the same result
    dictionary as the expected value.

    Args:
        actual (str): the result of calling the student's function
        expected (str): the expected result

    Returns (None | str): None, if the actual and expected values
      are the same and an error message if they are different.
    """
    if not isinstance(actual, dict):
        err_msg = TYPE_MSG.format("the value", type(actual), "Dict[str, Any]")
        return err_msg

    # Check the fixed fields
    for key in ["round_num", "viable_candidates", "vote_tally", "num_exhausted"]:
        err_msg = check_key(key, actual, expected)
        if err_msg:
            return err_msg

    if "drop" in expected:
        err_msg = check_key("drop", actual, expected)
        if err_msg:
            return err_msg
    elif "winner" in expected:
        err_msg = check_key("winner", actual, expected)
        if err_msg:
            return err_msg

    if "winner" in actual and "winner" not in expected:
        err_msg = "  The key 'winner' should not appear in the result dictionary."
        return err_msg

    return None


@pytest.mark.parametrize(("test_params"), read_config_file("run_election.json"))
def test_run_election(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("Run Election", test_num)

    if "ballot_filename" in params:
        ballots = ranked_choice.read_ballots(params["ballot_filename"])
        if not ballots:
            pytest.fail("Unable to read ballots from file: {params['ballot_filename']}")
    else:
        # just in case a rouge candidate string ends up in a test ballot
        ballots = [[c.strip().lower() for c in ballot] for ballot in params["ballots"]]

    ballots_copy = [b[:] for b in ballots]

    # just in case a rogue candidate string ends up in a test set of viable candidates
    viable_candidates = [c.strip().lower() for c in params["viable_candidates"]]
    viable_candidates_copy = viable_candidates[:]

    try:
        actual = ranked_choice_student.run_election(ballots, viable_candidates)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e)
        pytest.fail(err_msg + rmsg)

    # Check the result
    if actual is None:
        pytest.fail(NONE_MSG + rmsg)

    if not isinstance(actual, list):
        err_msg = TYPE_MSG.format("return value", type(actual), "List[Dict[str, Any]]")
        pytest.fail(err_msg + rmsg)

    expected = params["expected"]
    if len(actual) != len(expected):
        err_msg = LEN_MSG.format(len(actual), len(expected))
        pytest.fail(err_msg + rmsg)

    for idx, val in enumerate(actual):
        err_msg = check_results_dict(val, expected[idx])
        if err_msg:
            err_msg_start = (
                f"There is an error in the results dictionary\nat list index {idx}:\n"
            )
            pytest.fail(err_msg_start + err_msg + rmsg)

    # verify that the inputs were not changed
    if ballots_copy != ballots:
        err_msg = "The ballots input was modified, which is not allowed.\n"
        pytest.fail(err_msg + rmsg)

    if viable_candidates != viable_candidates_copy:
        err_msg = "The viable_candidates input was modified, which is not allowed.\n"
        pytest.fail(err_msg + rmsg)

    # Test passed
    return None


def check_mk_round_results_str(actual, expected):
    """
    Helper function that verifies the result of
    mk_round_results_str.

    Args:
        actual (str): the result of calling the student's function
        expected (str): the expected result

    Returns (None | str): None, if the actual and expected values
      are the same and an error message if they are different.
    """
    # Check the result
    if actual is None:
        return NONE_MSG

    if not isinstance(actual, str):
        err_msg = TYPE_MSG.format("return value", type(actual), type(expected))
        return err_msg

    if len(actual) != len(expected):
        err_msg = (
            "The return value has the wrong length:\n"
            f"  Actual length:   {len(actual)}\n"
            f"  Expected length: {len(expected)}\n"
        )
        return err_msg

    for idx, val in enumerate(actual):
        if val != expected[idx]:
            actual_snip = actual[max(0, idx - 5) : min(idx + 5, len(actual))]
            expected_snip = expected[max(0, idx - 5) : min(idx + 5, len(actual))]
            err_msg = (
                "The actual value and the expected value do not match.\n"
                f"  The first difference occurs at index {idx}. Here are\n"
                "  a pair of slices that show the difference:\n"
                f"    Actual snippet:   {repr(actual_snip)}\n"
                f"    Expected snippet: {repr(expected_snip)}\n"
            )
            return err_msg

    # Test passed
    return None


@pytest.mark.parametrize(("test_params"), read_config_file("mk_round_results_str.json"))
def test_mk_round_results_str(test_params):
    test_num, params = test_params

    round_results = params["round_results"]
    round_results_copy = copy.deepcopy(round_results)

    try:
        actual = ranked_choice_student.mk_round_results_str(round_results)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e)
        pytest.fail(err_msg)

    err_msg = check_mk_round_results_str(actual, params["expected"])
    if err_msg:
        rmsg = RECREATE_MSG.format("Make Round Results String", f"{test_num}")
        pytest.fail(err_msg + rmsg)

    if round_results != round_results_copy:
        pytest.fail("The round_results input was modified, which is not allowed.\n")

    # Test passed
    return None
