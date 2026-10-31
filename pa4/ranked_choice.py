"""
ADD MODULE HEADER COMMENT
"""

import click
import csv
import random
import os
import sys

from ranked_choice_student import ViableCandidates, Ballot, Precinct, City


def read_ballots(ballot_filename, mentioned_candidates):
    """
    Read the ballots from a file.

    Args:
        ballot_filename (str): the name of the file containing the ballot

    Returns (List[List[str] | None]: a list of the ranked-choice ballots from
      the specified file or None, if an error was encountered.
    """
    if not os.path.isfile(ballot_filename):
        print(f"File {ballot_filename} does not exist", file=sys.stderr)
        return None

    ballots = []
    with open(ballot_filename) as f:
        for idx, fields in enumerate(csv.reader(f)):
            # preprocess the candidate names
            choices = [s.strip().lower() for s in fields]
            if "" in choices:
                print(
                    f"Error in line: {idx + 1}: empty candidate name - {choices}",
                    file=sys.stderr,
                )
                return None

            if len(choices) == 0:
                # ignore blank lines
                continue

            if mentioned_candidates is not None:
                mentioned_candidates.update(choices)
            ballots.append(Ballot(choices))

    return ballots


def mk_precinct(
    pid, ballot_filename=None, ranked_choice_lists=None, mentioned_candidates=None
):
    """
    Make a precinct using either the ballots from the specified
    file or the specified list of ranked_choice lists.

    Args:
        pid (str): the precinct's identifier
        ballot_filename (str): the name of a file containing ballots (optional)
        ranked_choice_lists (List[List[str]]: a list of ranked choice lists (optional)
        mentioned_candidates (Set(str)): a set to be filled with the candidates
          who are mentioned in the ballots

    Returns (Precinct | None): returns the precinct if it can
      be constructed successfully and None if an error is encountered.
    """
    assert (ballot_filename and not ranked_choice_lists) or (
        not ballot_filename and ranked_choice_lists
    )

    if ballot_filename:
        ballots = read_ballots(ballot_filename, mentioned_candidates)
        if not ballots:
            print(f"Unable to read ballot file: {ballot_filename}", sys.stderr)
            return None
    else:
        # strip strings in case a rogue candidate string ends up in a test ballot
        ballots = []
        for rc_list in ranked_choice_lists:
            ballots.append(Ballot([c.strip().lower() for c in rc_list]))

    return Precinct(pid, ballots)


def mk_city_from_directory(city_name, city_dir, mentioned_candidates=None):
    """
    Make a city using the ballots stored in the directory named city_name

    Args:
        city_name (str): the name of the city
        city_dir (str): the name of the directory containing the election
          files for the city.
        mentioned_candidates (Set[str]): a set that will be filled with the
          candidates mentioned in the ballots.

    Returns (City): the city loaded with the ballots
      or None if an error was encountered
    """
    if not os.path.isdir(city_dir):
        print(f"Directory {city_dir} does not exist", file=sys.stderr)
        return None

    precinct_filename = os.path.join(city_dir, "precincts.txt")
    if not os.path.isfile(precinct_filename):
        print(
            f"Directory {city_dir} does contain a precincts.txt file", file=sys.stderr
        )
        return None

    city = City(city_name)
    precinct_names = [pname.strip() for pname in open(precinct_filename)]
    for precinct_name in precinct_names:
        precinct_ballot_filename = os.path.join(city_dir, precinct_name)
        city.add_precinct(
            mk_precinct(
                precinct_name,
                ballot_filename=precinct_ballot_filename,
                mentioned_candidates=mentioned_candidates,
            )
        )

    return city


def process_viables(viable_candidates, seed, mentioned_candidates):
    if viable_candidates:
        if seed:
            print(
                "Error: only one of --viable or --seed should be specified.",
                file=sys.stderr,
            )
            sys.exit(2)
        viable_candidates = [c.strip().lower() for c in viable_candidates.split(",")]
        print("vc:", viable_candidates)
        if "" in viable_candidates:
            print("Error: the empty string is not a viable candidate", file=sys.stderr)
            sys.exit(3)
    else:
        if seed:
            random.seed(seed)
        viable_candidates = sorted(mentioned_candidates)
        random.shuffle(viable_candidates)
        print(f"Viable candidates: {repr(', '.join(viable_candidates))}")

    return viable_candidates


@click.command()
@click.option("-c", "--city-name", type=str, default=None)
@click.option("-d", "--city-dir", type=str)
@click.option("-v", "--viable-candidates", type=str)
@click.option("-a", "audit_type", type=str, default=None)
@click.option("-s", "--seed", type=int, default=None)
def cmd(city_name, city_dir, viable_candidates, audit_type, seed):
    if city_name is None:
        print("No parameters.  Assume code is being loaded.")
        return

    if not viable_candidates:
        mentioned_candidates = set()
    else:
        mentioned_candidates = None
    city = mk_city_from_directory(
        city_name, city_dir, mentioned_candidates=mentioned_candidates
    )
    if city is None:
        sys.exit(2)

    viable_candidates = process_viables(viable_candidates, seed, mentioned_candidates)
    viable = ViableCandidates(viable_candidates)

    if audit_type and audit_type not in ["long", "short", "l", "s"]:
        print(
            "Error: audit type (if specified) must be one of: long, l, short, or s.",
            file=sys.stderr,
        )
        sys.exit(1)

    audit_trail = city.run_election(viable)

    if audit_type:
        for round in audit_trail:
            audit_flag = audit_type == "long" or audit_type == "l"
            print(round.construct_audit_str(audit_flag))
    else:
        winner = audit_trail[-1].find_winner()
        if winner:
            print(f"Winner: {winner}")
        else:
            print("No winner")


if __name__ == "__main__":
    cmd()
