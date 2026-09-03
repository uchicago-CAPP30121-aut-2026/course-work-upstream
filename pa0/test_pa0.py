"""
Programming Assignment #0: Automated test code
CAPP 30121
Autumn 2026
"""

import sys
import os
import helpers
import pytest

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

import pa0

MODULE = "pa0"

def test_two_plus_three():
    """
    Tests the two_plus_three function
    """
    recreate_msg = helpers.gen_recreate_msg(MODULE, "two_plus_three", *())
    try:
        actual = pa0.two_plus_three()
    except Exception as e:  # pylint: disable=broad-except
         helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, 5)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


def test_modify_file():
    """
    Tests if MODIFY_ME.md has been changed
    """
    original_contents="""Replace this line with any message of your choosing."""

    with open("MODIFY_ME.md", "r") as f:
        actual = f.read().strip()

    if actual == original_contents:
        pytest.fail("The file MODIFY_ME.md has not been modified. " + \
                    "Please modify it as instructed in the assignment.\n")


def test_create_folder():
    """
    Tests if the folder my_folder has been created and a file called my_file.txt
    has been created inside it.
    """
    if not os.path.isdir("my_folder"):
        pytest.fail("The folder my_folder has not been created. " + \
                    "Please create it as instructed in the assignment.\n")

    if not os.path.isfile("my_folder/my_file.txt"):
        pytest.fail("The file my_folder/my_file.txt has not been created. " + \
                    "Please create it as instructed in the assignment.\n")

    # Check if the file contains the string 'CAPP'
    expected_content = "CAPP"
    with open("my_folder/my_file.txt", "r") as f:
        actual_content = f.read().strip()

        if expected_content in actual_content:
            return  # Test passed
        else:
            err_msg = ("The file my_folder/my_file.txt does not contain the\n"
                        "expected content. Please ensure it contains the text"
                        "'CAPP' (in uppercase, anywhere in the document).\n")
            pytest.fail(err_msg)
