"""
CS 121: Ranked-choice elections -- student code

Student code for PA #3 goes in this file.
"""

import math


### Add your helper functions here or after mk_round_results_str


def run_election(ballots, viable_candidates_ordered):
    """
    Run the election using the specified ballots and the specified
    list of viable candidates.

    Args:
        ballots (List[List[str]]): a list of the ballots cast during the election
        viable_candidates_ordered (List[str]): a list of the
          candidates who are considered viable at the start of the
          election.

    Returns (List[Dict[str, Any]]): a list of the results for each round
    """

    ### Your code here.
    ### Replace None with a suitable return value.
    return None


#### START: DO NOT MODIFY THIS CODE
# Templates for construction the string for a round result.

# Use this template to create the string for a round
# - First argument is for the round number
# - Second argument is for a string constructed from the tally dictionary
# - Third argument is the number of exhausted ballots
ROUND_RESULT_STR = (
    "=" * 15
    + " Round {} "
    + "=" * 15
    + "\n"
    + "  Vote Tally:\n{}\n"
    + "  Number of exhausted ballots: {}\n"
)

# Use this template for a single candidate's entry in the tally
# - First argument is the name of the candidate
# - second argument is the number of votes the candidate received
# - the third argument is the tag (see below)
SINGLE_CAND_TALLY_STR = "    {}: {}{}\n"

DROP_TAG = "\t(drop)"
WINNER_TAG = "\t(winner)"
NO_TAG = ""

#### END: DO NOT MODIFY THIS CODE


def mk_round_results_str(round_results):
    """
    Construct a string for the audit trail for a round.

    Args:
        round_results (Dict[str, Any]): a dictionary that contains the
          results for a round.

    Returns (str): a string suitable for printing as part of an
      audit trail.
    """
    ### Your code here.

    ### Replace "" with a suitable return value.
    return None
