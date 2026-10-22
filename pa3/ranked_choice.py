"""
CAPP 30121: Ranked-choice elections -- command-line interface

The program runs a rank-choice election for a single precinct.  It has
one required parameter:

- the name of a ballot file

and three optional parameters,

- viable (-v or --viable): a comma-separated string with the name of candidates who
  should be considered viable,
- seed (-s or --seed): a value to use as the random seed when shuffling the list
  of candidates, and
- audit flag (-a or --audit): a flag to signal whether an audit trail of the election
  should be printed.

Only one of viable and seed may be specified.

Sample uses:

$ uv run python3 ranked_choice.py ballot_files/ballots_0.txt
Viable-candidate order: "red, green, blue, yellow"
Winner after 3 rounds: yellow

$ uv run python3 ranked_choice.py ballot_files/ballots_0.txt -s 14003
Viable-candidate order: "green, red, blue, yellow"
Winner after 3 rounds: yellow

$ uv run python3 ranked_choice.py ballot_files/ballots_0.txt -v  "red,blue,green" -a
... audit trail...
"""

import click
import csv
import os
import random
import sys

import ranked_choice_student

def read_ballots(ballot_filename):
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
                print(f"Error in line: {idx + 1}: empty candidate name - {choices}",
                      file=sys.stderr)
                return None

            if len(choices) == 0:
                # ignore blank lines
                continue

            ballots.append(choices)

    return ballots


def find_mentioned_candidates(ballots):
    """
    Find the candidates mentioned in a set of ballots.

    Args:
        ballots (List[List[str]]): a list of ranked-choice ballots

    Returns (Set(str)): a set with the candidates mentioned in the ballots
    """
    cands = set()
    for ballot in ballots:
        cands.update(ballot)
    return cands


@click.command()
@click.argument("filename", type=str)
@click.option("-v", "--viable", type=str, default=None)
@click.option("-s", "--seed", type=int, default=None)
@click.option("-a", "--audit_flag", is_flag=True)
def cmd(filename, viable, seed, audit_flag):
    ballots = read_ballots(filename)
    if ballots is None:
        # An error was encountered when reading the ballots
        sys.exit(1)

    if viable:
        if seed:
            print("Error: only one of viable or seed should be specified.",
                  file=sys.stderr)
            sys.exit(2)
        # preprocess the candidate names
        viable_candidates = \
            [c.strip().lower() for c in viable.split(",")]
        if "" in viable_candidates:
            print("Error: the empty string is not a viable candidate",
                  file=sys.stderr)
            sys.exit(3)
    else:
        if seed:
            random.seed(seed)
        viable_candidates = sorted(find_mentioned_candidates(ballots))
        random.shuffle(viable_candidates)
        print(f'Viable candidates: "{", ".join(viable_candidates)}"')

    audit_trail = ranked_choice_student.run_election(ballots, viable_candidates)
    assert audit_trail and len(audit_trail) > 0, \
        "The return value from run_election must be a non-empty list."

    if audit_flag:
        for round in audit_trail:
            print(ranked_choice_student.mk_round_results_str(round))
    else:
        round_str = "round" if len(audit_trail) == 1 else "rounds"
        if "winner" in audit_trail[-1]:
            winner = audit_trail[-1]["winner"]
            print(f"Winner after {len(audit_trail)} {round_str}: {winner}")
        else:
            print(f"Election ended without a winner after {len(audit_trail)}"
                  f" {round_str}.")


if __name__ == "__main__":
    cmd()
