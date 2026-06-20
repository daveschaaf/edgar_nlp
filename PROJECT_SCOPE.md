# EDGAR Financial Sentiment Analysis — Project Scope

*Last updated: 2026-06-12*

## Goal

A **research-style analysis** that doubles as an ML/NLP portfolio piece. **Replication-first**: stand on established prior work, reproduce a known result, and let a sharper research question emerge from doing the work. Novelty is explicitly *not* a requirement — a careful replication-plus-extension is a strong portfolio piece, and a lot of overlap with prior work is fine.

## Research question — OPEN (intentionally cleared)

Not fixed yet, by design. We replicate the anchor paper first (below), then let a question surface from what we observe — gaps, discrepancies, or things their setup didn't address. Earlier drafts framed this around hard-vs-soft information, post-announcement drift, and topic-vs-discourse structure; those are **parked as candidate directions** (see bottom), not commitments.

## Anchor prior work — what we replicate first

**Wu, Akin, Martineau, Grégoire & Veneris (2025)**, "Extracting the Structure of Press Releases for Predicting Earnings Announcement Returns," *ICAIF '25*. arXiv: 2509.24254. Near-identical setup to ours — the natural baseline to reproduce:

- **Data:** 8-K **EX-99.1** earnings press releases from EDGAR, 2005–2023 (~138k releases, ~6,500 firms).
- **Hard information:** earnings surprise = (actual EPS − consensus analyst EPS) / price five days prior.
- **Soft information:** the press-release text.
- **Methods:** LDA / bag-of-words vs. BERT family (BERT, MPNET, **FinBERT**); Lasso to build a return score from text; cross-sectional regression of announcement-day return on surprise + soft; SHAP for feature importance; rolling-window training to avoid look-ahead.
- **Key findings:** soft info is ~as informative as the earnings surprise; FinBERT extracts it best; prices **fully impound** the soft info by market open (supports market efficiency — a long-short strategy earns nothing after open); LDA topic analysis reveals managerial self-serving bias.
- **Note — their "structure" = topics, not discourse roles.** Their analysis is topic/embedding based, not a functional decomposition of the document.

> **Data-source caveat for replication:** they use **IBES** (analyst estimates), **CRSP** (returns), and **TAQ** (intraday) — paid/academic. Our replication uses free substitutes: EDGAR XBRL for EPS, yfinance for prices, Fama-French factors. This forces a *naive (random-walk) surprise* instead of analyst-consensus surprise — itself a meaningful difference worth examining (see SUE).

## Phases

1. **Validation / replication of prior work** *(Python)* — reproduce the Wu et al. core result on a tractable subsample with free data: pull 8-K EX-99.1 text + XBRL EPS, prices, factors; build lexicon and FinBERT text scores; regress announcement-day abnormal return on surprise + soft; check whether soft ≈ surprise and FinBERT > lexicon. **Goal of this phase: reproduce a known result and surface candidate research questions from the gaps.**
2. **TBD** — defined by what emerges from Phase 1 (see candidate directions).

## Languages — Python + R

- **Python** — all data pipelines and ML: EDGAR scraping/parsing, XBRL EPS, price/factor downloads, FinBERT + lexicon scoring. Output: a tidy analysis-ready dataset (one row per release).
- **R** — econometrics and the paper: regressions, significance testing, tables, writeup (Quarto / R Markdown).
- **Handoff artifact:** a single tidy dataset (Parquet/CSV) is the contract between the two stages.

## Data — one pipeline + two downloads

The EDGAR text extraction is the irreducible heavy lift (a real scraper). The analysis-side data is mostly static *downloads*, not additional pipelines.

1. **EDGAR pipeline** → 8-K filings, extract **EX-99.1** press-release text, **and** reported EPS via the XBRL `companyfacts` API.
2. **Daily prices** → yfinance (one call per ticker).
3. **Factor benchmark** → Fama-French factors CSV (Ken French data library).

- Endpoints: EDGAR `submissions` API + `Archives`. Respect SEC fair-access limits (10 req/sec, declared User-Agent).
- `acceptanceDateTime` (SGML header `<ACCEPTANCE-DATETIME>`, ET) gives filing time to the second; note it lags the wire release. Classify BMO / AMC / intraday and anchor returns accordingly.

### Resolution — DECIDED

- **Daily and weekly only.** Robust, cheap, standard in event studies; daily resolution washes out T=0 imprecision.
- **Minute/hour out of scope** — historical intraday data unavailable free (paid: Polygon/IEX; academic: TAQ).

## Scope tightening — DECIDED

- **8-K press releases only.** 10-K / 10-Q (MD&A) deferred to a possible sequel.
- **Narrow universe & period** for v1 — one sector or index slice over ~2 years; enough N for cross-sectional inference, a fraction of the scraping.
- **Model progression:** lexicon baseline (Loughran-McDonald) + fine-tuned FinBERT, optional off-the-shelf FinBERT middle step.

## ⚠️ Investigate deeper: earnings surprise / SUE

**SUE = Standardized Unexpected Earnings.** Flagged for a deeper dive — Dave is unfamiliar with it.

- *Why it's central:* the surprise is the "hard information" we hold fixed; replication and any extension need a credible surprise measure.
- *The paid version:* analyst-consensus surprise (IBES) — what Wu et al. use.
- *Our free substitute:* a **random-walk surprise** (this quarter's EPS vs. same quarter last year) from EDGAR XBRL — no external source; defensible "naive" surprise; note the limitation. The gap between naive and analyst-based surprise is itself a candidate question.
- **To-do:** read up on SUE definitions and the naive-vs-analyst distinction; decide the v1 measure.

## Candidate directions (post-replication) — PARKED

Preserved, not committed. Pick after Phase 1 surfaces something concrete.

- **Naive vs. analyst surprise** — how much does using a random-walk surprise (free) instead of analyst consensus (paid) change the hard-vs-soft conclusion?
- **Hard vs. soft incremental info / drift** — does language predict returns *after* the immediate reaction? *Threat:* market efficiency / "Rest in peace PEAD" (Martineau 2022) suggest the honest answer may be null.
- **Discourse-role structure vs. topic** — classify each segment's communicative function (results / operations / guidance / incident) and use structure as signal. *Status: uncertain this is the right angle.*
- **Forward-looking guidance** scored as its own dimension.
- **LP-DiD shock framing** — Dube, Girardi, Jordà & Taylor (2023) local-projections DiD, reusable from the NOAA study; treats each release as a shock and traces dynamic response by horizon.

## Open decisions

- [ ] **SUE deep-dive** — naive (random-walk) vs. analyst surprise for v1.
- [ ] Exact universe (which sector / index slice) and date range for the replication subsample.
- [ ] Market-model choice for abnormal returns (market-adjusted vs. Fama-French).
- [ ] Final deliverable format (paper + notebooks; optional dashboard).

## Literature & sources

- **Wu, Akin, Martineau, Grégoire & Veneris (2025)** — "Extracting the Structure of Press Releases for Predicting Earnings Announcement Returns," ICAIF '25. arXiv 2509.24254. *(Anchor paper to replicate.)* https://arxiv.org/abs/2509.24254
- Loughran & McDonald (2011) — why generic sentiment lexicons fail in finance.
- Tetlock (2007) — media sentiment and stock returns.
- Henry (2008) — "Are Investors Influenced By How Earnings Press Releases Are Written?" https://journals.sagepub.com/doi/10.1177/0021943608319388
- Huang, Teoh & Zhang (2014) — "Tone Management."
- Bernard & Thomas (1989/1990) — post-earnings-announcement drift (PEAD).
- Martineau (2022) — "Rest in Peace Post-Earnings Announcement Drift" (drift largely arbitraged away).
- Meursault et al. (2023) — "PEAD.txt: Post-Earnings-Announcement Drift Using Text."
- Li (2010) — information content of forward-looking statements in corporate filings.
- Dube, Girardi, Jordà & Taylor (2023) — "A Local Projections Approach to Difference-in-Differences," NBER WP 31184. Repo: github.com/danielegirardi/lpdid.
- *Rhetoric and Language in Strategic Financial Communication* (2025) — earnings announcements as impression management. https://www.tandfonline.com/doi/full/10.1080/1553118X.2025.2583142
- (Add the NOAA event-study reference / our own prior methodology notes.)
