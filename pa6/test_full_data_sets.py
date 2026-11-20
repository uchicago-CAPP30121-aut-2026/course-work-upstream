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

from test_asqp import (
    task1a_helper,
    task1b_helper,
    task1c_helper,
    task1d_helper,
    task2_helper,
    task3a_helper,
    task3b_helper,
    task3c_helper,
)

DATA_DIR = "full_data_sets/"
TEST_DIR = "full_data_sets/"


def test_task1a():
    file_name = "full_data_sets/asqp.asc"
    expected = 63.77200407619861
    task1a_helper(file_name, expected)


def test_task1b():
    file_name = "full_data_sets/asqp.asc"
    expected_delays = 0.1873460363600532
    expected_cancels = 0.012289377740552792
    task1b_helper(file_name, expected_delays, expected_cancels)


def test_task1c():
    file_name = "full_data_sets/asqp.asc"
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
    task1c_helper(file_name, expected_cancellations, expected_worst)


def test_task1d():
    file_name = "full_data_sets/asqp.asc"
    expected_worst = set(["DL", "UA", "B6", "F9", "G4", "NK"])
    task1d_helper(file_name, expected_worst)


def test_task2_full():
    task2_helper(DATA_DIR + "delays.npy", TEST_DIR + "task3_delays.npy")


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
