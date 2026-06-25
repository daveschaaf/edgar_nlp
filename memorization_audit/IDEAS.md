# Bridging this project → "Prediction or Memorization?" LLM trading-signal audit

*Captured 2026-06-25. Local notes — not committed (references forward strategy; repo is public).*

## Context (the PRD this connects to)

**One-line:** When an LLM appears to predict returns from financial news, measure how much of that "edge" is
genuine **prediction** vs. **recall of its own training data** — using a design that holds the market constant
(a **cross-model placebo**: OLD vs. NEW checkpoints of the same family/scale, differing only in training
cutoff) so the result survives a skeptical quant reviewer. Headline contribution is **methodological honesty**,
not a profit claim ("proud either way"). Anchored by a Loughran-McDonald lexicon baseline (can't memorize) and
a three-window read-out; IC (information coefficient) as the working edge metric. The LLM does exactly one
thing — text → structured sentiment score — and everything downstream is deterministic, auditable code.

## Why this project is a strong launchpad

The PRD's integrity claim ("AI for interpretation, deterministic for the rest") is the **keys-vs-values
discipline** already practiced here, and three of its components were literally built in Parts 1–8.

---

## Idea 1 — The IC read-out *is* the Part 8 bake-off harness, re-skinned

The PRD's core computation — *edge metric per window × per scorer*, scored against a pre-committed rule — is
structurally identical to the Part 8 harness (`record` / `RESULTS` scoring every method on one shared held-out
set).

- **Reuse:** the `record` harness pattern; swap *accuracy → information coefficient* (rank-corr of sentiment vs.
  forward return), add a **window** axis (the 3-window table). Scorers become `{OLD, NEW, lexicon}`.
- **Lexicon anchor already done:** Part 8 `lexicon_classify` (Loughran-McDonald-style) IS the PRD's
  no-cutoff baseline. Drops in unchanged as the regime detector.
- **"Change one variable" = the placebo:** the discipline applied to every part = OLD-vs-NEW holding
  family/scale fixed.
- **Serves:** fast path to Phase 1 — measurement spine + anchor are ported, not built.

## Idea 2 — The `INT` box is Part 5 + Part 7 — and Part 7's *validity rate* closes a confound the PRD misses

The single non-deterministic step (headline → sentiment score) is the **LLM-as-classifier** (Part 5:
`build_prompt` + `parse_label`) hardened with **structured extraction** (Part 7: JSON + CoT + robust
`parse_json` + validity-rate instrumentation).

- **Reuse:** Part 5 prompt/parse for the score; Part 7 robust parser + per-call validity tracking.
- **New door it closes:** the PRD controls a *capability* confound (newer = better at sentiment) but not a
  **parsing/format confound** — if NEW emits cleaner JSON than OLD, OLD's "edge" could decay just because more
  of its outputs failed to parse, which would *look like memorization*. Part 7's lesson ("validity is the
  gatekeeper") → **track validity-rate per model per window and confirm it's constant.**
- **Serves:** makes the one non-deterministic step auditable AND equalized across OLD/NEW.

## Idea 3 — Corroborate the placebo with a perplexity membership-inference probe (Part 1)  ← differentiator

The placebo is an *indirect* memorization signal (IC gap in Window 2). **Part 1's perplexity machinery** gives a
*direct, mechanical* one — and two independent signals agreeing is what survives a skeptic.

- **Idea:** memorized text has **lower perplexity/loss** under the model that trained on it. Compute per-headline
  perplexity under OLD and NEW; the memorization fingerprint = NEW shows systematically lower perplexity than
  OLD on **Window-2** headlines (in NEW's training window, not OLD's) — pointing the same way as the IC gap.
- **Reuse:** the Part 1 `perplexity()` function + the in-domain-vs-out-of-domain framing, applied across the
  training-cutoff boundary instead of across corpora.
- **Bonus (Part 6):** generate **synthetic "canary" headlines** the models provably never saw, as a negative
  control / "what does *no* memorization look like" reference.
- **Serves:** "behavioral IC gap **and** mechanical perplexity gap, both localized to Window 2" is triangulated —
  the piece that turns a competent audit into one a quant reviewer remembers, and it reuses the one part of the
  project nobody expects in a trading-signal audit.

---

## What's genuinely NEW (not covered by this project — the real Phase 0/1 build)

- **Point-in-time alignment** of each headline to the first tradeable forward-return window after it was public
  (the lookahead trap).
- **Returns / universe data + survivorship** (free substitutes noted in `PROJECT_SCOPE.md`: yfinance,
  Fama-French).
- **IC statistics + effective-sample power** (esp. the scarce post-cutoff Window 2/3).
- **Sourcing same-family, cutoff-spaced checkpoints with trustworthy documented cutoffs** — the binding
  constraint (PRD Phase-0 gate).
- **Headline hygiene** — exclude outcome-revealing headlines ("Stock soars 20% on beat").

This project supplies the **scorer, the anchor, and the measurement harness**; the **identification design and
market-side plumbing** are the new work.

## Recommended path

- **Fast Phase-1 spine:** Ideas 1 + 2 (port the harness, port the lexicon, harden the scorer).
- **Differentiator:** Idea 3 (perplexity membership-inference + synthetic canaries).
- **Next concrete step to pick up later:** (a) sketch the Part 8 harness refactor into a `window × scorer` IC
  engine; (b) outline the Phase-0 checkpoint-sourcing probe.

## Pointers (this repo)

- Scoring harness + lexicon: `EDGAR_Bakeoff_Part8.ipynb`
- LLM scorer (prompt/parse): `EDGAR_Sentiment_LLM_Part5.ipynb`
- Structured extraction + validity rate: `EDGAR_Structured_Extraction_Part7.ipynb`
- Perplexity machinery: `EDGAR_Continued_Pretraining_Part1.ipynb`
- Synthetic generation: `EDGAR_Sentiment_Synthetic_Part6.ipynb`
- Finance/econometrics framing + free-data substitutes: `PROJECT_SCOPE.md`
