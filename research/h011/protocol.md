# H011 structural-transfer design protocol (frozen before execution)

Date: 2026-10-11. Base main: `0debeeaad96f362a23c06961253d02fd8379675f`.
Status: DESIGN_ONLY; no organism evaluation, no dev/held-out seeds viewed.

## Scientific question
Can a minimal, deterministic relational representation help the *existing MIND organism* transfer its learned action rule to entirely unseen surface glyphs on the first action of an episode? This is a prerequisite, **not** a demonstration, of impasse-triggered procedural compilation or post-SIGKILL transfer.

## Hypothesis and mechanism
In a one-action `glyph` world, a hidden lifetime-stable binary rule maps equality/inequality of two publicly observed tokens to one of two actions. Training episodes use one alphabet; the late evaluation half uses a disjoint alphabet. The optional `analogy` organ emits the equality of the two raw token values. No hidden rule, phase, scorer information, or outcome is given to the organ. The organism learns the mapping from public feedback through its existing policy. Use `capacity=inf` in the primary comparison to eliminate workspace displacement as an explanation.

## Prospective primary effect (C024)
For 32 paired lifetimes, 200 episodes each, `glyph/dev`, the difference in late transfer first-action accuracy between `organism +analogy capacity=inf` and `organism capacity=inf` must exceed **0.10 absolute** with its entire conservative 95% interval above the margin. Ten percentage points is a deliberately meaningful change in binary-choice accuracy (one additional correct choice per ten), selected before any run, not tuned to data.

## Prospective shifted-lexicon confirmation (C025)
The same >0.10 absolute improvement must hold for `glyph/shift` with longer, structurally different held-out tokens and irrelevant noise. No claim is supported until dev and sealed held-out evaluations are executed and records committed. Claims are independent tests, not a license to cherry-pick one.

## Strongest simple rival
`rival:equality`: the **same QLearner** as the organism's policy, using a one-step equality feature derived from the same two public tokens, plus the standard public-outcome success table. It discards raw token identities and does not access the hidden rule. It may tie or beat the new organ, which would show that any gain is representational rather than distinctive cognitive integration. A further Bayes-style structural rival remains a desirable adversarial extension.

## Falsifiers and artifact checks
A null or reversed effect, interval not clearing 0.10, equal-information rival tie/win, train/eval token leakage, action-dependent world draws, a replay divergence, or a result that vanishes under the shifted variant all defeat stronger interpretations. This setup cannot by itself test first-try transfer *after actual SIGKILL*: require a later fresh-process intervention. Never infer L2 achievement or L3 from deterministic tests.

## Planned commands (ALL NOT_EXECUTED in this environment)
```bash
python -m mind doctor
python -m unittest discover -s tests
python -m mind check C024 --quick
python -m mind check C024 --record
python -m mind check C024 --heldout --record
python -m mind check C025 --record
python -m mind check C025 --heldout --record
python -m mind atlas
python -m mind check
python -m unittest discover -s tests
python -m mind doctor
python -m mind status --write
```

A full Git clone was attempted and failed: `Could not resolve host: github.com`. No claim records, seeds, independent review, or full-suite execution exist. SELF-REVIEW_ONLY. NOT_READY_FOR_PRODUCT_TRANSFER.
