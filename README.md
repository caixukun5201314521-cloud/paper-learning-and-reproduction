# Paper Learning & Code Reproduction

A paper-by-branch learning repository. Each branch corresponds to one paper and contains: the original PDF, a Chinese full translation, reproduction code, data-acquisition guides, and running results.

**Current branch: `unifying-data-effectiveness-assessment`**

## Paper

> **Unifying Data Effectiveness Assessment in User Churn Detection: An Indicator-Assisted Framework**
> Mengying Zhou, Qianyu He, Bruno Abrahao, Xin Wang, Yang Chen
> *Tsinghua Science and Technology*, Vol. 31, No. 4, pp. 2237–2250, 2026. DOI: 10.26599/TST.2024.9010230

INFO (INdicator-assisted FramewOrk) uses five interpretable **prior** indicators — activity periodicity, activity diversity, linguistic, graph structure, and interaction sentiment — to assess how effective each data category is for user-churn detection *before* running large-scale model trials.

## Repository layout

```
paper/        Original paper PDF (open access, CC BY 4.0; cite DOI when redistributing)
docs/         Full Chinese translation (formulas reconstructed from garbled PDF text)
code/         smoke_test.py (toolchain self-check) · foursquare_indicators.py (prior indicators)
              foursquare_profile.py (full data audit)
results/      Indicator results vs. paper Table 3 · complete daily series · data audit
              data_cleaning_reflections.md (lessons learned, English)
data/         Acquisition guides for all five datasets + 1000-row Foursquare samples
requirements.txt  Python dependencies
```

## Environment setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python code/smoke_test.py   # 7-part toolchain self-check
```

Note: NLTK's punkt tokenizer needs a one-time download. If `nltk.download` is blocked by its
SSRF guard (proxy fake-IP), fetch `punkt.zip` / `punkt_tab.zip` via curl and unzip into
`~/nltk_data/tokenizers/`.

## Data note (important)

**Raw datasets are NOT committed.** Reasons: (1) `socialgraph.dat` alone is 827 MB, far above
GitHub's 100 MB per-file limit; (2) the Foursquare (UMN/Sarwat) dataset was taken down at the
platform's request in 2013, so redistributing it is legally risky. Local raw copy lives in
`~/Downloads/201309_foursquare_dataset_umn/`; acquisition channels for all five datasets are
documented in [data/README.md](data/README.md); 1000-row samples are included for smoke-testing.

## Progress

- [x] Close reading + full Chinese translation of the paper
- [x] Indicator toolchain setup (pandas / scipy / networkx / sklearn / vaderSentiment / nltk)
- [x] Foursquare data acquisition & format audit (span 2011-12 ~ 2012-04, matches paper's "5 months")
- [x] Wikipedia & Airbnb public data sources confirmed (SNAP main.bz2; Inside Airbnb / Kaggle)
- [x] **Prior indicators computed on Foursquare** — see [results/Foursquare先验指标结果.md](results/Foursquare先验指标结果.md)
      Key finding: only 56 of 138 days were ever collected (pulsed crawling), which contaminates
      dataset-level periodicity; after decontamination the best granularity flips from week to day.
- [x] Full data audit + active-user subsample verification (users with ≥6 check-ins: 28,601 /
      250,270 — matches paper's 27,304 / 184,723 almost exactly)
- [x] [Data-cleaning reflections (English)](results/data_cleaning_reflections.md)
- [ ] Naive-LR posterior experiments; r_intra / r_inter validation

## Branching convention

One paper per branch, named by the paper title in lowercase-hyphenated form
(e.g., `unifying-data-effectiveness-assessment`), branched from the default branch.
