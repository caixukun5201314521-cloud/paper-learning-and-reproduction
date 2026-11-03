# Data-Cleaning Reflections: Reproducing INFO on the Foursquare (UMN Sarwat) Dataset

*Written while running the prior-trial indicators (Eqs. 1–7 of the paper) on the full local copy of the 2013-09 UMN/Sarwat Foursquare dataset (1,021,966 check-ins / 2,809,580 ratings / 27,098,472 friendship edges, 2011-12 ~ 2012-04). Every finding below is backed by numbers from our own runs; scripts: `code/foursquare_indicators.py`, `code/foursquare_profile.py`.*

## 1. Structural junk lines — and why guards must be explicit

The `.dat` files are PostgreSQL dumps with pipe-delimited padding. Beyond the two header lines, each file ends with:

- a `(1021966 rows)` footer line, and
- up to 16 extra lines listing unrelated tables (`table_name`, `api_accounts`, ...) appended after the footer.

**Lesson:** parsing by "skip first 2 lines" alone crashes or silently corrupts. We use three guards: skip blank lines, skip lines starting with `(`, and accept a row only if its field count matches the schema (`len(row) == 6` for check-ins). A parsing bug here explains the "one row with empty rating" we first mistook for dirty data — it was the footer.

## 2. Row order is insertion order, not time order

Raw rows jump across months (`2012-04-21 → 2012-04-22 → 2012-03-30 → 2011-12-09`). Any windowing or "first/last activity" logic requires an explicit `sort` on `created_at` first. Sorting is part of cleaning; forgetting it is silent.

## 3. Same-second duplicate check-ins

The platform allowed rapid re-check-ins. Example in the raw file (ids differ, everything else identical):

```
221963 | 1348362 | 7491 | ... | 2011-12-14 13:19:38
221962 | 1348362 | 7491 | ... | 2011-12-14 13:19:38
```

Dataset-wide: **5,704 duplicate groups, 5,845 surplus rows (0.57%)**. Effect is negligible at dataset level but inflates per-user daily counts (our most active user had 57 raw check-ins but only 28 distinct active days). Decide explicitly — deduplicate or keep — and document the choice; the paper is silent on this.

## 4. Cleaning vs. feature selection vs. annotation — three different things

- Empty `latitude/longitude` columns: **not cleaned** — simply not used. Choosing which columns feed an indicator is selection, not repair.
- The 82 zero days (Section 6): **cannot be cleaned** — they are a property of how the data was collected. The only honest treatments are annotation (flag them), exclusion (drop zero days), or restriction (longest contiguous window). Each changes the answer; we report all three.

## 5. Zero-filling the calendar is load-bearing

A daily count series must span every calendar day from first to last activity, filling absent dates with 0 (`Counter.get(date, 0)` over a date range). Without it, "windows" misalign and segment correlations are meaningless. This is the single easiest step to get wrong when bucketing event logs.

## 6. A bug we actually shipped, and the sanity check that caught it

In a dedup path we forgot to truncate `2012-04-21 02:08:07` to its date part, so every timestamp became its own "day" key. The resulting series was **all zeros** and φ came back `nan` — no exception, no warning. Two habits now enforced in our scripts:

1. **Print intermediate sanity numbers before computing** (non-zero day counts, total events consumed, users seen). For the fixed run: 28 active days, and the weekly buckets `5+0+4+0+0+0+2+4+...` sum back to 28 — the aggregate reconciles with the raw count.
2. **Treat `nan` as a signal, not an error**: it means "fewer than 2 windows" or "zero-variance segment", which is informative (e.g., a 56-day series has no valid monthly window). Returning `nan` explicitly is more honest than coercing it to 0.

## 7. The big one: collection is pulsed, not continuous

Plotting the complete daily series (`results/foursquare_daily_series.csv`) showed **only 56 of 138 days contain any check-in**; the other 82 days are zero, grouped into ~8 bursts (longest contiguous active stretch: 18 days, 2012-04-06 ~ 04-23; then 9, 7, 6...). This matches the dataset's provenance ( intermittent crawling of check-ins shared on Twitter): **zeros mean "the collector did not crawl", not "users did not check in".**

Consequences for periodicity (Eq. 1–3), quantified:

| Variant | Series | φ_day | φ_week | φ_month | Best granularity |
|---|---|---|---|---|---|
| A: raw (zeros kept) | 138 days | 0.2853 | 0.2895 | 0.1866 | week |
| B: zero days dropped | 56 days | 0.3765 | 0.2598 | N/A | day |
| C: longest contiguous window | 18 days | 0.6088 | 0.0499 | N/A | day |

Shared zero runs inflate inter-segment correlations, and 7-day zero blocks fabricate week-scale similarity. After removing the contamination the best granularity flips from **week to day**, so our initial "qualitatively consistent with the paper (weekly)" claim was retracted in the results report. The genuinely robust weekly evidence is the weekend effect in weekday means (Sat 25,871 / Sun 22,795 / Fri 20,087 vs. Wed 9,880), with the caveat of only 5–10 valid days per weekday.

**Lesson: profile the complete time axis before trusting any periodicity number.** This step is absent from the paper; its 27,304-user subsample may or may not have avoided the issue.

## 8. Population structure explains the paper's numbers

57.5% of all users (279,016) have exactly one check-in; mean is 2.11 check-ins/user. Users with ≥6 check-ins: **28,601 users / 250,270 check-ins — almost exactly the paper's Table 2 (27,304 users / 184,723 records)**. The paper clearly works on an active-user subsample (~5–6 check-in threshold, plus undisclosed filters). Reproducing on the full population is not comparable.

Even after subsampling + deduplication, our dataset-level φ remains above the paper's 0.112, and a per-user test (top user: φ ≈ 0.23–0.27) narrows but does not close the gap — pointing to user-level computation averaged over users, or phase alignment, as the remaining undisclosed details.

## 9. Takeaway checklist (what we would do first next time)

1. Plot/print the complete daily activity curve — collection structure first, behavior second.
2. Reconcile row counts: file lines vs. parsed rows vs. aggregate sums, every time.
3. Classify each intervention as cleaning (repair), selection (ignore), or annotation (flag) — they get different documentation.
4. Write guards for schema length and footer junk before writing any real logic.
5. Sort by time before any windowing.
6. Quantify duplicates; make the keep/drop decision explicit and reproducible.
7. Treat `nan` as information; never silently coerce it.
8. Match the paper's sample definition before comparing any number to the paper.
