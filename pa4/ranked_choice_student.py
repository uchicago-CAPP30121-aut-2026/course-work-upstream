"""
CAPP 30121: Ranked-choice elections -- student code

Student code for PA #4 goes in this file.
"""

import math


class ViableCandidates:
    """
    A class for representing the viable candidates
    """

    def __init__(self, candidates_in_order):
        """
        ViableCandidates constructor

        Args:
            canidates_in_order (List[str]): a list of the candidates in
              order by their drop position. (Later candidates get
              dropped first.)
        """
        ### Your code here

    def get_num_viable(self):
        """
        Returns (int): the number of candidates
        """

        ### Your code here

    def is_viable(self, candidate):
        """
        Is the specified candidate viable?

        Args:
            candidate (str): the name of the candidate to check

        Returns (bool): True if the specified candidate is viable and
          False otherwise.
        """
        ### Your code here

    def get_candidates_in_order(self):
        """
        Returns (Tuple[str]): a tuple with the candidates in order
        """
        ### Your code here

    def drop(self, drop_candidate):
        """
        Drop a known candidate.

        Args:
            candidate (str): the name of the candidate to drop

        Raises:
            Assertion error: if the specified candidate is not viable.

        Returns (ViableCandidates): a new instance of ViableCandidates
          without the specified candidate.
        """
        ### Your code here

    def __str__(self):
        """
        Returns (str): comma separated string with the candidates
          in order by drop position.
        """
        ### Your code here


class Ballot:
    """
    A class for representing a voter's ranked choice ballot
    """

    def __init__(self, ranked_choice_vote):
        """
        Ballot constructor

        Args:
            ranked_choice_vote (List[str]): the voter's choices in
              in order of preference
        """
        ### Your code here

    def find_first_viable(self, viable):
        """
        Find the first viable candidate in the voter's ranked
        choice ballot

        Args:
            viable (ViableCandidates): the candidates who are
              currently viable

        Returns (str | None): returns the first viable candidate in
          the voter's ballot or None, if the ballot does not contains
          a viable candidate.
        """
        ### Your code here

    def __str__(self):
        """
        Returns (str): comma separated string with the voter's choices in order.
        """
        ### Your code here


class Precinct:
    """
    A class for representing the votes cast in a precinct.
    """

    def __init__(self, pid, ballots):
        """
        Precinct constructor

        Args:
            pid (str): the precinct's identifier
            ballots (List[Ballot]): a list of the ballots cast in the
              precinct.
        """
        ### Your code here

    def run_round(self, viable):
        """
        Run a single round of voting for the precinct using the specified
        viable candidates.

        Args:
            viable (ViableCandidates): the candidates who are
              currently viable

        Returns (Tuple[Dict[str, int], int)]: return a pair with a dictionary
          that maps a candidate's name to the number of votes received by the
          candidate in this round (at this precinct) and the number of ballots
          that are exhausted.
        """
        ### Your code here

    def __str__(self):
        """
        See assignment writeup for a description of the required
        format.
        """
        ### Your code here


class RoundResults:
    """
    A class for representing the results from running round in
    a ranked-choice election.
    """

    def __init__(self, round_num, viable):
        """
        RoundResult Constuctor

        Args:
            round_num (int): the number of the round.
            viable (ViableCandidates): the candidates who are
              viable at the start of this round.
        """
        ### Your code here

    def add_precinct_results(self, pid, vote_tally, num_exhausted_ballots):
        """
        Add the results for a precinct into the results for the round.

        Args:
            pid (str): the precinct identifier
            vote_tally (Dict[str, int]): a dictionary that maps a candidate's
              name to the number of votes the candidate received in the round
            num_exhausted_ballots (int): the number of exhausted ballots
              encountered in the round.
        """
        ### Your code here

    def are_all_exhausted(self):
        """
        Are all the ballots exhausted?

        Return (bool): True, there are no available votes,
          False otherwise.
        """
        ### Your code here

    def find_winner(self):
        """
        Determine the winner of the round

        Raises:
            AssertionError: if called when all the ballots are exhausted

        Returns (str | None): the name of the winner or None, if no
          candidate meets the winning threshold (50% + 1).
        """
        ### Your code here

    def find_cand_to_drop(self):
        """
        Determine which candidate to drop

        Raises:
            AssertionError: if called when all the ballots are exhausted or
              when there is a winner.

        Returns (str): the name of the candidate with the fewest votes. Break
          ties based on the order specified for the candidates.
        """
        ### Your code here

    def construct_audit_str(self, long_form):
        # ruff: disable[F841] -- ignore unused variables for the templates.

        # Use this template to create the string for the round
        # - First argument is for the round number
        # - Second argument is for the per-precinct results
        #   (long-form audit only)
        # - Third argument is for the overall vote tally
        #   (see below for the vote tally format)
        # - Fourth argument is for the overall number of exhausted ballots
        round_results_template = (
            "=" * 15 + " Round {} " + "=" * 15 + "\n"
            "{}"
            "Overall:\n  Vote Tally:\n{}\n"
            "  Number of Exhausted Ballots: {}\n\n"
        )

        # Use this template to create the string for the results for a precinct,
        # if needed.
        # - First argument is for the precinct identifier
        # - Second argument is for a string constructed from the precinct's
        #   vote tally
        # - Third argument is the number of exhausted ballots
        precinct_template = (
            "Precinct {}:\n"
            "  Vote Tally:\n{}\n" + "  Number of exhausted ballots: {}\n\n"
        )

        # Use this template for a single candidate's entry in the tally
        # - First argument is the name of the candidate
        # - second argument is the number of votes the candidate received
        # - the third argument is the optional tag (see below)
        single_cand_tally_str = "    {}: {}{}\n"

        # Tags to add to a candidates string (do not include any extra spaces
        # before the tag
        drop_tag = "\t(drop)"
        winner_tag = "\t(winner)"
        no_tag = ""

        # ruff: enable[F841] -- reenable checking unused variables

        ### Your code here


class City:
    """
    A class for representing an election for a city.
    """

    def __init__(self, city_name):
        """
        City constructor

        Args:
            city_name (str): the name of the city
        """
        ### Your code here

    def add_precinct(self, precinct):
        """
        Add a precinct to the city.

        Args:
            precinct (Precinct): the precinct to add
        """
        ### Your code here

    def run_election(self, viable):
        """
        Run the election for the city using the specified
        list of viable candidates.

        Args:
            viable (ViableCandidates): the candidates who are
              viable at the start of the election

        Returns (List[RoundResults]): a list of results for each
          round in the election.
        """
        ### Your code here
