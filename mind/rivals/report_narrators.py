"""Pre-action broadcast readout and public-only 32-step transcript rival."""
from __future__ import annotations
from collections import deque
from typing import Dict, Optional, Sequence, Tuple

class BroadcastNarrator:
    """Readout of the globally reportable, pre-action broadcast; no action input."""

    @staticmethod
    def features(broadcast: Sequence[str]) -> Tuple[str, ...]:
        return tuple("broadcast:" + tag for tag in sorted(broadcast))


class Transcript32Narrator:
    """Stronger public-only rival: 32 raw observations, past actions and outcomes."""

    def __init__(self):
        self.history: deque = deque(maxlen=32)

    def features(self, obs: Dict[str, str], reward: float, outcome: Optional[int],
                 boundary: bool) -> Tuple[str, ...]:
        if boundary:
            self.history.clear()
        feats = ["now:" + str(k) + "=" + str(v) for k, v in sorted(obs.items())]
        if not boundary:
            feats.append("previous_outcome=" + str(outcome))
            feats.append("previous_reward=" + ("pos" if reward > 0 else "neg" if reward < 0 else "zero"))
        for lag, (past_obs, past_action) in enumerate(reversed(self.history), start=1):
            feats.append(f"lag{lag}:action={past_action}")
            feats.extend(f"lag{lag}:{k}={v}" for k, v in past_obs)
        return tuple(feats)

    def remember(self, obs: Dict[str, str], action: str) -> None:
        self.history.append((tuple(sorted((str(k), str(v)) for k, v in obs.items())), action))


REPORT_RIVALS = {
    "broadcast": BroadcastNarrator,
    "transcript32": Transcript32Narrator,
}
