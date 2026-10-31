import os
import json
import pytest


# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")


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
