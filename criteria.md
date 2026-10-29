# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Clearly-AI and clearly-human text score far apart

In each of 3 trials, the combined score for `sample/clearly_ai.json` is at
least **0.30 higher** than the combined score for `sample/clearly_human.json`,
and `sample/clearly_human.json` **never** receives the high-confidence AI label
in any trial.

**Why this target:** If the two clearest cases the system will ever see land
close together, there is no room between them for an "unsure" band, and every
label is close to a coin flip. The second half keeps the expensive mistake in
view: if plainly human writing can be accused, anyone can.

---

## 2. Every label is reachable, with no gaps

`scoring.label_ranges()` shows the three label ranges covering 0.0–1.0 with no
gaps and no overlaps. Combined scores of 0.51 and 0.95 produce **different**
labels. Across 9 fixed inputs (the 3 `sample/` files plus 6 I choose), each of
the three labels appears **at least 2 times** in every one of 3 trials.

**Why this target:** A label nothing ever reaches is a decision the system
can't actually make. A single flip at 0.5 would treat barely-AI and certainly-AI
text the same.

---

## 3. Every appeal is recorded and changes status

For **5 of 5** appeals sent with a real `content_id` and a reason, `/appeal`
returns 200, and `GET /log` shows a new entry with `event: "appeal"` and
`status: "under_review"` that appears *after* the original decision, with the
original decision entry unchanged. An appeal with a `content_id` that doesn't
exist returns **404** and writes **no** appeal entry.

**Why this target:** The appeal is the only recourse for a wrongly flagged
writer. If even one appeal fails silently, that person stays accused with no
record that they objected.

---

## 4. Malformed submissions are refused, never crash

All 5 of these requests to `/submit` return **400** with
`"error": "bad_request"`, and **0** return 500: no `text` field, `text: ""`,
`text: "   "`, `text: 12345`, and a body that isn't JSON. `/ping` still answers
afterward.

**Why this target:** A crash on malformed input is one of the most common real
failures. A writing site that sends a bad request should get a clear refusal,
not a broken service.

---

## 5. Enormous text is rejected, not half-scored

A `/submit` with **100,000 characters** of text returns within **30 seconds**
with **413** and `"error": "too_large"`, and a rejection entry appears in the
log. Text up to **20,000 characters** is still accepted.

**Why this target:** The detector only reads the first 400 tokens. Without a
limit, a huge submission would be judged on a fraction of its text while looking
like a full verdict, and it can tie up the service for everyone else.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
