"""H013 causal action-report experiment on MIND's existing organism/worlds.

No separate agent or world is constructed. The two readouts see identical
public data; only the grounded readout additionally sees selected workspace
tags. Both are trained on identical labels, then frozen for evaluation.
"""
from __future__ import annotations

import hashlib
import json

from ..kernel import Organism
from ..worlds import make_world
from .report_readout import Decoder, PublicTranscript


def run_report_probe(world, variant, seed, episodes=180, train_episodes=120,
                     cut=False):
    """Return paired prequential action-Brier scores for one lifetime.

    The optional access cut starts after training, while selected workspace
    content remains reportable. The readouts do not see the current action
    until after forecasting. Private world info is never used.
    """
    if not 0 < train_episodes < episodes:
        raise ValueError("require 0 < train_episodes < episodes")
    if cut:
        config = ("organism @%d:cut:goals>policy @%d:cut:memory>policy"
                  % (train_episodes, train_episodes))
    else:
        config = "organism"
    agent = Organism(config, seed)
    env = make_world(world, seed, variant)
    transcript = PublicTranscript()
    narrator, grounded = Decoder(), Decoder()
    sums = {"narrator": 0.0, "grounded": 0.0}
    n_test = 0
    train_hash = hashlib.sha256()

    for ep in range(episodes):
        obs = env.reset()
        transcript.reset_episode()
        reward, outcome, boundary = 0.0, None, True
        while True:
            actions = tuple(env.legal())
            public = transcript.features(obs, reward, outcome, actions)
            decision = agent.step(obs, reward, outcome, boundary, actions)
            internal = public + tuple("ws:" + tag for tag in decision.broadcast)
            np = narrator.forecast(public, actions)
            gp = grounded.forecast(internal, actions)
            if ep < train_episodes:
                # This digest MUST match between intact and cut lives.
                event = [ep, obs, reward, outcome, list(decision.broadcast),
                         decision.action]
                train_hash.update((json.dumps(event, sort_keys=True) + "\n").encode())
                narrator.learn(public, actions, decision.action, np)
                grounded.learn(internal, actions, decision.action, gp)
            else:
                sums["narrator"] += Decoder.brier(np, decision.action)
                sums["grounded"] += Decoder.brier(gp, decision.action)
                n_test += 1
            transition = env.step(decision.action)
            transcript.observe(obs, decision.action, transition.reward,
                               transition.outcome)
            if transition.done:
                agent.end_episode(transition.reward, transition.outcome)
                break
            obs, reward, outcome, boundary = (transition.obs, transition.reward,
                                              transition.outcome, False)

    if not n_test:
        raise AssertionError("no held-back action events")
    n, g = sums["narrator"] / n_test, sums["grounded"] / n_test
    return {"seed": seed, "world": world, "variant": variant, "cut": cut,
            "steps": n_test, "narrator_brier": n, "grounded_brier": g,
            "gain": n - g, "training_digest": train_hash.hexdigest()}
