"""Does an efference copy beat a generic estimator that sees the same stream?

The organ predicts the sensation its last act should have produced and broadcasts
the error. The rival is the organism's own Q-learner on the current observation,
the act just taken, and a short raw history of both, with the policy's step size,
discount, exploration and conjunctions. It has no forward model and no world
parameters. The act is forced, so the two arms face the same self-caused motion.
The margin is 0.04, half the 0.05 bar C037 sets for an optimal trace over a
moment judge: the learned copy has to capture at least half of the advantage
that bar treats as real. Forty-eight seeds, because a late-half gap of a few
points is not located by sixteen.
"""
from mind.claims import Claim, Compare

CLAIM = Claim(
    id="C038",
    title="An efference copy beats a matched estimator at attributing external impulses",
    statement="In poltergeist/dev, an organism with an efference organ attributes whether an external impulse "
              "was present more accurately than a generic state estimator given the same public observations, "
              "its own acts, rewards and outcomes, by more than 0.04.",
    kind="effect",
    scope="L2",
    question="H010",
    about=("efference",),
    depends_on=("K12", "C037"),
    extends=("C037", "mind/organs/efference.py", "mind/worlds/poltergeist.py"),
    test=Compare(world="poltergeist", a="organism +efference", b="rival:estimator", metric="attributed",
                 direction=">", margin=0.04, seeds=48),
    by="Cursor Agent",
    created="2026-10-11",
    rationale="H010. The rival is matched on information and on the learner, and unmatched on the forward "
              "model: that is the comparison. Scope is this organism in poltergeist/dev. Not a claim about "
              "phenomenal experience, and not a result that transfers to the Anjo product.",
)
