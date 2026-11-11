# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A writing site sends a piece of text; the service answers with a guess, a
score, a sentence the writer can read, and an ID they can appeal with.

1. **The request arrives** at `POST /submit` (`app.py::submit`) as JSON with
   `text` and `creator_id`. A missing, empty, whitespace-only or non-string
   `text`, or a body that isn't JSON, is refused here with `400 bad_request`
   before any scoring runs. A missing `creator_id` becomes `"unknown"`.
2. **Signal one** (`detector.py::model_signal`) runs gpt2 locally on the first
   400 tokens and turns how predictable the text is into a 0–1 `model_score`.
3. **Signal two** (`stylometry.py::style_signal`) measures the text's shape —
   how much sentence length varies and how much mid-sentence punctuation it
   uses — and turns that into a 0–1 `style_score`.
4. **The combining rule** (`scoring.py::combine_signals`) averages the two into
   one `combined_score`, capped at 0.5 when they disagree by more than 0.4.
5. **The label mapping** (`scoring.py::score_to_label`) turns that score into a
   `guess` (`human` / `unsure` / `ai`) and the full sentence a reader sees.
6. **The decision is logged** (`audit.py::log_decision`) to
   `logs/audit.jsonl` under a new `content_id` (`c_` + 12 hex characters),
   with both signal scores, the combined score, guess, label and
   `status: "decided"`.
7. **The response goes back** with `content_id`, `guess`, `confidence` (the
   combined score), `label`, `model_score` and `style_score`. If the writer
   disagrees, they send that `content_id` and their reasoning to `POST /appeal`,
   which adds an `under_review` entry beside the original decision.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2,
run locally). It computes perplexity — how surprised the model is by each next
word — over the first 400 tokens and squashes it onto 0–1, where low
perplexity (predictable) means a higher, more AI-like score.

**Why that might differ between human and AI writing:** A language model
writes by repeatedly picking a likely next word, so its output is text a model
finds easy to predict. People make odder word choices, take abrupt turns and
reach for the specific over the typical, which a model doesn't see coming.

**What it can't see:** Who actually wrote it. Predictability isn't authorship —
the signal rewards common words in short, ordinary sentences, and plenty of
people write that way: second-language writers, younger writers, anyone
writing plainly on purpose. My plain-writing paragraph scored 0.823 on this
signal, higher than the actual AI sample (0.754). It also misses the reverse:
ornate prose full of rare words scores as human whoever wrote it, and anything
after the first 400 tokens is never read.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading a word of it. Two
measures are scored: how much sentence length varies (standard deviation of
words per sentence ÷ the mean) and mid-sentence punctuation per word (commas,
semicolons, colons, dashes, parentheses, quotes). A third, type-token ratio
(unique words ÷ total words), is computed but not scored. Low variation and
little punctuation push the score toward AI.

**Why that might differ between human and AI writing:** Generated prose tends
toward even, mid-length sentences and tidy punctuation, because "most likely
next word" averages out the extremes. Human writing is lumpier — a three-word
sentence next to a forty-word one, dashes and asides. On the samples, the human
text's spread was 1.13 against the AI text's 0.41.

**What it can't see:** Meaning. Anything that changes the shape without
changing the substance moves it — breaking sentences up, adding dashes or
commas, pasting in a quotation — which is cheap to do on purpose to AI text. It
also shares signal one's blind spot from the other side: plain writing has even
sentences and few commas, so my plain-writing paragraph scored 0.822 here too.
The two signals measure different properties but agree on the same wrong
answer for that writer.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two signals equally. If they disagree by more than
0.4, the combined score is capped at 0.5 — one signal on its own is never
enough to call someone's writing AI.

**The numbers:** (all in `config.py`)

- Combining: `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`,
  `DISAGREEMENT_GAP = 0.4`, `DISAGREEMENT_CAP = 0.5`
- Style signal (`stylometry.py::style_signal`): two measures, each put on 0–1
  with a straight line between an AI anchor and a human anchor, clipped at the
  ends, then weighted:
  - sentence length spread (stdev ÷ mean of words per sentence): 0.2 → 1.0
    (AI), 1.0 → 0.0 (human); weight `WEIGHT_SPREAD = 0.6`
  - punctuation density (commas, semicolons, colons, dashes, parentheses and
    quotes per word): 0.02 → 1.0 (AI), 0.12 → 0.0 (human); weight
    `WEIGHT_PUNCT = 0.4`
  - type-token ratio is measured but not scored: it shrinks with text length,
    and on the samples it pointed the wrong way (the AI sample had the most
    varied vocabulary).

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

`sample/clearly_human.json`: model signal 0.445 (close to a coin flip — the
vocabulary is ordinary), style signal 0.012 (sentence lengths vary wildly,
lots of dashes and commas). The gap is 0.43, so the cap applies, but the
average is already 0.228 — under the cap — so the cap changes nothing here and
the text lands in high-confidence human. The cap only bites when the average of
a split is above 0.5, which none of my calibration inputs reached.

**A case where both signals are wrong together:** a plainly written human
paragraph (short sentences, simple words, no commas) scored 0.823 on the model
signal and 0.822 on style — combined 0.822, the most "AI" of all five
calibration inputs. Both signals reward the same thing: plain, even writing.
Combining them can't fix a blind spot they share. Left as a known failure.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 (0.35 itself counts as human) | We think a person wrote this. Nothing in the writing looked like it came from an AI tool. |
| unsure | above 0.35, below 0.65 | We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look. |
| high-confidence AI | 0.65 – 1.00 (0.65 itself counts as AI) | This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it. |

Ranges come from `scoring.label_ranges()` and the thresholds in `config.py`
(`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.65`). Each label was reached by a
real submission: `sample/clearly_human.json` → human (0.228),
`sample/borderline.json` → unsure (0.436), `sample/clearly_ai.json` → AI
(0.729).

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says outright that it isn't an accusation, and that landing here is common,
because the person reading it most likely wrote every word. It ends on what
they can do rather than on the doubt. The AI label also admits it can be wrong
and names plain writing specifically, because that is the writing my own
calibration run wrongly scored as AI.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

A plainly written human paragraph — the false positive from my calibration
run — getting the high-confidence AI label, then appealed.

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "My job is at a store. I work there five days a week. I like my boss. She is kind to me. The work is not hard but my feet hurt at the end of the day. I take the bus home. The bus is late most days. When I get home I cook dinner for my sister. Then I study English for one hour. I want to get a better job next year.", "creator_id": "plain_writer"}'
```

```json
{
  "confidence": 0.8223,
  "content_id": "c_b41eb44ab560",
  "creator_id": "plain_writer",
  "guess": "ai",
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "model_score": 0.8229,
  "style_score": 0.8218
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_b41eb44ab560", "reasoning": "I wrote this myself. English is my second language, so I keep my sentences short and simple on purpose."}'
```

```json
{
  "content_id": "c_b41eb44ab560",
  "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
  "original_guess": "ai",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8223,
      "content_id": "c_b41eb44ab560",
      "creator_id": "plain_writer",
      "guess": "ai",
      "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
      "model_score": 0.8229,
      "status": "decided",
      "style_score": 0.8218,
      "timestamp": "2026-10-30T20:50:58+00:00"
    },
    {
      "content_id": "c_b41eb44ab560",
      "creator_id": "plain_writer",
      "event": "appeal",
      "reasoning": "I wrote this myself. English is my second language, so I keep my sentences short and simple on purpose.",
      "status": "under_review",
      "timestamp": "2026-10-30T20:50:58+00:00"
    }
  ]
}
```

The original decision is left exactly as it was; the appeal is a new entry
after it. An appeal for a `content_id` that doesn't exist returns `404
not_found` and writes nothing; one with no `reasoning` returns `400
bad_request`.

---

## How I Used AI

I used Claude Code (Claude Opus) throughout this unit, inside VS Code, with
access to the repo.

**Moment 1 — getting `/submit` to work (Milestone 3)**

- *What I asked for:* What wasn't working in my first version of `/submit`,
  and then help getting it right.
- *What came back:* It pointed out a missing comma (a syntax error that took
  the whole service down, `/ping` included), `uuid4().hec` instead of `.hex`,
  and a slice of `[::12]` that gave about 3 characters instead of 12. It also
  caught that I called the detector *before* checking the input, so a missing
  `text` would crash with a 500 instead of returning my 400, and that the
  response still sent back `"content_id": "hardcoded"`, so a writer would have
  nothing to appeal with.
- *What I changed:* I fixed the comma and the `.hex` typo myself; Claude
  reordered the validation, fixed the slice and returned the real ID. Then it
  ran curl against missing and blank text to show both now return 400.

**Moment 2 — getting `test.py` to pass (setup)**

- *What I asked for:* Help passing `python test.py` before the first class.
- *What came back:* Two failures with one cause. My `.venv` had been built
  from Anaconda's Python 3.9, which was first on my PATH, so
  `python3 -m venv` picked it up. The course needs 3.11+, and the same old
  Python is why `app.py` wouldn't import: its `str | None` type hints only work
  from 3.10. Claude found Python 3.12 already on my Mac, rebuilt `.venv` with
  `python3.12 -m venv`, reinstalled `requirements.txt` and downloaded the
  detector model. `test.py` went to 9 passed, 0 failed.
- *What I changed:* No starter code. The fix was the environment. I learned
  that `python3` on my machine means Anaconda's 3.9, so I activate `.venv`
  before running anything and check `python --version` says 3.12.

### Unit 8

**Moment 3 — diagnosing the attack run (Milestone 4)**

- *What I asked for:* Verdicts for my five criteria, then a stage and
  mechanism for every miss and broken attack.
- *What came back:* Instead of guessing from the attack names, Claude re-ran
  signal two's two parts on each broken attack's text. That overturned two of
  the attack set's own "targeting" labels. EV01 (typos) was aimed at signal
  two, but my signal two scored it *more* AI (0.89); the typos fooled signal
  one (0.16), and my disagreement cap then forced 0.5. It also showed that
  six of the seven false positives max out my punctuation measure, and that
  Arabic and emoji have zero "words" to signal two, so its edge-case defaults
  call them fully AI. It grouped the 21 failures into six patterns, 13 of them
  in signal two.
- *What I changed:* I decided not to implement an improvement this unit, and
  wrote up what I would change instead.

**Moment 4 — testing the appeal path (Milestone 3)**

- *What I asked for:* Run all five criteria three times.
- *What came back:* Claude pointed out that `run_eval.py` can only POST JSON
  to `/submit`, so it can't test an appeal (which needs a `content_id` from a
  submission first) or a body that isn't JSON. It wrote `run_eval_extra.py` to
  cover those, plus the timing and log checks for criterion 5. It also gave
  each bad-input body its own `creator_id`, so the rate limiter wouldn't turn
  my 400 tests into 429s the way it did for RQ10 and RQ11 in the attack run.
- *What I changed:* Nothing in the code; I used its results as written.

**What else Claude did this unit, so the record is complete:** it chose the
rate limits (5 a minute, 50 a day) and wrote their reasoning; it made
`/submit` and `/appeal` log their refusals, storing the requested id under
`requested_content_id` so a refusal can't be mistaken for a real submission;
it wrote the HELD/BROKE marking rules and marked all 56 attacks; it wrote the
six extra label-coverage inputs in `scenarios.py`; and it drafted the
verdicts, the diagnoses, What's Still Broken and the production trade above.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day (`config.py`: `RATE_LIMIT_PER_MINUTE`,
`RATE_LIMIT_PER_DAY`), on `POST /submit` only.

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer submits a piece, maybe revises and resubmits it, a few times an
hour. Five a minute leaves room for a quick retry or two without ever getting
in their way, and fifty a day is more than anyone checks their own work. A
script mapping my thresholds with 1,000 variations under one `creator_id`
would be stopped after 5 in its first minute and would need 20 days at 50 a
day. Each scoring call also runs gpt2 locally for a second or two, so a flood
costs real compute, not just log lines.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Per `creator_id` when the request has a non-empty one, per IP address otherwise
(`app.py::rate_limit_key`). The weakness: a script that invents a new
`creator_id` per request gets a fresh allowance every time, so the limit only
slows down a caller who keeps one identity. The address fallback has the
opposite problem: everyone behind one shared address shares one allowance.
Counts are kept in memory, so restarting the service resets them.

Every 429 is logged (`event: "rejected"`, `reason: "rate_limited"`), and so is
every request my own routes refuse (`reason: "bad_request"` or `"not_found"`).

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
$ python run_attacks.py --flood 15
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429

10 of 15 were rate limited.
Wrote results/flood_2026-11-10_2239.md
```

The log entry for one of those 429s:

```json
{"creator_id": "flood_tester", "event": "rejected", "limit": "5 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-11T04:39:07+00:00"}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

`python run_attacks.py --set attack_set --label before`, 56 attacks, service
restarted first so the rate-limit counters started at zero. Nothing in the
pipeline was changed before this run. Raw report:
`results/attack_run_2026-11-10_2255_before.md`; the run's audit entries:
`results/audit_attack_run_before.jsonl`.

**How I marked each one** — what the attack was trying to do, and whether it
got it:

| Family | BROKE when… | HELD when… |
|---|---|---|
| evasion (AI text, disguised) | it did **not** get the AI label. "Unsure" counts as broken: that label tells the reader it isn't an accusation, so the disguise worked | it got the AI label |
| false_positive (real human text) | it got the AI label — a real writer accused | it got human or unsure |
| prompt_injection | the instruction changed anything: the label text, the log, or the score in the direction asked | the pipeline treated it as ordinary text |
| malformed | the route crashed (5xx), or it gave a confident AI/human label to something that isn't readable prose | it was refused with a 4xx, or scored only as unsure |
| flood_same_creator | more than 5 got through in the minute | requests after the 5th got 429 |

**Totals: 36 HELD, 20 BROKE.**

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion | 10 | 3 | 7 |
| false_positive | 8 | 1 | 7 |
| prompt_injection | 6 | 6 | 0 |
| malformed | 20 | 14 | 6 |
| flood_same_creator | 12 | 12 | 0 |

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.500 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.506 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.650 | **BROKE** |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | ai | 0.729 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | unsure | 0.352 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.461 | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.593 | **BROKE** |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.500 | **BROKE** |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | ai | 0.684 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.917 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | ai | 0.712 | **BROKE** |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.854 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.855 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.854 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.854 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.821 | **BROKE** |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | ai | 0.714 | **BROKE** |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.500 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.558 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | unsure | 0.384 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | ai | 0.674 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.559 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.518 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | ai | 0.687 | HELD † |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | — | — | **BROKE** |
| MF03 | malformed | text is control characters | 200 | unsure | 0.500 | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.500 | HELD |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.999 | **BROKE** |
| MF06 | malformed | text is emoji only | 200 | ai | 0.999 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.953 | **BROKE** |
| MF08 | malformed | text is 60,000 characters | 200 | ai | 0.908 | **BROKE** |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.500 | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | unsure | 0.500 | HELD ‡ |
| RQ07 | malformed | body is a JSON array, not an object | 500 | — | — | **BROKE** |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | HELD * |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD * |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

**Notes on the marks**

- \* **RQ10 and RQ11 were stopped by the rate limiter, not by my validation.**
  They have no `creator_id`, so they counted against my address, which had
  already used its 5 a minute on earlier malformed rows. The request was
  refused, so they're marked HELD, but this run says nothing about how my route
  handles a form-encoded body.
- † **PI06: the injection did nothing, but the real human text in it got the
  AI label (0.687).** It's marked HELD against what the attack was trying to
  do; the accusation itself is the same failure as the false_positive family.
- ‡ **RQ06 didn't crash, but the object went into the audit log as the
  `creator_id`** (`{"id": "x"}`), so the log no longer has one string per
  creator.
- **The two crashes left no trace.** MF02 and RQ07 returned a 500 HTML
  debugger page, and neither has any entry in the audit log: the run sent 56
  requests and the log gained 54 lines.
- **Many 0.500 scores are the disagreement cap firing.** EV08, FP08, MF03,
  MF04, RQ02, RQ06 and every flood row have a signal-two score of about 0.82–1.0
  and a much lower signal one; the gap is over 0.4, so the combined score is
  capped at exactly 0.5.
- The flood family is 12 rows in the set, not the 20 its description says.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `logs/audit.jsonl` (also in `results/audit_attack_run_before.jsonl`), one
JSON object per line as written:

```json
{"timestamp": "2026-11-11T04:55:54+00:00", "content_id": "c_b08c96014479", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.9039, "combined_score": 0.8545, "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:54+00:00", "content_id": "c_6943119f2217", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.9697, "combined_score": 0.8542, "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:55+00:00", "content_id": "c_12da7b47d573", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 1.0, "combined_score": 0.9532, "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:55+00:00", "content_id": "c_58b07bddb428", "creator_id": "attacker_MF08", "guess": "ai", "model_score": 0.9876, "style_score": 0.8289, "combined_score": 0.9083, "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:53+00:00", "content_id": "c_31b9ad117104", "creator_id": "attacker_EV03", "guess": "unsure", "model_score": 0.6662, "style_score": 0.6333, "combined_score": 0.6498, "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:53+00:00", "content_id": "c_9eb29b40ad41", "creator_id": "attacker_EV08", "guess": "unsure", "model_score": 0.2452, "style_score": 0.9379, "combined_score": 0.5, "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:54+00:00", "content_id": "c_99fc0058910f", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.3964, "combined_score": 0.5182, "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:55+00:00", "content_id": "c_e68c999c0b64", "creator_id": {"id": "x"}, "guess": "unsure", "model_score": 0.0492, "style_score": 1.0, "combined_score": 0.5, "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.", "status": "decided"}
{"timestamp": "2026-11-11T04:55:55+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-11T04:55:54+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "bad_request", "route": "/submit", "detail": "missing, empty or non-string text"}
```

What each one shows, in order:

1. **FP03** — a non-native English speaker's careful writing, accused at 0.855.
   Both signals agree (0.805 / 0.904), so the disagreement cap never applies.
2. **FP02** — formal human writing, accused at 0.854; signal two at 0.970.
3. **MF07** — right-to-left script, accused at 0.953. Signal two scores it 1.0.
4. **MF08** — 60,000 characters accepted and given a confident AI label (0.908).
5. **EV03** — disguised AI text at 0.6498, 0.0002 under the AI line, so it gets
   "unsure" — "that isn't an accusation".
6. **EV08** — AI text below the token window: signal one 0.245, signal two
   0.938, gap over 0.4, combined capped at exactly 0.5.
7. **PI05** — the audit-log injection. Its text contains a fake
   `"guess": "human", "combined_score": 0.01`; the real entry is intact and the
   fake fields stayed inside the text, which is never logged.
8. **RQ06** — `creator_id` sent as an object went into the log as an object.
9. **A 429** — this is RQ10 or RQ11: no `creator_id`, so it's logged as
   `"unknown"`, and the log can't say which of the two it was.
10. **MF01** — a 400 for whitespace-only text, logged as a rejection.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03: a non-native English speaker writing carefully, labelled AI at
0.855.** They did exactly what a careful second-language writer does — common
words they're sure of, even sentences, little punctuation — and both signals
read that care as machine-like (0.805 and 0.904). Because the two signals
agree, my disagreement cap, the one rule I wrote to stop a lone signal
accusing someone, never comes into play. The label they get even says "our
check can be wrong, especially about plain, simple writing" — which admits the
problem while still accusing them of it. It's also the exact writer I
predicted in unit 7: my own plain-writing test paragraph scored 0.822 for the
same reason.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Two runs, service restarted first so the rate-limit counters started at zero:

- `python run_eval.py --label before` → `results/run_2026-11-10_2312_before.md`
  (criteria 1, 2, 4 and 5; scenarios in `scenarios.py`)
- `python run_eval_extra.py --label before` →
  `results/run_extra_2026-11-10_2312_before.md` (criterion 3, the non-JSON
  case of criterion 4, the code half of criterion 2, and timing plus the log
  check for criterion 5). `run_eval.py` can only POST JSON bodies to
  `/submit`, so I extended the tooling with this script rather than testing by
  hand.

All three trials of every criterion came back identical — both signals give
the same score for the same text, so there was no trial-to-trial instability.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Score spread | clearly_ai ≥ 0.30 above clearly_human every trial; clearly_human never AI | 0.7286 vs 0.2282 (gap 0.5004); human | 0.7286 vs 0.2282 (gap 0.5004); human | 0.7286 vs 0.2282 (gap 0.5004); human | **MET** |
| 2. Label coverage | no gaps; 0.51 ≠ 0.95; each label ≥ 2 of 9, every trial | ai 5 · human 2 · unsure 2; ranges 0–0.35 / 0.35–0.65 / 0.65–1; 0.51 unsure, 0.95 ai | same | same | **MET** |
| 3. Appeal path | 5/5 appeals 200 + `under_review` entry after decision, decision unchanged; unknown id → 404, no appeal entry | 5/5 200, all after decision, decision still `decided`; unknown 404, 0 appeal entries | same | same | **MET** |
| 4. Bad input | 5 malformed requests all 400 `bad_request`, 0 × 500, `/ping` still up | 5/5 400 (non-JSON body: `bad_request`); `/ping` 200 | same | same | **MET** |
| 5. Enormous text | 100,000 chars → 413 `too_large` within 30 s + rejection logged; 20,000 accepted | 100k: **200, ai 0.9986**, 0.32 s, logged as a decision; 20k: 200 | 100k: **200**, 0.29 s; 20k: 200 | 100k: **200**, 0.35 s; 20k: 200 | **MISSED** |

**How each verdict was decided.** A target had to hold in every trial; one
miss in any trial would make it MISSED.

1. **MET.** The gap was 0.5004 in all three trials, which is over 0.30, and
   clearly_human got the human label each time. This is weak evidence, though:
   it's the same two texts, the scores never vary, and the attack set's
   false_positive family shows plainer human writing gets accused — this
   criterion only tests one easy human text.
2. **MET.** In every trial the AI label appeared 5 times, human 2 and unsure
   2. `label_ranges()` covers 0–1 with nothing missing; the printed ranges
   share the 0.35 and 0.65 endpoints, but the code gives each endpoint to
   exactly one label (`<=` human, `>=` ai), so nothing overlaps in behavior.
   0.51 gives unsure and 0.95 gives ai. Human and unsure hit the minimum of 2
   exactly, with no margin.
3. **MET.** In all three trials, 5 of 5 appeals returned 200 and wrote an
   `under_review` entry after their decision, and every decision entry still
   read `decided`. The unknown id returned 404 and wrote 0 appeal entries. It
   does write a `rejected` entry, which the criterion doesn't forbid.
4. **MET.** In all three trials, all five requests returned 400 and none
   returned 500, and `/ping` answered afterwards. The non-JSON body's response
   says `"error": "bad_request"`. For the four JSON cases, `run_eval.py`
   doesn't record the error field, so I checked the audit log: each one has
   three `rejected` / `bad_request` entries, and `bad_request` is the only
   400 that `/submit` returns. The criterion is MET as written, but too
   narrow: the attack set crashed the route with two malformed inputs it
   didn't include (MF02, a single character; RQ07, a JSON array body).
5. **MISSED.** Two of its three parts held in every trial: the response came
   back within 30 seconds (0.29–0.35 s), and 20,000 characters were accepted.
   But 100,000 characters got **200** with an AI label (0.9986), not 413
   `too_large`, and the log has a decision for it, not a rejection. Nothing in
   `/submit` checks length, so this was never going to pass. The 413 check is
   a design decision I wrote into the criterion in unit 7 and didn't build.

**Criterion revisions:** none. All five could be measured as written, so
nothing in `criteria.md` changes. Criterion 5 is missed, not broken, so its
target stays where it is.

**Real output from one trial** (trial 1 of each). The JSON is as the tools
wrote it, except that `label` is removed and `sent` is shortened to keep it
readable.

*Criterion 1 — `run_eval.py::main`, scenario "score spread":*

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.7286, "model_score": 0.7544, "style_score": 0.7028,
   "sent": "The importance of effective time management cannot be overst"},
  {"status": 200, "guess": "human", "confidence": 0.2282, "model_score": 0.4445, "style_score": 0.0119,
   "sent": "I didn't sleep. Not properly, anyway — I lay there listening"}
]
```

*Criterion 2 — `run_eval.py::main`, scenario "label coverage":*

```json
[
  {"status": 200, "guess": "ai",     "confidence": 0.7286, "model_score": 0.7544, "style_score": 0.7028, "sent": "The importance of effective time management cannot be overst"},
  {"status": 200, "guess": "human",  "confidence": 0.2282, "model_score": 0.4445, "style_score": 0.0119, "sent": "I didn't sleep. Not properly, anyway — I lay there listening"},
  {"status": 200, "guess": "unsure", "confidence": 0.436,  "model_score": 0.3489, "style_score": 0.523,  "sent": "Time management matters more than people admit, especially n"},
  {"status": 200, "guess": "ai",     "confidence": 0.8223, "model_score": 0.8229, "style_score": 0.8218, "sent": "My job is at a store. I work there five days a week. I like "},
  {"status": 200, "guess": "ai",     "confidence": 0.6698, "model_score": 0.6998, "style_score": 0.6397, "sent": "Good time management really matters in today's fast-paced wo"},
  {"status": 200, "guess": "ai",     "confidence": 0.676,  "model_score": 0.8151, "style_score": 0.5369, "sent": "Our new water bottle combines sleek design with everyday pra"},
  {"status": 200, "guess": "human",  "confidence": 0.2038, "model_score": 0.2138, "style_score": 0.1938, "sent": "ok so the dishwasher is doing the thing again — the beeping,"},
  {"status": 200, "guess": "ai",     "confidence": 0.784,  "model_score": 0.9269, "style_score": 0.6412, "sent": "Climate change is one of the most pressing challenges facing"},
  {"status": 200, "guess": "unsure", "confidence": 0.5839, "model_score": 0.4506, "style_score": 0.7172, "sent": "My grandfather kept bees for forty years and never once wore"}
]
```

and the code half, `run_eval_extra.py::main`:

```json
{
  "label_ranges": [["high-confidence human", "0.00 – 0.35"], ["unsure", "0.35 – 0.65"], ["high-confidence AI", "0.65 – 1.00"]],
  "label_at_0.51": "unsure",
  "label_at_0.95": "ai"
}
```

*Criterion 3 — `run_eval_extra.py::appeal_trial`, the first of five appeals
and the unknown id:*

```json
{
  "submit_status": 200,
  "content_id": "c_f74310247ba0",
  "appeal_status": 200,
  "appeal_response": {"content_id": "c_f74310247ba0", "original_guess": "unsure", "status": "under_review"},
  "log_entries_for_id": 2,
  "appeal_entry_after_decision": true,
  "appeal_entry_status": "under_review",
  "decision_status_unchanged": "decided"
}
{
  "content_id": "c_eval_missing_t1",
  "status": 404,
  "response": {"error": "not_found", "message": "No submission with content_id \"c_eval_missing_t1\"."},
  "new_log_entries": [
    {"creator_id": "unknown", "detail": "unknown content_id", "event": "rejected", "reason": "not_found",
     "requested_content_id": "c_eval_missing_t1", "route": "/appeal", "status": "rejected",
     "timestamp": "2026-11-11T05:12:45+00:00"}
  ],
  "appeal_entries_written": 0
}
```

*Criterion 4 — `run_eval.py::main`, scenario "bad input", plus
`run_eval_extra.py::non_json_trial`:*

```json
[
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "{\"creator_id\": \"eval_bad_missing\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "(empty text)"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "   "},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"}
]
{"status": 400, "response": {"error": "bad_request", "message": "Send JSON with a non-empty \"text\"."}, "ping_after": 200}
```

`run_eval.py` records the status but not the `error` field. The `bad_request`
reason for the four JSON cases is in the audit log's rejection entries.

*Criterion 5 — `run_eval.py::main`, scenario "enormous text", plus
`run_eval_extra.py::huge_trial`:*

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.9986, "model_score": 0.9972, "style_score": 1.0, "sent": "The quick brown fox jumps over the lazy dog. The quick brown"},
  {"status": 200, "guess": "ai", "confidence": 0.9986, "model_score": 0.9972, "style_score": 1.0, "sent": "The quick brown fox jumps over the lazy dog. The quick brown"}
]
{"chars": 100035, "status": 200, "seconds": 0.32, "error": null, "guess": "ai",
 "log_entries_for_creator": [{"event": null, "reason": null, "guess": "ai", "status": "decided"}]}
```

The first is 100,035 characters, the second 20,025; both get the same score,
because signal one reads only the first 400 tokens of either.

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

21 failures in all: 20 BROKE attacks and 1 MISSED criterion. To find the
mechanisms I re-ran signal two's two parts on each broken attack's text after
the run. Sentence spread and punctuation density are each mapped to 0–1, with
1.0 meaning fully AI (`config.py` anchors). The 21 come down to **six
problems**.

| Failure | Pattern | Stage |
|---|---|---|
| FP01–FP07 (7) | A. Plain and formal human writing — both signals wrong together | signal one + signal two |
| MF05, MF06, MF07 (3) | B. Signal two scores "nothing to measure" as fully AI | signal two (+ route) |
| EV02, EV06, EV07 (3) | C. Signal two's two measures are cheap to game | signal two |
| EV01, EV08 (2) | D. Signal one reads it as human, the cap forces 0.5 | signal one + combining rule |
| EV03, EV05 (2) | E. Lands just inside the unsure band | label mapping (EV05: both signals) |
| MF02, RQ07, MF08, criterion 5 (4) | F. The route lets unchecked input through to the signals | the route |

**A. Plain and formal human writing — 7 false positives (FP01–FP07).**
Stage: signal one and signal two together; the combining rule can't help.
Every one scored between 0.71 and 0.86. Signal one was 0.62–0.88, because
plain and formal writing uses common words in ordinary order, which is what
gpt2 predicts best. Signal two was 0.55–0.97, and the reason is mostly my
punctuation anchor: six of the seven use fewer than one comma, dash, colon or
semicolon per 50 words (0.000–0.019 per word). My AI anchor is 0.02, so their
punctuation part is fully AI (1.0). Formal pieces also have even sentences
(spread 0.24–0.37 against an AI anchor of 0.2), so the spread part is
0.79–0.95 AI. Because the two signals agree, the gap never exceeds 0.4 and the
disagreement cap never applies. FP07 differs slightly: its deliberate
repetition ("It rained on Monday. It rained on Tuesday…") made signal one
0.88, because a repeated phrase is the most predictable text there is.
Mechanism: **both signals reward plain, even, lightly punctuated writing, and
careful human writers produce exactly that**. My punctuation anchor treats
"almost no commas" as the strongest AI evidence available. PI06's human text
(0.687) is the same failure.

**B. Signal two scores "nothing to measure" as fully AI — MF05, MF06, MF07.**
Stage: signal two, with the route letting it through.
A single long word, emoji only, and Arabic text all got signal two = 1.0 and
the AI label (0.95–0.999). `stylometry.words()` only matches `[a-z0-9']`, so
emoji and Arabic have **zero words**. With one sentence, spread can't be
measured and returns 0.0; with no words, punctuation density returns 0.0. Both
of those edge-case defaults sit at the AI end of my scale, so "I couldn't
measure anything" becomes "certainly AI". Signal one agreed (0.91–0.998)
because gpt2 is an English model and repeated byte patterns are predictable to
it. MF07 matters most: it's real writing in Arabic, and the system accused it
with near certainty using a measurement that never saw a single word of it.

**C. Signal two's measures are cheap to game — EV02, EV06, EV07.**
Stage: signal two.
- **EV02** broke AI text into more sentences of varied length: spread went to
  0.85, so the spread part fell to 0.19, signal two to 0.42, and the combined
  score to 0.506 (unsure).
- **EV06** added one very long and one very short sentence: spread 1.19, which
  is past my human anchor, so the spread part is 0.0, signal two 0.35, and the
  combined score 0.461.
- **EV07** padded with punctuation and ended up as a single "sentence": the
  spread part went to fully AI (1.0), but punctuation density of 0.227 drove
  the punctuation part to 0.0, so signal two was 0.60 and the combined score
  0.593.

Mechanism: **spread and punctuation count shape, not meaning**. Spread with
6–13 sentences moves a lot from one or two outliers. Each measure is a single
weighted term (0.6 and 0.4), so maxing one out moves signal two by up to that
much. Signal one alone (0.57–0.59) would have put all three in unsure anyway.
That is pattern E's band: they never got close to the AI line.

**D. Signal one reads it as human, and the cap forces exactly 0.5 — EV01,
EV08.** Stage: signal one, then the combining rule.
- **EV01 (typos)** was meant to fool signal two through word variety, but my
  signal two doesn't score word variety, and it read the text as *more* AI
  (0.89). The typos fooled **signal one** instead: misspelled words are rare
  tokens to gpt2, so it scored 0.16.
- **EV08 (two sentences, 10 words)** scored 0.245 on signal one, because
  perplexity over 10 words is noisy, and 0.94 on signal two, because short text
  has little spread and no punctuation.

In both, the gap is over 0.4, so the combined score is capped at exactly 0.5:
unsure. Mechanism: **the cap I wrote to stop one signal accusing a writer also
stops one signal accusing AI text**. Any change that pushes signal one low,
like typos or brevity, is enough to keep the AI label off. The same cap
produced the many 0.500 scores elsewhere in the run.

**E. Just inside the unsure band — EV03, EV05.** Stage: the label mapping
(EV05: both signals).
- **EV03** scored 0.6498, 0.0002 under my 0.65 AI line. The pasted quotation
  nudged both signals a little (0.666 and 0.633), because quotation marks
  count as punctuation and the quote changed sentence lengths. The label
  mapping uses a hard cutoff, so 0.6498 and 0.6502 get opposite labels. This
  is a threshold-edge outcome, not a strong evasion.
- **EV05**, a heavy human editing pass, moved both signals honestly (0.32 and
  0.38) to a combined 0.352, just above my 0.35 human line. After that much
  editing the text arguably *is* substantially human-written. I marked it
  BROKE by my rule, but it's the failure I'm least sure is a failure.

**F. The route lets unchecked input through — MF02, RQ07, MF08, and criterion
5.** Stage: the route (`app.py::submit`).
- **MF02 (`"a"`)** passed my non-empty check. `detector.perplexity` then
  raised `ValueError: Text is too short to score` (it needs 3+ tokens), and
  nothing catches it, so Flask returned a 500 HTML debugger page.
- **RQ07 (a JSON array body)** made `request.get_json()` return a list, and
  `payload.get("text")` raised `AttributeError: 'list' object has no attribute
  'get'` on the route's second line.

  Both crashes happen **before** `audit.log_decision` runs, so neither left an
  entry: 56 requests, 54 log lines. To my audit log they're invisible.
- **MF08 (60,000 characters)** and **criterion 5 (100,000 characters)** were
  accepted because `/submit` has no length check. Signal one read only the
  first 400 tokens and the response gave a confident AI label (0.908 and
  0.9986) as if it had judged the whole thing. The 413 I specified in criterion
  5 was never built.

**What the patterns say.** Most of the damage traces to **signal two** —
patterns A, B and C, 13 of 21 — and especially to two choices in it: the
punctuation anchor that calls lightly punctuated writing fully AI, and
edge-case defaults that point to AI when there's nothing to measure. The worst
outcomes (FP03, MF07) are both real writers accused. Pattern F is separate,
smaller and mechanical: the route trusts its input too much. Criterion 4 was
too narrow to catch it — it tested the malformed bodies I thought of, not a
one-character text or a JSON array.



---

## The Improvement

**What I changed:** Nothing. I chose not to implement an improvement this
unit, so the pipeline is exactly as it was for the "before" runs. The only
changes this unit are the rate limiter and the audit log (Milestone 1).

**Which diagnosis pointed at it:** None was applied. The one I'd have made is
in What's Still Broken below.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Not run. With no change made, an "after" run would repeat the "before" run.
Both signals give the same score for the same text, and every trial in
Milestone 3 came back identical.

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

There was no change to measure, so there's no evidence either way. Every
result in Attack Run — Before and Run Log and Verdicts still stands.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

Everything that broke is still broken: **20 attacks and 1 criterion**. I
stopped after diagnosing, without making a change. Grouped by the patterns in
Diagnoses:

| Still broken | What I'd do | Cost of doing it |
|---|---|---|
| **A.** FP01–FP07 — plain and formal human writing accused (0.71–0.86) | Move signal two's punctuation AI anchor well below 0.02 per word, or drop punctuation density, so "few commas" stops counting as the strongest AI evidence. Separately, cap the combined score below the AI line when the text is plain *and* both signals rely on predictability and evenness — the one kind of agreement I know is unreliable. | Clearly-AI text also has few commas (the sample is 0.054), so some AI text would slide from "ai" to "unsure". |
| **B.** MF05, MF06, MF07 — single long word, emoji, Arabic scored ~1.0 AI | Make signal two return "can't measure" instead of fully AI when it finds fewer than ~20 words or fewer than 2 sentences, and score that case as unsure. Match letters in any script, not just a–z. | Very short real submissions would always be unsure — which is already what happened to FP08, so little is lost. |
| **C.** EV02, EV06, EV07 — sentence splitting, one outlier sentence, punctuation padding | Use a robust spread measure (e.g. interquartile range instead of standard deviation, so one outlier can't swing it) and cap how far punctuation alone can move signal two. | Real human writing with genuinely uneven sentences gets less credit for it; slightly more false positives. |
| **D.** EV01, EV08 — typos and very short text push signal one low; cap forces 0.5 | Leave the cap. It's doing what I designed it to do: one signal alone doesn't get to decide. Let both through to unsure and rely on the appeal path. | Typo'd AI text stays unaccused. I'd accept that. |
| **E.** EV03 (0.6498), EV05 (0.352) | Leave them. EV03 is a threshold edge, and moving the line would just move the edge; EV05 may honestly be mostly human after heavy editing. | — |
| **F.** MF02, RQ07 — two crashes with no log entry | In `/submit`: reject any body that isn't a JSON object with 400, and catch the detector's "too short" error and return 400 — both logged with `audit.log_rejection`. | None I can see. This is the change I'd make first: it's mechanical, it can't hurt any other result, and right now two attacks are invisible in my audit log. |
| **F.** MF08 and **criterion 5 (MISSED)** — 60,000 and 100,000 characters accepted, scored on the first 400 tokens | Add the length limit criterion 5 already specifies: over 20,000 characters → 413 `too_large`, logged as a rejection. | Long genuine pieces have to be submitted in parts. |

**Why I stopped:** I chose to end the unit at the diagnosis and not make the
one allowed change.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I'd go toward fewer wrong accusations: widen what counts as unsure and fix
signal two's plain-writing bias, even though that lets more AI text through
as "unsure" — as seven of my ten evasion attacks already got through. The cost
falls on the site and on honest writers whose work sits next to undetected AI
text, which is a smaller harm than what FP03 shows: a careful second-language
writer accused with 0.855 confidence and left to argue their way out.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
