"""Identical-state H013 policy access cut and self-model sham."""
from __future__ import annotations
from copy import deepcopy
from typing import Dict, Optional, Sequence, Tuple
from ..kernel import Organism

def _cut_fork(agent: Organism, obs: Dict[str, str], reward: float,
              outcome: Optional[int], boundary: bool, actions: Sequence[str],
              uncut_action: str, uncut_broadcast: Sequence[str]) -> Tuple[str, str]:
    """Identical-state, one-tick interventions; never advance the live organism."""
    cut = deepcopy(agent)
    sham = deepcopy(agent)
    for source in ("goals", "memory"):
        cut.lesion(f"cut:{source}>policy")
        sham.lesion(f"cut:{source}>self_model")
    a = cut.step(obs, reward, outcome, boundary, actions)
    b = sham.step(obs, reward, outcome, boundary, actions)
    if a.broadcast != tuple(uncut_broadcast) or b.broadcast != tuple(uncut_broadcast):
        raise AssertionError("access lesion changed reportable broadcast: invalid counterfactual")
    if b.action != uncut_action:
        raise AssertionError("self-model sham changed current action: invalid control")
    return a.action, b.action
