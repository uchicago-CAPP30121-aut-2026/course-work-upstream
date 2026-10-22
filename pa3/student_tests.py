"""
CAPP 30121: Ranked-choice elections -- student test code

This file contains student-written test code.
"""

# These functions can be called without using their module names
# as qualifiers.  For example, read_ballots("ballot_files/ballots_0.txt").
from test_ranked_choice_student import check_results_dict
from ranked_choice import read_ballots

# The functions in ranked_choice_student need to be called using
# ranked_choice_student as a qualifer.  For example,
# ranked_choice_student.run_election(...).
import ranked_choice_student

# Here's a sample run election test function.  You will want to expend
# significant effort into writing test functions for your helper
# functions.  This test function is included to help you understand
# how to use the provided functions.

def run_election_test1():
    ballots = read_ballots("ballot_files/ballots_2.txt")
    viable_cands = ["red", "yellow", "blue", "green"]
    actual_audit_trail = ranked_choice_student.run_election(ballots, viable_cands)

    expected_audit_trail = [
        {
            "round_num": 1,
            "vote_tally": {"red": 2, "blue": 1, "yellow": 2, "green": 1},
            "num_exhausted": 0,
            "viable_candidates": ["red", "yellow", "blue", "green"],
            "drop": "green",
        },
        {
            "round_num": 2,
            "vote_tally": {"red": 3, "blue": 1, "yellow": 2},
            "num_exhausted": 0,
            "viable_candidates": ["red", "yellow", "blue"],
            "drop": "blue",
        },
        {
            "round_num": 3,
            "vote_tally": {"red": 3, "yellow": 3},
            "num_exhausted": 0,
            "viable_candidates": ["red", "yellow"],
            "drop": "yellow",
        },
        {
            "round_num": 4,
            "vote_tally": {"red": 5},
            "num_exhausted": 1,
            "viable_candidates": ["red"],
            "winner": "red",
        },
    ]

    assert actual_audit_trail is not None, "Test failed: function returned None"
    assert isinstance(actual_audit_trail, list), (
        "Test failed: retrun value has the wrong type"
    )

    alen = len(actual_audit_trail)
    elen = len(expected_audit_trail)
    err_msg = (
        f"Test failed: the length of the acutal audit trail ({alen})\n"
        f"does not match the length of the expected audit trail ({elen})\n"
    )
    assert alen == elen, err_msg

    for idx, actual in enumerate(actual_audit_trail):
        expected = expected_audit_trail[idx]
        err_msg = check_results_dict(actual, expected)
        if err_msg:
            err_msg = f"Test failed for round {idx}\n" + err_msg
            assert False, err_msg


if __name__ == "__main__":
    run_election_test1()
    # add calls to your test functions here.
