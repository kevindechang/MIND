"""Optional stateless equality feature from two public observed glyphs."""
from ..kernel import Content, Organ

class Analogy(Organ):
    name = "analogy"
    home = ("procedural-transfer",)
    defaults = {}

    def propose(self, sense, ctx):
        if "sample" not in sense.obs or "candidate" not in sense.obs:
            return []
        return [Content(self.name, "equal", "1" if sense.obs["sample"] == sense.obs["candidate"] else "0", 0.95)]
