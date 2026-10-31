"""
CAPP 30121: Ranked-choice elections revisited -- student test code

This file contains student-written test code.
"""

# These functions can be called without using their module names
# as qualifiers.  For example, read_ballots("ballot_files/ballots_0.txt").
from ranked_choice import read_ballots, mk_precinct, mk_city_from_directory

# The constructors for the classes in ranked_choice_student
# can be used without a qualified.
from ranked_choice_student import ViableCandidates, Ballot, Precinct, City

def test_viable_helper(cands_in_order):
    vc = ViableCandidates(cands_in_order)
    assert vc.get_num_viable() == len(cands_in_order)
    for cand in cands_in_order:
        assert vc.is_viable(cand)
    # a candidate name that is unlikely to occur
    name = "123xyz!@#"
    assert name not in cands_in_order and not vc.is_viable(name)
    assert vc.get_candidates_in_order() == tuple(cands_in_order)

    for cand in cands_in_order:
        new_vc = vc.drop(cand)
        assert isinstance(new_vc, ViableCandidates)
        # Do a check to see if the new candidate has the right
        # candidates. Make a list with all of the candidates except
        # the one that was dropped.
        new_cands = [c for c in cands_in_order if c != cand]
        assert new_vc.get_candidates_in_order() == tuple(new_cands)

    assert str(vc).split(",") == cands_in_order


def test_all_viable():
    test_viable_helper(["red", "green", "blue"])

if __name__ == "__main__":
    test_all_viable()
    # add calls to your test functions here.
