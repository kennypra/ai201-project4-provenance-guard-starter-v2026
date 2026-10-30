# Milestone 4 — calibration run

Both signals on five inputs, run directly through the functions (not the
service, so nothing was logged). Weights and anchors as in `config.py` at the
time of the run.

| Input | model | style | gap | combined | spread | punct |
|---|---|---|---|---|---|---|
| clearly AI (`sample/clearly_ai.json`) | 0.754 | 0.703 | 0.05 | 0.729 | 0.41 | 0.054 |
| clearly human (`sample/clearly_human.json`) | 0.445 | 0.012 | 0.43 | 0.228 | 1.13 | 0.117 |
| borderline (`sample/borderline.json`) | 0.349 | 0.523 | 0.17 | 0.436 | 0.47 | 0.090 |
| plain human (written by Claude to imitate a plain writer) | 0.823 | 0.822 | 0.00 | 0.822 | 0.44 | 0.000 |
| lightly-edited AI (clearly_ai with contractions, simpler words) | 0.700 | 0.640 | 0.06 | 0.670 | 0.51 | 0.051 |

Raw measures on the samples, before scaling:

| Sample | sentence_length_spread | type_token_ratio | punctuation_density |
|---|---|---|---|
| clearly_ai | 0.41 | 0.85 | 0.054 |
| borderline | 0.47 | 0.79 | 0.090 |
| clearly_human | 1.13 | 0.73 | 0.117 |

## What it showed

- **Split case:** clearly human — model 0.445 vs style 0.012. Cap applied but
  had no effect (average already 0.228).
- **Shared blind spot:** plain human writing scores ~0.82 on both signals and
  would get the high-confidence AI label at the current 0.65 threshold.
  Decision: documented as a known failure rather than tuned away.
- **Criterion 1 (one run):** 0.729 − 0.228 = 0.50 ≥ 0.30, and clearly_human is
  not in the AI band. Unit 8 needs it across three trials.
- **Label check:** 0.51 → unsure, 0.95 → ai. No single flip at 0.5.

## Plain human text used

> My job is at a store. I work there five days a week. I like my boss. She is
> kind to me. The work is not hard but my feet hurt at the end of the day. I
> take the bus home. The bus is late most days. When I get home I cook dinner
> for my sister. Then I study English for one hour. I want to get a better job
> next year.

## Lightly-edited AI text used

> Good time management really matters in today's fast-paced work environment.
> People who build strong organizational habits are better at meeting deadlines
> and they get less stressed. There are a few strategies that help. First,
> prioritize. Figure out the most important tasks and do them first so the
> critical stuff gets done. Second, cut down on distractions. Setting aside
> blocks of time for focused work is widely considered helpful. Finally, take
> regular breaks to keep your performance up.
