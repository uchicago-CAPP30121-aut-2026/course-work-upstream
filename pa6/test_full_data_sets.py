import numpy as np
import pandas as pd
import pickle

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

from test_asqp import task1a_helper

DATA_DIR = "full_data_sets/"
TEST_DIR = "full_data_sets/"


def test_task1a():
    file_name = "full_data_sets/asqp.asc"
    _, arrival_delay, _ = get_task1_data(file_name)
    if arrival_delay is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )

    actual = average_delay(arrival_delay)
    expected = 63.77200407619861
    assert np.isclose(actual, expected), (
        "Value returned by average_delay not as expected"
    )


def test_task1b():
    file_name = "full_data_sets/asqp.asc"

    _, arrival_delay, cancellation_code = get_task1_data(file_name)
    if arrival_delay is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )
    actual_delays, actual_cancels = delay_and_cancel_fractions(
        arrival_delay, cancellation_code
    )

    expected_delays = 0.1873460363600532
    expected_cancels = 0.012289377740552792
    assert np.isclose(actual_delays, expected_delays), (
        "Value returned by delay_and_cancel_fractions not as expected"
    )
    assert np.isclose(actual_cancels, expected_cancels), (
        "Value returned by delay_and_cancel_fractions not as expected"
    )


def test_task1c():
    file_name = "full_data_sets/asqp.asc"

    carrier, _, cancellation_code = get_task1_data(file_name)
    if carrier is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )

    actual_cancellations, actual_worst = per_carrier_cancels(carrier, cancellation_code)
    expected_cancellations = {
        "DL": 412,
        "AA": 4356,
        "AS": 459,
        "UA": 1554,
        "B6": 53,
        "HA": 33,
        "F9": 70,
        "G4": 62,
        "NK": 52,
        "WN": 931,
    }
    expected_worst = "AA"

    assert actual_cancellations == expected_cancellations, (
        "Value returned by per_carrier_cancels not as expected"
    )
    assert actual_worst == expected_worst, (
        "Value returned by per_carrier_cancels not as expected"
    )


def test_task1d():
    file_name = "full_data_sets/asqp.asc"
    carrier, arrival_delay, _ = get_task1_data(file_name)
    if carrier is None:
        assert False, (
            f"Error: Could not load {file_name}.\nAre you in the right directory?"
        )
    actual_worst = set(underperforming_carriers(carrier, arrival_delay))
    expected_worst = set(["DL", "UA", "B6", "F9", "G4", "NK"])

    assert actual_worst == expected_worst, (
        "Value returned by underperforming_carriers not as expected"
    )


def task2_helper(actual_filename, expected_filename):

    actual = read_and_process_npy(actual_filename)
    expected = np.load(expected_filename)

    assert np.array_equal(actual, expected), (
        "Array returned by read_and_process_npy not as expected"
    )


def test_task2_full():
    task2_helper(DATA_DIR + "delays.npy", TEST_DIR + "task3_delays.npy")


def task3a_helper(actual_filename, expected_filename, w):

    ts = np.load(actual_filename)
    actual = remove_irregularities(ts, w)
    expected = np.load(expected_filename)

    assert np.isclose(actual, expected).all(), (
        "Array returned by remove_irregularities not as expected"
    )


def test_task3a_full_0():

    w = 1
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4a_delays_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def test_task3a_full_1():

    w = 2
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4a_delays_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def test_task3a_full_2():

    w = 3
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4a_delays_w" + str(w) + ".npy"
    task3a_helper(actual_filename, expected_filename, w)


def task3b_helper(actual_filename, expected_filename, w):

    ts = np.load(actual_filename)
    actual = remove_trend(ts, w)
    expected = np.load(expected_filename)

    assert np.isclose(actual, expected).all(), (
        "Array returned by remove_irregularities not as expected"
    )


def test_task3b_full_0():

    w = 1
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4b_delays_w" + str(w) + ".npy"
    task3b_helper(actual_filename, expected_filename, w)


def test_task3b_full_1():

    w = 2
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4b_delays_w" + str(w) + ".npy"
    task3b_helper(actual_filename, expected_filename, w)


def test_task3b_full_2():

    w = 1
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4b_delays_w" + str(w) + ".npy"
    task3b_helper(actual_filename, expected_filename, w)


def task3c_helper(actual_filename, expected_filename, w, expected_month):

    ts = np.load(actual_filename)
    actual_buckets, actual_month = is_seasonal(ts, w)
    expected_buckets = np.load(expected_filename)

    assert np.isclose(actual_buckets, expected_buckets).all(), (
        "Array returned by is_seasonal not as expected"
    )
    assert actual_month == expected_month, (
        "Month returned by is_seasonal not as expected"
    )


def test_task3c_0():

    w = 1
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4c_delays_w" + str(w) + ".npy"
    expected_month = 6

    task3c_helper(actual_filename, expected_filename, w, expected_month)


def test_task3c_1():

    w = 2
    actual_filename = DATA_DIR + "task3_delays.npy"
    expected_filename = DATA_DIR + "task4c_delays_w" + str(w) + ".npy"
    expected_month = 6

    task3c_helper(actual_filename, expected_filename, w, expected_month)
