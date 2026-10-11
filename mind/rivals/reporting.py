"""H013 causal action-report probe; no organism-generated self-report claim."""
from __future__ import annotations
from copy import deepcopy
import math
from typing import Dict
from ..kernel import Organism
from ..worlds import make_world
from .report_learner import OnlineActionReadout
from .report_narrators import BroadcastNarrator, Transcript32Narrator
from .report_interventions import _cut_fork

def run_report_probe(seed: int, world: str = "vigil", variant: str = "long",
                     episodes: int = 200, probe_every: int = 5) -> Dict[str, float]:
    """Return same-action-stream predictive loss and one-step causal cuts.

    Late-half scoring only. Vigil scores bell decisions, not the easy wait
    majority; outage scores all late ticks. Every probe is selected from the
    episode index and public bell/time, never from the action or outcome.
    """
    if episodes < 4 or probe_every < 1:
        raise ValueError("need >=4 episodes and probe_every >=1")
    if world not in ("vigil", "outage"):
        raise ValueError("H013 probe supports vigil and outage only")
    organism = Organism("organism", seed)
    env = make_world(world, seed, variant)
    report_model, transcript_model = OnlineActionReadout(), OnlineActionReadout()
    transcript = Transcript32Narrator()
    report_loss = transcript_loss = 0.0
    report_cut_delta = transcript_cut_delta = 0.0
    scored = probes = changed = sham_changed = 0
    for episode in range(episodes):
        obs = env.reset()
        reward, outcome, boundary = 0.0, None, True
        tick_in_episode = 0
        while True:
            actions = tuple(env.legal())
            transcript_features = transcript.features(obs, reward, outcome, boundary)
            # Save an untouched state BEFORE the original step, so the cut is causal.
            selected = (episode >= episodes // 2 and episode % probe_every == 0
                        and (obs.get("bell") == "1" if world == "vigil" else tick_in_episode == 12))
            snapshot = deepcopy(organism) if selected else None
            decision = organism.step(obs, reward, outcome, boundary, actions)
            broadcast_features = BroadcastNarrator.features(decision.broadcast)
            report_p = report_model.predict(broadcast_features, actions)
            transcript_p = transcript_model.predict(transcript_features, actions)
            # Prediction functions have no access to the current action; use it only
            # for scoring and subsequent online learning, never as an input feature.
            if episode >= episodes // 2 and (world != "vigil" or obs.get("bell") == "1"):
                report_loss -= math.log(max(report_p[decision.action], 1e-12))
                transcript_loss -= math.log(max(transcript_p[decision.action], 1e-12))
                scored += 1
            report_model.learn(broadcast_features, decision.action, report_p)
            transcript_model.learn(transcript_features, decision.action, transcript_p)
            transcript.remember(obs, decision.action)
            if selected:
                cut_action, sham_action = _cut_fork(
                    snapshot, obs, reward, outcome, boundary, actions,
                    decision.action, decision.broadcast)
                probes += 1
                changed += int(cut_action != decision.action)
                sham_changed += int(sham_action != decision.action)
                # The same report sees identical broadcast in both forks.
                # This measures whether its probability assigned to the actual
                # action deteriorates under a cut of the causal policy path.
                report_cut_delta += math.log(
                    max(report_p[decision.action], 1e-12) / max(report_p[cut_action], 1e-12))
                transcript_cut_delta += math.log(
                    max(transcript_p[decision.action], 1e-12) / max(transcript_p[cut_action], 1e-12))
            step = env.step(decision.action)
            if step.done:
                organism.end_episode(step.reward, step.outcome)
                break
            obs, reward, outcome, boundary = step.obs, step.reward, step.outcome, False
            tick_in_episode += 1
    if not scored or not probes:
        raise AssertionError("insufficient scored or counterfactual events")
    return {
        "seed": float(seed), "scored": float(scored), "probes": float(probes),
        "report_logloss": report_loss / scored,
        "transcript32_logloss": transcript_loss / scored,
        "report_gain": (transcript_loss - report_loss) / scored,
        "cut_changed": float(changed), "sham_changed": float(sham_changed),
        "cut_rate": changed / probes, "sham_rate": sham_changed / probes,
        "report_cut_loss_increase": report_cut_delta / probes,
        "transcript_cut_loss_increase": transcript_cut_delta / probes,
    }
