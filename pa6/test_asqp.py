import numpy as np
import pandas as pd
import pickle
import pytest

# import student code
from asqp import (
    get_task1_data,
    average_delay,
    delay_and_cancel_fractions,
    per_carrier_cancels,
    underperforming_carriers,
    read_and_process_npy,
    remove_irregularities,
    remove_trend,
    is_seasonal,
)

# might need a helper to compare dfs
DATA_DIR = "data/"
TEST_DIR = "test-data/"

EXCEPTION_MSG = (
    "An unexpected exception:\n\n"
    "  {}: {}\n\n"
    "was raised in the {} method and is causing your code\n"
    "to fail. This behavior is likely due to a bug in your code.\n"
)

NONE_MSG = (
    "The method returned None when a {} was expected.\n"
    "Did you forget to include a return statement?\n"
)


######### Testing Part 1: DELAYS AND CANCELLATIONS #########

def task1a_helper(file_name, expected):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import asqp\n"
        f"    _, arrival_delay, _ = asqp.get_task1_data({repr(file_name)})\n"
        "    actual = asqp.average_delay(arrival_delay)\n"
        f"    expected = {expected}\n"
        "    # To check the actual value run: np.isclose(actual, expected)\n"
    )

    _, arrival_delay, _ = get_task1_data(file_name)
    if arrival_delay is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )

    try:
        actual = average_delay(arrival_delay)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "average_delay")
        pytest.fail(err_msg + recreate_msg)

    if actual is None:
        pytest.fail(NONE_MSG.format("floating point value") + recreate_msg)

    assert np.isclose(actual, expected), (
        "Value returned by average_delay not as expected" + recreate_msg
    )

def test_task1a_0():
    task1a_helper("data/tiny.asc", 86.0)


def test_task1a_1():
    task1a_helper("data/tiny_all_delayed.asc", 62.5)


def task1b_helper(file_name, expected_delays, expected_cancels):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import asqp\n"
        f"    _, arrival_delay, cancellation_code = asqp.get_task1_data({repr(file_name)})\n"
        "    actual_delays, actual_cancels = asqp.delay_and_cancel_fractions(arrival_delay, cancellation_code)\n"
        f"    expected_delays = {expected_delays}\n"
        "    # to check expected delays: np.isclose(actual_delays, expected_delays)\n"
        f"    expected_cancels = {expected_cancels}\n"
        "    # to check expected delays: np.isclose(actual_cancels, expected_cancels)\n"
    )

    _, arrival_delay, cancellation_code = get_task1_data(file_name)
    if arrival_delay is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )

    try:
        actual = delay_and_cancel_fractions(arrival_delay, cancellation_code)
        if actual is None:
            pytest.fail(NONE_MSG.format("tuple") + recreate_msg)
        actual_delays, actual_cancels = actual
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(
            type(e).__name__, e, "delay_and_cancel_fractions"
        )
        pytest.fail(err_msg + recreate_msg)

    assert np.isclose(actual_delays, expected_delays), (
        "Value returned by delay_and_cancel_fractions not as expected\n\n"
        + recreate_msg
    )
    assert np.isclose(actual_cancels, expected_cancels), (
        "Value returned by delay_and_cancel_fractions not as expected\n\n"
        + recreate_msg
    )


def test_task1b_0():
    task1b_helper("data/tiny.asc", 0.2, 0.1)


def test_task1b_1():
    task1b_helper("data/tiny_all_on_time.asc", 0.0, 0.0)


def test_task1b_2():
    task1b_helper("data/tiny_all_delayed.asc", 1.0, 0.0)


def test_task1b_3():
    task1b_helper("data/tiny_all_cancelled.asc", 0.0, 1.0)


def task1c_helper(file_name, expected_cancellations, expected_worst):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import asqp\n"
        f"    carrier, _, cancellation_code = asqp.get_task1_data({repr(file_name)})\n"
        "    actual_cancellations, actual_worst = asqp.per_carrier_cancels(carrier, cancellation_code)\n"
        f"    expected_worst = {repr(expected_worst)}\n"
        "    # to check expected worst: actual_worst == expected_worst\n"
        f"    expected_cancellations = {expected_cancellations}\n"
        "    # to check expected cancellations: actual_cancellations == expected_cancellations\n"
    )

    carrier, _, cancellation_code = get_task1_data(file_name)
    if carrier is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )

    try:
        actual = per_carrier_cancels(carrier, cancellation_code)
        if actual is None:
            pytest.fail(NONE_MSG.format("tuplea") + recreate_msg)
        actual_cancellations, actual_worst = actual
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "per_carrier_cancels")
        pytest.fail(err_msg + recreate_msg)

    assert actual_cancellations == expected_cancellations, (
        "Value returned by per_carrier_cancels not as expected"
    )
    assert actual_worst == expected_worst, (
        "Value returned by per_carrier_cancels not as expected"
    )


def test_task1c_0():
    task1c_helper(
        "data/tiny.asc", {"AA": 0, "WN": 0, "DL": 0, "B6": 0, "UA": 0, "AS": 1}, "AS"
    )


def test_task1c_1():
    task1c_helper(
        "data/tiny_all_cancelled.asc",
        {"WN": 3, "AA": 3, "UA": 2, "DL": 1, "AS": 1},
        "AA",
    )


def task1d_helper(file_name, expected_worst):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import asqp\n"
        f"    carrier, arrival_delay, _ = asqp.get_task1_data({repr(file_name)})\n"
        "    actual_worst = asqp.underperforming_carriers(carrier, arrival_delay)\n"
        f"    expected_worst = {set(expected_worst)}\n"
        "    # to check expected worst: actual_worst == expected_worst\n"
    )

    carrier, arrival_delay, _ = get_task1_data(file_name)
    if carrier is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )

    try:
        actual_worst = underperforming_carriers(carrier, arrival_delay)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "per_carrier_cancels")
        pytest.fail(err_msg + recreate_msg)

    if actual_worst is None:
        pytest.fail(NONE_MSG.format("set of strings") + recreate_msg)

    assert actual_worst == set(expected_worst), (
        "Value returned by underperforming_carriers not as expected"
    )


def test_task1d_0():
    task1d_helper("data/tiny.asc", ["WN"])


def test_task1d_1():
    task1d_helper("data/tiny_all_delayed.asc", ["AA", "WN", "DL"])


######### Testing Part 2: READING NPY FILE #########


def task2_helper(actual_filename, expected_filename):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import numpy as np\n"
        "    import asqp\n"
        f"    actual = asqp.read_and_process_npy({repr(actual_filename)})\n"
        f"    expected = np.load({repr(expected_filename)})\n"
        "    # to cehck the actual value run: np.array_equal(actual, expected)\n"
    )

    try:
        actual = read_and_process_npy(actual_filename)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "read_and_process_npy")
        pytest.fail(err_msg + recreate_msg)

    expected = np.load(expected_filename)

    if actual is None:
        pytest.fail(NONE_MSG.format("Numpy array") + "\n\n" + recreate_msg)

    assert np.array_equal(actual, expected), (
        "Array returned by read_and_process_npy not as expected\n\n" + recreate_msg
    )


def test_task2_0():
    task2_helper(DATA_DIR + "delays_tiny1.npy", TEST_DIR + "task3_delays_tiny1.npy")


def test_task2_1():
    task2_helper(DATA_DIR + "delays_tiny2.npy", TEST_DIR + "task3_delays_tiny2.npy")


######### Testing Part 2: TIME SERIES #########


def task3a_helper(actual_filename, expected_filename, w):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import numpy as np\n"
        "    import asqp\n"
        f"    ts = np.load({repr(actual_filename)})\n"
        f"    actual = asqp.remove_irregularities(ts, {w})\n"
        f"    expected = np.load({repr(expected_filename)})\n"
        "    # to check the actual value run: np.isclose(actual, expected).all()\n"
    )

    ts = np.load(actual_filename)
    try:
        actual = remove_irregularities(ts, w)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "remove_irregularities")
        pytest.fail(err_msg + recreate_msg)

    if actual is None:
        pytest.fail(NONE_MSG.format("Numpy array") + "\n\n" + recreate_msg)

    expected = np.load(expected_filename)
    assert np.isclose(actual, expected).all(), (
        "Array returned by remove_irregularities not as expected\n\n" + recreate_msg
    )


def test_task3a_0():

    w = 1
    actual_filename = "test-data/task3_delays_tiny1.npy"
    expected_filename = "test-data/task4a_delays_tiny1_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def test_task3a_1():

    w = 2
    actual_filename = "test-data/task3_delays_tiny1.npy"
    expected_filename = "test-data/task4a_delays_tiny1_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def test_task3a_2():

    w = 3
    actual_filename = "test-data/task3_delays_tiny1.npy"
    expected_filename = "test-data/task4a_delays_tiny1_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def test_task3a_3():

    w = 1
    actual_filename = "test-data/task3_delays_tiny2.npy"
    expected_filename = "test-data/task4a_delays_tiny2_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def test_task3a_4():

    w = 2
    actual_filename = "test-data/task3_delays_tiny2.npy"
    expected_filename = "test-data/task4a_delays_tiny2_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def test_task3a_5():

    w = 3
    actual_filename = "test-data/task3_delays_tiny2.npy"
    expected_filename = "test-data/task4a_delays_tiny2_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def task3b_helper(actual_filename, expected_filename, w):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import numpy as np\n"
        "    import asqp\n"
        f"    ts = np.load({repr(actual_filename)})\n"
        f"    actual = asqp.remove_trend(ts, {w})\n"
        f"    expected = np.load({repr(expected_filename)})\n"
        "    # to check the actual value run: np.isclose(actual, expected).all()\n"
    )

    ts = np.load(actual_filename)
    try:
        actual = remove_trend(ts, w)
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "remove_trend")
        pytest.fail(err_msg + recreate_msg)

    if actual is None:
        pytest.fail(NONE_MSG.format("Numpy array") + "\n\n" + recreate_msg)

    expected = np.load(expected_filename)
    assert np.isclose(actual, expected).all(), (
        "Array returned by remove_irregularities not as expected\n\n" + recreate_msg
    )


def test_task3b_0():

    w = 1
    actual_filename = "test-data/task3_delays_tiny1.npy"
    expected_filename = "test-data/task4b_delays_tiny1_w" + str(w) + ".npy"
    task3b_helper(actual_filename, expected_filename, w)


def test_task3b_1():

    w = 2
    actual_filename = "test-data/task3_delays_tiny1.npy"
    expected_filename = "test-data/task4b_delays_tiny1_w" + str(w) + ".npy"
    task3b_helper(actual_filename, expected_filename, w)


def test_task3b_2():

    w = 1
    actual_filename = "test-data/task3_delays_tiny2.npy"
    expected_filename = "test-data/task4b_delays_tiny2_w" + str(w) + ".npy"
    task3b_helper(actual_filename, expected_filename, w)


def test_task3b_3():

    w = 2
    actual_filename = "test-data/task3_delays_tiny2.npy"
    expected_filename = "test-data/task4b_delays_tiny2_w" + str(w) + ".npy"
    task3b_helper(actual_filename, expected_filename, w)


def task3c_helper(actual_filename, expected_filename, w, expected_month):
    recreate_msg = (
        "To recreate this test, run the following in ipython:\n"
        "    import numpy as np\n"
        "    import asqp\n"
        f"    ts = np.load({repr(actual_filename)})\n"
        f"    actual_buckets, actual_month = asqp.is_seasonal(ts, {w})\n"
        f"    expected_buckets = np.load({repr(expected_filename)})\n"
        "    # to check the expected bucket values run: np.isclose(actual_buckets, expected_buckets).all()\n"
        f"    expected_month = {expected_month}\n"
        "    # to check the expected month run: actual_month == expected_month\n"
    )

    ts = np.load(actual_filename)
    try:
        actual = is_seasonal(ts, w)
        if actual is None:
            pytest.fail(NONE_MSG.format("tuple") + "\n\n" + recreate_msg)
        actual_buckets, actual_month = actual
    except Exception as e:
        err_msg = EXCEPTION_MSG.format(type(e).__name__, e, "is_seasonal")
        pytest.fail(err_msg + recreate_msg)

    expected_buckets = np.load(expected_filename)
    assert np.isclose(actual_buckets, expected_buckets).all(), (
        "Array returned by is_seasonal not as expected\n\n"
        + recreate_msg
        + "    # to check the buckets run: np.isclose(actual_buckets, expected_buckets).all()\n"
    )
    assert actual_month == expected_month, (
        "Month returned by is_seasonal not as expected\n\n"
        + recreate_msg
        + "    # to check the month run: actual_month == expected_month\n"
    )


def test_task3c_0():

    w = 1
    actual_filename = "test-data/task3_delays_tiny1.npy"
    expected_filename = "test-data/task4c_delays_tiny1_w" + str(w) + ".npy"
    expected_month = 0

    task3c_helper(actual_filename, expected_filename, w, expected_month)


def test_task3c_1():

    w = 2
    actual_filename = "test-data/task3_delays_tiny1.npy"
    expected_filename = "test-data/task4c_delays_tiny1_w" + str(w) + ".npy"
    expected_month = 0

    task3c_helper(actual_filename, expected_filename, w, expected_month)


def test_task3c_2():

    w = 1
    actual_filename = "test-data/task3_delays_tiny2.npy"
    expected_filename = "test-data/task4c_delays_tiny2_w" + str(w) + ".npy"
    expected_month = 2

    task3c_helper(actual_filename, expected_filename, w, expected_month)


def test_task3c_3():

    w = 2
    actual_filename = "test-data/task3_delays_tiny2.npy"
    expected_filename = "test-data/task4c_delays_tiny2_w" + str(w) + ".npy"
    expected_month = 2

    task3c_helper(actual_filename, expected_filename, w, expected_month)
