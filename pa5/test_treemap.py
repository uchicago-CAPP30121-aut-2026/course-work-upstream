import json
import pytest
import os
import sys

# get the student's code from the current directory
# not from the directory the test file lives in
sys.path.insert(0, ".")

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

import atus
import helpers
import treemap
from treenode import TreeNode


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


def check_tree_weights(tree, expected_weights):
    weight_err_msg = (
        "The weight of the node with code {} does not match the expected value\n"
        "  Actual weight: {}\n"
        "  Expected weight: {}\n"
    )

    expected_weight = expected_weights.get(tree.code, 0)
    if tree.weight != expected_weight:
        return weight_err_msg.format(repr(tree.code), tree.weight, expected_weight)

    for kid in tree.get_children_as_list():
        err_msg = check_tree_weights(kid, expected_weights)
        if err_msg:
            return err_msg

    # Test passed.
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("compute_weights.json")
)
def test_compute_tree_weights(test_params):
    test_num, params = test_params
    if params["prefix"]:
        part_tree = atus.load_participant(
            params["part_num"], time_code=params["prefix"]
        )
        load_str = (
            f"atus.load_participant({params['part_num']}, "
            f"time_code = {repr(params['prefix'])})\n"
        )
    else:
        part_tree = atus.load_participant(params["part_num"])
        load_str = f"atus.load_participant({params['part_num']})\n"

    rmsg = (
        "\n\nTo recreate this test, run:\n"
        "    import treemap, atus\n"
        f"    part_tree = {load_str}"
        "    actual = treemap.compute_weights(part_tree)\n"
    )

    try:
        actual = treemap.compute_weights(part_tree)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "compute_weights") + rmsg
        pytest.fail(err_msg + rmsg)

    err_msg = check_return_value(actual, params["expected_return_value"])
    if err_msg:
        pytest.fail(err_msg + rmsg)

    err_msg = check_tree_weights(part_tree, params["expected_weights"])
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("collect_codes.json")
)
def test_collect_codes(test_params):
    test_num, params = test_params
    if params["prefix"]:
        part_tree = atus.load_participant(
            params["part_num"], time_code=params["prefix"]
        )
        load_str = (
            f"atus.load_participant({params['part_num']}, "
            f"time_code = {repr(params['prefix'])})\n"
        )
    else:
        part_tree = atus.load_participant(params["part_num"])
        load_str = f"atus.load_participant({params['part_num']})\n"

    rmsg = (
        "\n\nTo recreate this test, run:\n"
        "    import treemap, atus\n"
        f"    part_tree = {load_str}"
        "    actual = treemap.collect_codes(part_tree)\n"
    )

    try:
        actual = treemap.collect_codes(part_tree)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "collect_codes") + rmsg
        pytest.fail(err_msg + rmsg)

    err_msg = check_return_value(actual, set(params["expected_return_value"]))
    if err_msg:
        pytest.fail(err_msg + rmsg)

    # test passed
    return None


@pytest.mark.parametrize(
    ("test_params"), helpers.read_config_file("compute_treemap_rectangles.json")
)
def test_compute_treemap_rectangles(test_params):
    test_num, params = test_params
    if params["prefix"]:
        part_tree = atus.load_participant(
            params["part_num"], time_code=params["prefix"]
        )
        load_str = (
            f"atus.load_participant({params['part_num']}, "
            f"time_code = {repr(params['prefix'])})\n"
        )
    else:
        part_tree = atus.load_participant(params["part_num"])
        load_str = f"atus.load_participant({params['part_num']})\n"

    rmsg = (
        "\n\nTo recreate this test, run:\n"
        "    import treemap, atus\n"
        f"    part_tree = {load_str}"
        "    treemap.compute_weights(part_tree)\n"
        "    rects = treemap.compute_treemap_rectangles(part_tree)\n\n"
    )

    # set the weights first!
    try:
        actual = treemap.compute_weights(part_tree)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "compute_weights") + rmsg
        pytest.fail(err_msg + rmsg)

    try:
        actual = treemap.compute_treemap_rectangles(
            part_tree, params["height"], params["width"]
        )
    except Exception as e:
        err_msg = (
            EXCEPTION_MSG.format(type(e).__name__, e, "compute_treemap_rectangles")
            + rmsg
        )
        pytest.fail(err_msg + rmsg)

    expected = params["expected_return_value"]

    # Test failed: what is wrong with the actual value?
    if actual is None:
        pytest.fail(NONE_MSG.format("value of type List[Rectangle]") + rmsg)

    if not isinstance(actual, list):
        # Return value has the wrong type
        pytest.fail(TYPE_MSG.format("return value", type(actual), list) + rmsg)

    if len(actual) != len(expected):
        pytest.fail(LEN_MSG.format("return value", len(actual), len(expected)) + rmsg)

    for idx, e_val in enumerate(expected):
        e_val = eval(e_val)
        a_val = actual[idx]
        if e_val != a_val:
            pytest.fail(
                f"The function returned the wrong value.\n"
                f"The first difference is at index {idx}\n"
                f"  Actual value at index {idx}: \n    {repr(a_val)}\n"
                f"  Expected value at index {idx}: \n    {repr(e_val)}\n" + rmsg
            )

    # test passed
    return None
