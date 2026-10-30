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



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

### Signal two — the style signal

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

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

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
