# Handoff Summary — EDGAR Financial NLP (practice → portfolio)

*Prepared 2026-06-20 for continuation in Claude Code.*

## What this project is

A hands-on learning project that adapts the user's grad-course NLP assignments to the **financial domain**, building toward an eventual portfolio piece on **earnings-disclosure sentiment and stock returns**. Scope was deliberately narrowed from a full research project to the **simplest runnable exercise that can grow**. The immediate mode is *learning/practice*; the long-term target is a portfolio artifact for **ML/NLP engineer** hiring.

Work is split into two complementary tracks on one shared problem (financial sentiment):

- **Track A — encoder / fine-tuning** (from the user's Assignments 2 & 3): continued pretraining, fine-tuning, FinBERT, QLoRA.
- **Track B — generative LLM / prompting** (from Assignment 4): LLM-as-classifier, synthetic data, structured extraction, chain-of-thought.

Unifying design: **Financial PhraseBank is the shared benchmark** every method is scored on; **`eloukas/edgar-corpus` is the pretraining fuel**. Each part changes exactly one variable ("change one variable" discipline).

## Current state

- ✅ **Part 1 built** — `EDGAR_Continued_Pretraining_Part1.ipynb` (continued pretraining of GPT-2 on EDGAR 10-K text + before/after perplexity, in-domain vs out-of-domain). Colab/T4, not yet run by the user.
- ⬜ Parts 2–8 designed but not built (roadmap below).
- The user is about to run Part 1 themselves.

## Files in this folder

- `PROJECT_SCOPE.md` — full scoping history and decisions, including the *original* (larger) research framing and parked candidate research directions. Read this for the deeper finance/econometrics context (event study, LP-DiD, SUE, free-vs-paid data gaps).
- `EDGAR_Continued_Pretraining_Part1.ipynb` — the Part 1 deliverable.
- `HANDOFF.md` — this file.

## Roadmap (Parts 1–8)

**Foundation**
1. **Continued pretraining** — GPT-2 on EDGAR + perplexity (domain adaptation). *(built)*

**Track A — encoder / fine-tuning**
2. **Fine-tune for sentiment** — base GPT-2 vs. Part-1 EDGAR-pretrained GPT-2 on Financial PhraseBank. Tests whether continued pretraining helped downstream. *(mirrors Assignment 2 §2)*
3. **Encoder classifier + FinBERT payoff** — `bert-base` vs. `ProsusAI/finbert` via [CLS] classification on the same task. FinBERT = the published version of Part 1's idea. *(mirrors Assignment 2 §3)*
4. **PEFT scaling (optional)** — QLoRA fine-tune a larger model on the same task. *(mirrors Assignment 3)*

**Track B — generative LLM / prompting**
5. **LLM-as-classifier** — zero-shot then few-shot Mistral-7B-Instruct (4-bit) on the same test set; no-training baseline vs. the fine-tuned models.
6. **Synthetic data generation** — prompt Mistral to generate labeled financial sentences, add to the Part 2/3 training set, measure accuracy change. The bridge from Track B → Track A; attacks the labeling bottleneck.
7. **Structured extraction + explainable sentiment** — prompt LLM to emit JSON (sentiment, guidance direction, key figures) from real press-release text, with CoT rationales. The natural on-ramp to real 8-K data.

**Convergence**
8. **Bake-off** — one results table scoring every approach on a held-out set (lexicon → fine-tuned GPT-2 → FinBERT → QLoRA → zero/few-shot LLM → synthetic-augmented). Portfolio centerpiece.

Parts are modular: after a track's prerequisite, they can be done in any order.

## Technical conventions / constraints

- **Runtime:** Google Colab, **T4 GPU**. Everything must fit a T4 (Mistral-7B in 4-bit via bitsandbytes, as in Assignment 4).
- **`datasets==2.21.0` pin** — required because `eloukas/edgar-corpus` and `wikitext` are script-based datasets newer `datasets` versions reject. Use `trust_remote_code=True`.
- **GPT-2 pad token:** add `[PAD]`, `resize_token_embeddings`; Part 1's data class keeps only full-length chunks so pad tokens never enter training.
- Hyperparameters in Part 1: `max_len=100`, `batch_size=4`, `lr=1e-5`, `TRAIN_STEPS=1000`, `EDGAR_YEAR='year_2020'`, `TARGET_CHUNKS=15000`. Tunable at top of notebook.
- Part 1 currently concatenates all filing sections; alternative is MD&A only (`section_7`) — one-line change if a more narrative corpus is wanted.

## Datasets & models (HuggingFace IDs)

- Pretraining corpus: `eloukas/edgar-corpus` (10-K filing text, unlabeled, by year).
- Out-of-domain control: `wikitext` / `wikitext-2-raw-v1`.
- Sentiment benchmark: `takala/financial_phrasebank` (config `sentences_allagree`, 3-class pos/neutral/neg, ~2,264 sentences; no predefined split — do your own `train_test_split`). Simplification used: can drop "neutral" to run binary.
- Models: `gpt2`, `bert-base-cased`, `ProsusAI/finbert`, `mistralai/Mistral-7B-Instruct-v0.3`.

## Academic-integrity note

The user has **not yet completed Assignment 4** (image gen/CLIP/BLIP + Mistral prompt engineering). Practicing the *techniques* in this project is fine; do **not** reproduce or pre-fill Assignment 4's graded answers. Track B (Parts 5–7) practices the same prompting techniques on financial data — keep it separate from the graded notebook.

## Background / prior work (for if the bigger project resumes)

- **Anchor paper:** Wu, Akin, Martineau, Grégoire & Veneris (2025), "Extracting the Structure of Press Releases for Predicting Earnings Announcement Returns," ICAIF '25 (arXiv 2509.24254). Near-identical setup (8-K EX-99.1 text, hard-vs-soft information, FinBERT). Their "structure" = LDA topics, not discourse roles.
- **Free-vs-paid data gap:** they used IBES/CRSP/TAQ (paid). Free substitutes: EDGAR XBRL for EPS, yfinance for prices, Fama-French factors. Biggest divergences: no analyst-consensus surprise (use a naive random-walk SUE instead), survivorship bias in yfinance, GAAP vs. street EPS, no historical intraday. See `PROJECT_SCOPE.md` for the full table.
- The multimodal half of Assignment 4 (image gen/CLIP/BLIP) does **not** fit this text project — intentionally excluded.

## Suggested next step

Build **Part 2** (fine-tune base GPT-2 vs. EDGAR-pretrained GPT-2 on Financial PhraseBank), reusing the Part 1 pretrained model. Keep the same Colab/T4 + `datasets==2.21.0` conventions.
