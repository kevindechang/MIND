"""World registry. Every agent is evaluated in every world it is pointed at."""
from .glyph import Glyph
from .outage import Outage
from .vigil import Vigil
from .workshop import Workshop

WORLDS = {cls.name: cls for cls in (Vigil, Outage, Workshop, Glyph)}


def make_world(name: str, seed: int, variant: str = "dev"):
    if name not in WORLDS:
        raise ValueError(f"unknown world {name!r}; choose {sorted(WORLDS)}")
    return WORLDS[name](seed, variant)
