import json
import pytest
import os
import sys

import ranked_choice
import helpers

# get the student's code from the current directory
# not from the directory the test file lives in
sys.path.insert(0, ".")
import ranked_choice_student


# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

NONE_MSG = (
    "The method returned None when a {} was expected.\n"
    "Did you forget to include a return statement?\n"
)

TYPE_MSG = "The {} has the wrong type:\n  Actual type:   {}\n  Expected type: {}\n"

LEN_MSG = "The {} has the wrong length:\n  Actual length:   {}\n  Expected length: {}\n"

RECREATE_MSG = (
    "\nSee the information for {} - Test {} for\n"
    + "the steps needed to recreate this test.\n"
)

EXCEPTION_MSG = (
    "An unexpected exception:\n\n"
    "  {}: {}\n\n"
    "was raised in the {} method and is causing your code\n"
    "to fail. This behavior is likely due to a bug in your code.\n"
)

CON_EXCEPTION = "{} constructor failed with an exception:\n  {}:{}\n"


def check_return_value(actual, expected):
    """
    Do basic checks---equality, unexpected/expected None, type, etc---
    on the actual and expected return values.
    """
    if (expected is None and actual is None) or (actual == expected):
        # test passed
        return None

    val_err_msg = (
        "The method returned the wrong value:\n"
        "  Actual return value: {}\n"
        "  Expected return value: {}\n"
    )

    # Test failed: what is wrong with the actual value?
    if actual is None or expected is None:
        return val_err_msg.format(repr(actual), repr(expected))

    if not isinstance(actual, type(expected)):
        # Return value has the wrong type
        return TYPE_MSG.format("return value", type(actual), type(expected))

    return val_err_msg.format(repr(actual), repr(expected))


def check_sequence(actual, expected):
    """
    Do basic checks on a sequence return value.
    """
    if (expected is None and actual is None) or (actual == expected):
        # test passed
        return None

    val_err_msg = (
        "The method returned the wrong value:\n"
        "  Actual return value: {}\n"
        "  Expected return value: {}\n"
    )

    # Test failed: what is wrong wrong with the actual value?
    if actual is None or expected is None:
        return val_err_msg.format(repr(actual), repr(expected))

    if not isinstance(actual, type(expected)):
        # Return value has the wrong type
        return TYPE_MSG.format("return value", type(actual), type(expected))

    if len(actual) != len(expected):
        return LEN_MSG.format("return value", len(actual), len(expected))

    # Value has the right type and length, but is not correct
    if len(expected) < 3:
        # print the whole value for pairs.
        return val_err_msg.format(repr(actual), repr(expected))
    else:
        for idx, eval in enumerate(expected):
            aval = actual[idx]
            if eval != aval:
                if isinstance(expected, str):
                    lb = max(0, idx - 5)
                    ub = min(idx + 5, len(expected))
                    return (
                        f"The method returned the wrong value.\n"
                        f"  The first difference occurs at index {idx}.  Here\n"
                        "   are a pair of slices that show the first difference\n"
                        "   a bit of context:\n"
                        f"    actual[{lb} : {ub}]: '{actual[lb:ub]}'\n"
                        f"    expected[{lb} : {ub}]: '{expected[lb:ub]}'\n"
                    )
                else:
                    return (
                        f"The method returned the wrong value.\n"
                        f"The first difference is at index {idx}\b"
                        f"  Actual value at index {idx}: {repr(actual)}\n"
                        f"  Expected value at index {idx}: {repr(expected)}\n"
                    )

    assert False, "Code should never reach this assertion."


def check_viable_method(params, method_name, method_fn, expected_tag):
    """
    Helper for checking ViableCandidate methods.
    """

    try:
        vc = ranked_choice_student.ViableCandidates(params["cands_in_order"])
    except Exception as e:
        return CON_EXCEPTION.format("ViableCandidates", type(e).__name__, e)

    try:
        actual = method_fn(vc)
    except Exception as e:
        return EXCEPTION_MSG.format(type(e).__name__, e, method_name)

    if "order" in expected_tag:
        expected = tuple(params["expected"][expected_tag])
    else:
        expected = params["expected"][expected_tag]
    return check_return_value(actual, expected)


@pytest.mark.parametrize(("test_params"), helpers.read_config_file("viable.json"))
def test_viable_get_num_viable(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("ViableCandidates get_num_viable", test_num)

    err_msg = check_viable_method(
        params, "get_num_viable", lambda vc: vc.get_num_viable(), "num_viable"
    )
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed.
    return None


@pytest.mark.parametrize(("test_params"), helpers.read_config_file("viable.json"))
def test_viable_is_viable(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("ViableCandidates is_viable", test_num)

    for cand in params["cand_args"]:
        err_msg = check_viable_method(
            params, "is_viable", lambda vc: vc.is_viable(cand), f"is_viable_{cand}"
        )
        if err_msg:
            pytest.fail(err_msg + rmsg)

    # test passed.
    return None


@pytest.mark.parametrize(("test_params"), helpers.read_config_file("viable.json"))
def test_viable_get_candidates_in_order(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("ViableCandidates get_candidates_in_order", test_num)

    err_msg = check_viable_method(
        params,
        "get_candidates_in_order",
        lambda vc: vc.get_candidates_in_order(),
        "in_order",
    )
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed.
    return None


@pytest.mark.parametrize(("test_params"), helpers.read_config_file("viable.json"))
def test_viable_str(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("ViableCandidates __str__", test_num)

    err_msg = check_viable_method(params, "__str__", lambda vc: str(vc), "str")
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed.
    return None


@pytest.mark.parametrize(("test_params"), helpers.read_config_file("viable.json"))
def test_viable_drop(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("ViableCandidates drop", test_num)

    try:
        vc = ranked_choice_student.ViableCandidates(params["cands_in_order"])
    except Exception as e:
        pytest.fail(CON_EXCEPTION("ViableCandidates", type(e).__name__, e) + rmsg)

    # run the student's function
    try:
        actual = vc.drop(params["drop_cand"])
    except AssertionError:
        if params["expected"].get("drop_exception_expected", False):
            # test passed -- an AssertionError was expected.
            return
        # test failed -- an AssertionError was NOT expected.
        err_msg = (
            "The drop method generated an AssertionError when one was not expected.\n"
        )
        pytest.fail(err_msg + rmsg)
    except Exception as e:
        pytest.fail(EXCEPTION_MSG.format(type(e).__name__, e, "drop method") + rmsg)

    if params["expected"].get("drop_exception_expected", False):
        # test failed -- an AssertionError was expected.
        err_msg = (
            "The drop method was expected to generate an.\n"
            "AssertionError. No such error was generated.\n"
        )
        pytest.fail(err_msg + rmsg)

    val_err_msg = (
        "The method returned the wrong value:\n"
        "  Actual return value: {}\n"
        "  Expected return value: {}\n"
    )

    if actual is None:
        descr = "an instance of ranked_choice_students.ViableCandidates"
        err_msg = val_err_msg.format(repr(actual), descr)

        pytest.fail(err_msg + rmsg)

    if not isinstance(actual, ranked_choice_student.ViableCandidates):
        # Return value has the wrong type
        err_msg = TYPE_MSG.format(
            "return value", type(actual), "ranked_choice_student.ViableCandidates"
        )
        pytest.fail(err_msg + rmsg)

    actual_in_order = actual.get_candidates_in_order()
    expected_in_order = tuple(params["expected"]["drop"])
    if actual_in_order != expected_in_order:
        err_msg = (
            "actual.get_candidates_in_order() returned the wrong value,\n"
            "which suggests that the return value from the drop method\n"
            "was constructed with the wrong list of candidates:\n"
            f"  actual.get_candidates_in_order returned:  {actual_in_order}\n"
            f"  expected result is:                       {expected_in_order}\n"
        )
        pytest.fail(err_msg + rmsg)

    # test passed.
    return None


@pytest.mark.parametrize(("test_params"), helpers.read_config_file("ballot.json"))
def test_ballot_find_first_viable(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("Ballot find_first_viable method", test_num)

    try:
        b = ranked_choice_student.Ballot(params["ranked_choices"])
    except Exception as e:
        pytest.fail(CON_EXCEPTION("Ballot", type(e).__name__, e) + rmsg)

    try:
        vc = ranked_choice_student.ViableCandidates(params["cands_in_order"])
    except Exception as e:
        pytest.fail(
            CON_EXCEPTION.format("ViableCandidates", type(e).__name__, e) + rmsg
        )

    try:
        actual = b.find_first_viable(vc)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "find_first_viable") + rmsg
        pytest.fail(err_msg)

    err_msg = check_return_value(actual, params["expected_first_viable"])
    if err_msg:
        pytest.fail(err_msg + rmsg)


@pytest.mark.parametrize(("test_params"), helpers.read_config_file("ballot.json"))
def test_ballot_str(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("Ballot __str__ method", test_num)

    try:
        b = ranked_choice_student.Ballot(params["ranked_choices"])
    except Exception as e:
        pytest.fail(CON_EXCEPTION("Ballot", type(e).__name__, e) + rmsg)

    try:
        actual = str(b)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "Ballot __str__") + rmsg
        pytest.fail(err_msg)

    err_msg = check_sequence(actual, params["expected_str"])
    if err_msg:
        pytest.fail(err_msg + rmsg)


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("precinct_run_round.json")
)
def test_precinct_run_round(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("Precinct run_round", test_num)
    try:
        p = ranked_choice.mk_precinct(
            params["pid"], ballot_filename=params["ballot_filename"]
        )
    except Exception as e:
        pytest.fail(
            EXCEPTION_MSG.format(type(e).__name__, e, "ranked_choice.mk_precinct")
            + rmsg
        )

    try:
        vc = ranked_choice_student.ViableCandidates(params["cands_in_order"])
    except Exception as e:
        pytest.fail(
            CON_EXCEPTION.format("ViableCandidates", type(e).__name__, e) + rmsg
        )

    try:
        actual = p.run_round(vc)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "Precinct run_round")
        pytest.fail(err_msg + rmsg)

    # Change the type of the expected value from list to tuple.
    err_msg = check_sequence(actual, tuple(params["expected_run_round"]))
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("precinct_run_round.json")
)
def test_precinct_str(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("Precinct __str__", test_num)

    try:
        p = ranked_choice.mk_precinct(
            params["pid"], ballot_filename=params["ballot_filename"]
        )
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "ranked_choice.mk_precinct")
        pytest.fail(err_msg + rmsg)

    try:
        actual = str(p)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "Precinct __str__")
        pytest.fail(err_msg + rmsg)

    err_msg = check_sequence(actual, params["expected_str"])
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed
    return None


def rr_helper(params, fn, fn_name, expected_key, assertion_failure_expected=False):
    try:
        vc = ranked_choice_student.ViableCandidates(params["cands_in_order"])
    except Exception as e:
        return CON_EXCEPTION.format("ViableCandidates", type(e).__name__, e)

    try:
        rr = ranked_choice_student.RoundResults(params["round_num"], vc)
    except Exception as e:
        return CON_EXCEPTION("RoundResults", type(e).__name__, e)

    try:
        for pid, result in params["per_precinct_results"].items():
            (vote_tally, num_exhausted_ballots) = result
            rr.add_precinct_results(pid, vote_tally, num_exhausted_ballots)
    except Exception as e:
        ename = type(e).__name__
        err_msg = (
            f"An unexpected exception {ename} was raised while executing\n"
            "the add_precinct_results method and is causing "
            f"your code to fail:\n  {e}\n"
            "This behavior is likely due to a bug in your code.\n"
        )
        return err_msg

    try:
        actual = fn(rr)
    except AssertionError:
        if assertion_failure_expected:
            # the test passed
            return None
        # test failed -- an AssertionError was NOT expected.
        err_msg = (
            f"The {fn_name} method generated an AssertionError "
            "when one was not expected.\n"
        )
        return err_msg
    except Exception as e:
        return EXCEPTION_MSG.format(type(e).__name__, e, fn_name)

    if assertion_failure_expected:
        # test failed -- an AssertionError was expected.
        err_msg = (
            f"The {fn_name} method was expected to generate an AssertionError.\n"
            "No such error was generated.\n"
        )
        return err_msg

    if "audit" in expected_key:
        # show partial results for non-matching audit strings
        return check_sequence(actual, params["expected"][expected_key])
    else:
        return check_return_value(actual, params["expected"][expected_key])


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("round_results.json")
)
def test_round_results_cand_to_drop(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("RoundResults find_cand_to_drop", test_num)

    # drop should raise an exception failure of all the ballots are exhausted or
    # if there is a winner.
    drop_assertion_expected = params["expected"]["all_exhausted"] or (
        params["expected"]["winner"] is not None
    )

    err_msg = rr_helper(
        params,
        lambda rr: rr.find_cand_to_drop(),
        "find_cand_to_drop",
        "drop",
        drop_assertion_expected,
    )
    
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("round_results.json")
)
def test_round_results_are_all_exhausted(test_params):
    test_num, params = test_params

    err_msg = rr_helper(
        params,
        lambda rr: rr.are_all_exhausted(),
        "are_all_exhausted",
        "all_exhausted",
        False,
    )
    if err_msg:
        pytest.fail(
            err_msg + RECREATE_MSG.format("RoundResults are_all_exhausted", test_num)
        )

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("round_results.json")
)
def test_round_results_find_winner(test_params):
    test_num, params = test_params

    # the test should throw an assertion failure if all the ballots
    # are exhausted.
    winner_assertion_failure = params["expected"]["all_exhausted"]

    err_msg = rr_helper(
        params,
        lambda rr: rr.find_winner(),
        "find_winner",
        "winner",
        winner_assertion_failure,
    )
    if err_msg:
        pytest.fail(err_msg + RECREATE_MSG.format("RoundResults find_winner", test_num))

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("round_results.json")
)
def test_round_results_audit_long(test_params):
    test_num, params = test_params

    err_msg = rr_helper(
        params,
        lambda rr: rr.construct_audit_str(True),
        "construct_audit_str(True)",
        "audit_str_long",
        False,
    )
    if err_msg:
        pytest.fail(err_msg + RECREATE_MSG.format("RoundResults find_winner", test_num))

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("round_results.json")
)
def test_round_results_audit_short(test_params):
    test_num, params = test_params

    err_msg = rr_helper(
        params,
        lambda rr: rr.construct_audit_str(False),
        "construct_audit_str(False)",
        "audit_str_short",
        False,
    )
    if err_msg:
        pytest.fail(err_msg + RECREATE_MSG.format("RoundResults find_winner", test_num))

    # test passed
    return None


def check_round_results(idx, actual_rr, expected_rr):
    val_err_msg = (
        "The RoundResults structure at index {} has the\n"
        "wrong value:\n"
        "  Actual {}: {}\n"
        "  Expected {}: {}\n"
    )

    # Check None
    if actual_rr is None:
        err_msg = (
            f"Round results value at index {idx} is None\n"
            f"when an instance of RoundResults was expected"
        )
        return err_msg

    # Check type
    if not isinstance(actual_rr, ranked_choice_student.RoundResults):
        err_msg = (
            f"Round results value at index {idx} is has type {type(actual_rr)}\n"
            f"when an instance of RoundResults was expected"
        )
        return err_msg

    val_err_msg = (
        "The RoundResults structure at index {} has the\n"
        "wrong value:\n"
        "  Actual {}: {}\n"
        "  Expected {}: {}\n"
    )

    # check all_exhausted, winner and drop candidates.
    try:
        actual_all_exhausted = actual_rr.are_all_exhausted()
    except Exception as e:
        return (
            f"An unexpected exception occurred when checking the RoundResults "
            "structure at index {idx}\n"
            f"  {type(e).__name__}: {e}\n\n"
            "was raised in the are_all_exhausted method and is causing your code\n"
            "to fail. This behavior is likely due to a bug in your code.\n"
        )

    err_msg = check_return_value(actual_all_exhausted, expected_rr["all_exhausted"])
    if err_msg:
        return err_msg
    elif expected_rr["all_exhausted"]:
        # the test passed, don't check for a winner or a drop candidate.
        return None

    try:
        actual_winner = actual_rr.find_winner()
    except Exception as e:
        return (
            "An unexpected exception occurred when checking the "
            f"RoundResults structure at index {idx}\n"
            f"  {type(e).__name__}: {e}\n\n"
            "was raised in the find_winner method and is causing your code\n"
            "to fail. This behavior is likely due to a bug in your code.\n"
        )

    err_msg = check_return_value(actual_winner, expected_rr["winner"])
    if err_msg is not None:
        return val_err_msg.format(
            idx, "winner", repr(actual_winner), "winner", repr(expected_rr["winner"])
        )
    elif actual_winner is not None:
        return None

    try:
        actual_drop = actual_rr.find_cand_to_drop()
    except Exception as e:
        return (
            "An unexpected exception occurred when checking the "
            f"RoundResults structure at index {idx}\n"
            f"  {type(e).__name__}: {e}\n\n"
            "was raised in the find_cand_to_drop method and is causing your code\n"
            "to fail. This behavior is likely due to a bug in your code.\n"
        )

    err_msg = check_return_value(actual_drop, expected_rr["drop"])
    if err_msg is not None:
        return val_err_msg.format(
            idx,
            "candidate to drop",
            repr(actual_drop),
            "candidate to drop",
            repr(expected_rr["drop"]),
        )

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("city_run_election.json")
)
def test_city_run_election(test_params):
    test_num, params = test_params

    rmsg = RECREATE_MSG.format("City run_election", test_num)

    try:
        city = ranked_choice.mk_city_from_directory(
            params["city_name"], params["city_dir"]
        )
    except Exception as e:
        pytest.fail(EXCEPTION_MSG.format(type(e).__name__, e, "mk_city") + rmsg)

    if city is None:
        pytest.fail("Unable to construct city\n" + rmsg)

    try:
        vc = ranked_choice_student.ViableCandidates(params["cands_in_order"])
    except Exception as e:
        pytest.fail(
            CON_EXCEPTION.format("ViableCandidates", type(e).__name__, e) + rmsg
        )

    try:
        actual = city.run_election(vc)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "city run_election")
        pytest.fail(err_msg + rmsg)

    # Check None
    if actual is None:
        err_msg = (
            "Return value is None when a list of\n"
            "instances of RoundResults was expected"
        )
        pytest.fail(err_msg + rmsg)

    expected = params["expected"]

    # Check type
    if not isinstance(actual, type(expected)):
        err_msg = TYPE_MSG.format("return value", type(actual), type(expected))
        pytest.fail(err_msg + rmsg)

    # Check length
    if len(actual) != len(expected):
        pytest.fail(LEN_MSG.format("return value", len(actual), len(expected)) + rmsg)

    for idx, expected_rr in enumerate(expected):
        actual_rr = actual[idx]
        err_msg = check_round_results(idx, actual_rr, expected_rr)
        if err_msg:
            pytest.fail(err_msg + rmsg)

    # test passed
    return None
