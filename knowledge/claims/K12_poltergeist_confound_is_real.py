"""The poltergeist confound is real: one sensation does not reveal its cause.

A previous world for this question was rejected because a single transition
exposed the hidden polarity and the external event was not actually aliased
with the act. This check fails if any (act, sensation) pair is possible for
only one polarity — including when the actuator did not slip — or for only one
answer to "was there an external impulse?", or if a private cause key appears
in an observation. It does not score any agent.
"""
from mind.claims import Check, Claim

_BANNED = ("polarity", "external", "slip", "cause", "label", "applied")


def instrument(ctx):
    from mind.worlds import make_world
    from mind.worlds.poltergeist import confound_problems, sensation
    problems = []
    for variant in ("dev", "gusty", "slippy"):
        problems.extend(confound_problems(variant))
    quiet = sensation(1, 1, False, 0)
    aliased = sensation(-1, 1, False, 2)
    if quiet != 1 or aliased != 1:
        problems.append(f"push alias is {quiet} vs {aliased}, expected 1 and 1")
    env = make_world("poltergeist", 0, "dev")
    obs = env.reset()
    for _ in range(48):
        leaked = [key for key in _BANNED if key in obs]
        if leaked:
            problems.append("observation leaked " + ",".join(leaked))
            break
        step = env.step(env.legal()[0] if env.phase == "act" else "no")
        obs = env.reset() if step.done else step.obs
    ok = not problems
    return {"verdict": "HOLDS" if ok else "FAILS", "robust": True, "problems": problems[:8],
            "summary": "dev, gusty and slippy: every act and clipped sensation is consistent with both "
                       "polarities, with and without a slip, and with both external-presence labels; "
                       "private cause keys stay out of the observation"
                       if ok else "confound broken: " + "; ".join(problems[:3])}


CLAIM = Claim(
    id="K12",
    title="Poltergeist aliases an act with an external impulse, and does not label the cause",
    statement="In every poltergeist variant, every pairing of a push or a pull with a clipped sensation is "
              "consistent with both hidden polarities even when the actuator does not slip, and with an "
              "external impulse being either present or absent; a push under opposite polarities can share "
              "one sensation while the impulse differs; private cause keys never appear in the observation.",
    kind="invariant",
    scope="instrument",
    question="H010",
    test=Check(instrument, seeds=0),
    extends=("mind/worlds/poltergeist.py",),
    by="Cursor Agent",
    created="2026-10-11",
    rationale="Test of the test for H010. If this fails, an attribution score is not evidence about "
              "self-caused versus external change.",
)
