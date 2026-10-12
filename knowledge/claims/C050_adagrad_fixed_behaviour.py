"""H014 optimizer control: better prediction without selecting broadcast inputs.

Primary: normalised/all minus AdaGrad/all late-half Brier > .008 on the same
baseline vigil/dev lives (300 episodes). Margin chosen at C017's scale before
the eight-seed pilot. sqrt/all, bias-only and memory controls are descriptive.
Pilot found sqrt/all stronger than AdaGrad/all; this claim does not assert
AdaGrad is the best optimizer. No behavioural, efficiency, transfer or L3 claim.
"""
from mind.claims import Check, Claim


def optimizer_control(ctx):
    from mind.shadow import fixed_behaviour_many
    from mind.stats import bootstrap_ci, compare
    conditions = {
        "adagrad": {"model_params": {"step": "adagrad"}},
        "sqrt": {"model_params": {"step": "sqrt"}},
        "bias_normalised": {"model_params": {"gate": "bias"}},
        "bias_adagrad": {"model_params": {"step": "adagrad", "gate": "bias"}},
        "drop_memory": {"drop": ("memory",), "model_params": {"step": "adagrad"}},
        "sham_memory": {"sham": ("memory",), "model_params": {"step": "adagrad"}},
    }
    rows = fixed_behaviour_many(ctx.lab, "organism", "vigil", "dev", ctx.seeds, 300,
                                conditions, audit_shams=True)
    for r in rows:
        audit = r["sham_audit"]["memory"]
        if not r["exact"] or not all(audit[k] for k in ("presence_kept", "count_kept", "load_kept")):
            raise RuntimeError("K09/K10 shadow or sham invariant failed")
        if audit["fallback_scored"]:
            raise RuntimeError("sham falls back on real contents in the scored half")
    primary = compare([r["brier"] for r in rows], [r["adagrad"] for r in rows],
                      ">", 0.008, seed="C050|primary")
    diagnostic = {}
    for label, a, b in (("sqrt_gain", "brier", "sqrt"),
                        ("bias_rule_gain", "bias_normalised", "bias_adagrad"),
                        ("context_gain_adagrad", "bias_adagrad", "adagrad"),
                        ("memory_net_adagrad", "drop_memory", "adagrad"),
                        ("memory_content_adagrad", "sham_memory", "adagrad"),
                        ("memory_carry_adagrad", "sham_memory", "drop_memory")):
        m, lo, hi = bootstrap_ci([r[a] - r[b] for r in rows], seed="C050|" + label)
        diagnostic[label] = {"mean": m, "lo": lo, "hi": hi, "descriptive": True}
    return {"verdict": primary["verdict"], "robust": True, "primary": primary,
            "diagnostic": diagnostic,
            "scores": {k: sum(r[k] for r in rows) / len(rows) for k in ("brier", *conditions)},
            "per_seed": [{"seed": r["seed"], **{k: r[k] for k in ("brier", *conditions)}} for r in rows],
            "summary": f"fixed-behaviour vigil Brier gain {primary['diff']:+.4f} "
                       f"[{primary['lo']:+.4f},{primary['hi']:+.4f}] > 0.008; "
                       f"normalised {primary['a']:.4f}, AdaGrad {primary['b']:.4f}"}


CLAIM = Claim(
    id="C050", title="AdaGrad improves self-model prediction on fixed vigil events",
    statement="On baseline organism vigil/dev lives, AdaGrad/all reduces late-half Brier by more than "
              "0.008 against the normalised/all self-model on identical actions, broadcasts and outcomes.",
    kind="threshold", scope="L2", question="H014", depends_on=("K09", "K10", "K14"),
    extends=("C030", "C036"), test=Check(optimizer_control, seeds=32),
    by="Codex (H014 session)", created="2026-10-11",
    rationale="Test the update-rule alternative before attributing benefits to learned input selection. "
              "This Check explicitly compares predictors on one stream; live-agent rival scores are not commensurate.",
)
