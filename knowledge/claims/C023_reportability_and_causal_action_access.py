"""H013: does a reportable broadcast both predict and causally constrain action?

Pre-execution prediction, not a claim of self-awareness. The broadcast narrator
is an external online readout, NOT an organism-generated verbal report. Its
strongest simple rival uses 32 raw public observations, past actions and
outcomes, with the identical learner. Predictions are scored on the SAME
organism's actions. One-step cuts are made on identical predecision state;
sham cuts reach self_model rather than policy. If the transcript rival ties or
wins, or cutting causal access changes too few actions, the conjunction fails.

Margins are selected without running H013 data: 0.03 nats/bell is a small but
meaningful improvement over a powerful public-history baseline; 0.10 of bell
actions is a minimal substantive causal-access effect, conservative relative
to C003's large long-gap goals ablation effect. The two simultaneous tests
form an intersection-union claim, not two opportunistic ways to pass.
"""
from mind.claims import Check, Claim


def report_access(ctx):
    from mind.rivals.reporting import run_report_probe
    from mind.stats import bootstrap_ci

    # Both worlds run on the same sealed seeds; outage/silent is an explicit
    # secondary generalisation/negative-control diagnostic, not a second pass gate.
    vigil = [run_report_probe(seed, "vigil", "long", episodes=200) for seed in ctx.seeds]
    outage = [run_report_probe(seed, "outage", "silent", episodes=60) for seed in ctx.seeds]
    gain, gain_lo, gain_hi = bootstrap_ci([r["report_gain"] for r in vigil], seed="C023:gain")
    causal, causal_lo, causal_hi = bootstrap_ci(
        [r["cut_rate"] - r["sham_rate"] for r in vigil], seed="C023:cut")
    if any(r["sham_changed"] != 0 for r in vigil + outage):
        raise AssertionError("sham altered action: causal manipulation invalid")
    if min(r["probes"] for r in vigil) < 10:
        raise AssertionError("too few preregistered counterfactual bell events")
    if gain_lo > 0.03 and causal_lo > 0.10:
        verdict = "HOLDS"
    elif gain_hi <= 0.03 or causal_hi <= 0.10:
        verdict = "FAILS"
    else:
        verdict = "INCONCLUSIVE"
    return {
        "verdict": verdict, "robust": True,
        "gain_nats_per_bell": gain, "gain_ci": [gain_lo, gain_hi],
        "causal_cut_rate_minus_sham": causal, "causal_ci": [causal_lo, causal_hi],
        "vigil_probes": int(sum(r["probes"] for r in vigil)),
        "outage_silent_report_gain": sum(r["report_gain"] for r in outage) / len(outage),
        "outage_silent_cut_rate": sum(r["cut_rate"] for r in outage) / len(outage),
        "vigil_report_cut_loss_increase": (sum(r["report_cut_loss_increase"] for r in vigil)
                                            / len(vigil)),
        "vigil_transcript_cut_loss_increase": (sum(r["transcript_cut_loss_increase"]
                                                for r in vigil) / len(vigil)),
        "summary": (f"vigil/long report minus transcript32 gain {gain:+.4f} "
                    f"[{gain_lo:+.4f},{gain_hi:+.4f}] nats/bell (need >0.03); "
                    f"causal cut-sham {causal:+.4f} [{causal_lo:+.4f},{causal_hi:+.4f}] "
                    f"(need >0.10); outage/silent secondary measured"),
    }


CLAIM = Claim(
    id="C023",
    title="Reportable workspace predicts action and has causal policy access",
    statement="In vigil/long, an online decoder of the reportable broadcast predicts the organism's "
              "own bell action at least 0.03 nats/tick better than a transcript32 decoder "
              "trained on the same action labels, AND identical-state dual cuts of goals and "
              "memory to policy change at least 0.10 of bell decisions beyond a self-model "
              "sham while the reportable broadcast remains unchanged.",
    kind="effect", scope="L2", question="H013", depends_on=("K01",),
    extends=("C003", "C004"), test=Check(report_access, seeds=16),
    by="MIND research agent (DESIGN ONLY)", created="2026-10-11",
    rationale="Separates prediction of action from causal access to policy; a public-history "
              "rival win or a null cut is a valid falsifier, not a consciousness result.",
)
