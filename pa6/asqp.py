"""
CAPP 30121: Airline Service Quality Performance (ASQP) data

Answer questions about airline performance data.
"""
import sys

import numpy as np
import pandas as pd

############## TASK1 1 TEST HELPER ##############

def get_task1_data(filename):
    """
    Load the data for Task 1 and extract NumPy arrays for the
     - carrier data: a NumPy array of strings;
     - time delay data: a NumPy array of integers
     - cancellation code data: a NumPy array of of strings

    Args:
        filename (str): the ASC file to load

    Returns (Tuple[NumPy array of str, NumPy array of int, NumPy array of str):
       a tuple with arrays for the carrier data, time delay data, and
       cancellation codes from the specified file.
    """
    try:
        df = pd.read_csv(filename, sep="|", low_memory=False)
    except FileNotFoundError:
        print(f"Error: File {filename} not found", sys.stderr)
        return None, None, None

    carrier = np.array(df["Marketing Carrier"], dtype=str)
    arrival_delay = np.array(df["Arrival Delay"], dtype='int64')
    cancellation_code = np.array(df["Cancellation Code"], dtype=str)
    return (carrier, arrival_delay, cancellation_code)


############## TASK1 1 ##############


def average_delay(arrival_delay):
    """
    Given ASQP data, determine the average flight delay

    Args:
        arrival_delay (NumPy array of integers): flight arrival times (negative
            if the flight is early, positive if the flight is late)

    Returns (float): the average delay of non-early flights
    """
    ### YOUR CODE HERE ###


def delay_and_cancel_fractions(arrival_delay, cancellation_code):
    """
    Given ASQP data, compute the fraction of delayed and cancelled flights

    Args:
        arrivals_time (NumPy array of integers): flight arrival times
        cancellation_code (NumPy array of strings): flight cancellation codes

    Returns (tuple of floats): fraction of flights that were delayed,
        fraction of flights that were cancelled
    """
    ### YOUR CODE HERE ###


def per_carrier_cancels(carrier, cancellation_code):
    """
    Given ASQP data, determine how many of each carrier's flights were
        cancelled, and which carrier cancelled the most flights

    Args:
        carrier (Numpy array of strings): the carrier for each fligh
        cancellation_code (NumPy array of strings): the flight cancellation code
          for each flight

    Returns (dictionary, string): a dictionary mapping a carrier to the number of
        cancelled flights, and the carrier with the most cancellations
    """
    ### YOUR CODE HERE ###


def underperforming_carriers(carrier, arrival_delay):
    """
    Given ASQP data, determine which carriers have a worse than average delay

    Args:
        carrier (Numpy array of strings): the carrier for each fligh
        arrivals_time (NumPy array of integers): flight arrival times

    Returns (Set[str]): carriers whose average delay is worse than the overall
        average delay
    """


############## TASK 2 ##############


def read_and_process_npy(filename):
    """
    Read in and process time series ASQP data

    Args:
        filename (string): name of the NPY file

    Returns (NumPy array): a time series NumPy array
    """
    ### YOUR CODE HERE ###


############## PART 2 HELPER FUNCTION ##############


### Do NOT modify this function
def perform_least_squares(y):
    """
    Given a data set, finds the line best fit perform least squares

    Args:
        y (array): data

    Returns (tuple of floats): the slope and y-intercept of the
        line fitted to y
    """

    x = np.arange(len(y))
    A = np.vstack([x, np.ones(len(y))]).T
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]

    return m, b


############## TASK 3 ##############


def remove_irregularities(ts, width):
    """
    Apply a smoothing technique to remove irregularities from the
        times series ASQP data

    Args:
        ts (NumPy array): the time series
        width (int): the width over which to smoothe

    Returns (NumPy array): smoothed time series data
    """
    ### YOUR CODE HERE ###


def remove_trend(ts, width):
    """
    Remove overall trend from time series ASQP data

    Args:
        ts (NumPy array): the time series
        width (int): the width over which to smoothe

    Returns (NumPy array): detrended time series data
    """
    ### YOUR CODE HERE ###


def is_seasonal(ts, width):
    """
    Bucket late flights, determine the bucket with the most
        late flights

    Args:
        ts (NumPy array): the time series
        width (int): the width over which to smoothe
        list_of_indices (lit of list of ints): something here

    Returns (NumPy array, int): number of delays in each month,
        the index of the month with the most delays (January = 0, etc.)
    """
    ### YOUR CODE HERE ###
