"""Organ registry. To contribute an organ: add a module here, register it in
ORGANS, keep it event-sourced (see kernel.Organ), and run `python -m mind check`.
Optional organs are enabled per experiment with the `+name` modifier."""
from .efference import Efference
from .goals import Goals
from .memory import Memory
from .perception import Perception
from .policy import Policy
from .self_model import SelfModel

ORGANS = {cls.name: cls for cls in (Perception, Memory, Goals, SelfModel, Policy, Efference)}

# Fixed order = the order organs propose and learn each tick.
DEFAULT_ORGANS = ("perception", "memory", "goals", "self_model", "policy")
