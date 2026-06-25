# EDGAR Financial NLP — a hands-on tour of model adaptation

A learning project that works through the modern toolkit for **financial sentiment analysis** — from a 2011
word-counting lexicon to a 4-bit quantized 7B LLM — one technique per notebook, each building on the last. The
techniques are adapted from graduate NLP coursework and retargeted to the financial domain (SEC filings and
earnings text).

Every method is scored on the **same benchmark** ([Financial PhraseBank](https://huggingface.co/datasets/takala/financial_phrasebank)),
and each notebook changes **exactly one variable** versus the one before it, so every comparison is honest.

## Two tracks, one bake-off

- **Track A — encoder / fine-tuning:** domain-adaptive pretraining, full fine-tuning, FinBERT, QLoRA.
- **Track B — generative / prompting:** LLM-as-classifier, synthetic data generation, structured extraction.
- **Convergence:** a final bake-off scores everything in one table.

## How the notebooks teach

Each part (from Part 2 on) ships as **two files**:

- **`*_PRACTICE.ipynb`** — the version you work through, with the key code blanked out as `### YOUR CODE HERE`.
- **`*.ipynb`** — the answer key to check yourself against *after* attempting.

Every notebook follows the same four-point structure:

1. **A `## 0. Why` section** — the problem the technique solves and the decision it informs.
2. **The core concept is the blank** — you *write* the thing the notebook exists to teach (the QLoRA config, the
   prompt, the scoring harness), not just read it.
3. **The effect is instrumented** — you *measure* what each choice does (memory, trainable parameters, accuracy,
   JSON-validity, cost), never take it on faith.
4. **Reflection prompts** — predict-before-you-run and short ✍️ questions that make you articulate the *why*.

## The notebooks

> ▶ = open the **practice** notebook in Colab. Answer keys are linked by name.

| # | Topic | Practice | Answer key |
|---|-------|----------|------------|
| 1 | **Continued pretraining** — adapt GPT-2 to EDGAR 10-K text; before/after perplexity (in- vs out-of-domain) | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Continued_Pretraining_Part1.ipynb) *(pre-written)* | — |
| 2 | **Fine-tune GPT-2** — base vs. EDGAR-pretrained, sentiment as next-token prediction | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Sentiment_Finetune_Part2_PRACTICE.ipynb) | [key](EDGAR_Sentiment_Finetune_Part2.ipynb) |
| 3 | **BERT `[CLS]` classifier** — `bert-base` vs. `ProsusAI/finbert`; + frozen-probe & zero-shot explorations | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Sentiment_BERT_Part3_PRACTICE.ipynb) | [key](EDGAR_Sentiment_BERT_Part3.ipynb) |
| 4 | **QLoRA** — 4-bit Mistral-7B fine-tune; build the config and *measure* memory/params/accuracy | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Sentiment_QLoRA_Part4_PRACTICE.ipynb) | [key](EDGAR_Sentiment_QLoRA_Part4.ipynb) |
| 5 | **LLM-as-classifier** — zero-/few-shot prompting; the no-training baseline + a prompt-wording experiment | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Sentiment_LLM_Part5_PRACTICE.ipynb) | [key](EDGAR_Sentiment_LLM_Part5.ipynb) |
| 6 | **Synthetic data** — generate labeled sentences with the LLM, augment a scarce seed set, measure the lift | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Sentiment_Synthetic_Part6_PRACTICE.ipynb) | [key](EDGAR_Sentiment_Synthetic_Part6.ipynb) |
| 7 | **Structured extraction** — prompt the LLM to emit JSON (sentiment, guidance, figures) with chain-of-thought | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Structured_Extraction_Part7_PRACTICE.ipynb) | [key](EDGAR_Structured_Extraction_Part7.ipynb) |
| 8 | **The bake-off** — score every method on one held-out set; one table, accuracy vs. cost | [▶](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/EDGAR_Bakeoff_Part8_PRACTICE.ipynb) | [key](EDGAR_Bakeoff_Part8.ipynb) |

**Companion — [Choosing a Training Method](https://colab.research.google.com/github/daveschaaf/edgar_nlp/blob/main/Choosing_a_Training_Method_PRACTICE.ipynb)** ([key](Choosing_a_Training_Method.ipynb)):
a no-code judgment lab — scenario triage ("which method, and why?") plus a predict-the-ranking scoreboard that
the parts above fill in.

## Running them

- **Platform:** Google Colab with a **T4 GPU** (Runtime → Change runtime type → T4). Everything is sized to fit.
- **Gated model:** Parts 4–8 use `mistralai/Mistral-7B-Instruct-v0.3` (4-bit). Accept the license on Hugging
  Face and log in when the notebook prompts.
- **Datasets pin:** Part 1 pins `datasets==2.21.0` (the EDGAR corpus is a script-based dataset). Later parts
  load Financial PhraseBank straight from its zip, so no pin is needed.
- **Workflow:** open the `*_PRACTICE` notebook, fill the `### YOUR CODE HERE` blanks, run top-to-bottom once
  (re-running model-load cells stacks copies and causes OOM), then diff against the answer key.

## Repository layout

- `Part*` notebooks — the lessons (above).
- [`PROJECT_SCOPE.md`](PROJECT_SCOPE.md) — the larger research framing this practice track was scoped down
  from: replicating an earnings-announcement-returns study on free data (the eventual destination).
- [`HANDOFF.md`](HANDOFF.md) — design notes and the original roadmap.
- [`tools/`](tools/) — `strip_widgets.py` + a git pre-commit hook that keeps Colab-run notebooks renderable on
  GitHub (Colab writes malformed widget metadata that otherwise breaks rendering).

## Datasets & models

- **Pretraining corpus:** `eloukas/edgar-corpus` (10-K filing text, by year).
- **Benchmark:** `takala/financial_phrasebank`, config `sentences_allagree` (3-class, ~2,264 sentences).
- **Models:** `gpt2`, `bert-base-cased`, `ProsusAI/finbert`, `mistralai/Mistral-7B-Instruct-v0.3`.

---

*A learning artifact: the goal is to build, fairly compare, and reason about the full spectrum of model
adaptation — not to ship a production classifier.*
