# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 22:55
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_ea663b46cf88` | unsure | 0.500 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_7f7ec0b705cb` | unsure | 0.506 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_31b9ad117104` | unsure | 0.650 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_be7861c546df` | ai | 0.729 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_2d9e8a526959` | unsure | 0.352 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_c86324ab8cc6` | unsure | 0.461 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_a81c089d5066` | unsure | 0.593 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_9eb29b40ad41` | unsure | 0.500 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_2c835a51ed02` | ai | 0.684 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_2657d3c31448` | ai | 0.917 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_cf0a7cbdbe18` | ai | 0.712 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_6943119f2217` | ai | 0.854 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_b08c96014479` | ai | 0.855 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_70cc41828a18` | ai | 0.854 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_5bc1dfd02153` | ai | 0.854 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_f6a5449f9116` | ai | 0.821 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_b05db47fbd71` | ai | 0.714 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_613d7c44588f` | unsure | 0.500 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_74d9b55a27ca` | unsure | 0.558 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_2b19c3b5da8d` | unsure | 0.384 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_24d291b4c9f0` | ai | 0.674 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_5f4379a7da5d` | unsure | 0.559 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_99fc0058910f` | unsure | 0.518 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_f477d98bf8af` | ai | 0.687 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `c_1b941542c7ef` | unsure | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `c_0ea9017ec074` | unsure | 0.500 |  |
| MF05 | malformed | text is a very long single word | 200 | `c_4d3601d9193b` | ai | 0.999 |  |
| MF06 | malformed | text is emoji only | 200 | `c_97756afc96f8` | ai | 0.999 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_12da7b47d573` | ai | 0.953 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `c_58b07bddb428` | ai | 0.908 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_a7dbac6ec758` | unsure | 0.500 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c_e68c999c0b64` | unsure | 0.500 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_3c7330dd5c83` | unsure | 0.500 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_2862fe25d40a` | unsure | 0.500 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_4b3376d471a8` | unsure | 0.500 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_6fe1f03c17a8` | unsure | 0.500 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_42d4ace148f3` | unsure | 0.500 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_ea663b46cf88",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.8918,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_7f7ec0b705cb",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5058,
  "model_score": 0.5943,
  "style_score": 0.4173,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_31b9ad117104",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6498,
  "model_score": 0.6662,
  "style_score": 0.6333,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_be7861c546df",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.7294,
  "model_score": 0.6114,
  "style_score": 0.8474,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_2d9e8a526959",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3517,
  "model_score": 0.3212,
  "style_score": 0.3821,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_c86324ab8cc6",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4612,
  "model_score": 0.5727,
  "style_score": 0.3496,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_a81c089d5066",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5931,
  "model_score": 0.5862,
  "style_score": 0.6,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_9eb29b40ad41",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2452,
  "style_score": 0.9379,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_2c835a51ed02",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.6837,
  "model_score": 0.7042,
  "style_score": 0.6631,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_2657d3c31448",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9169,
  "model_score": 0.9792,
  "style_score": 0.8546,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_cf0a7cbdbe18",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.7122,
  "model_score": 0.6175,
  "style_score": 0.8069,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_6943119f2217",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8542,
  "model_score": 0.7387,
  "style_score": 0.9697,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_b08c96014479",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8545,
  "model_score": 0.8051,
  "style_score": 0.9039,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_70cc41828a18",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8539,
  "model_score": 0.8329,
  "style_score": 0.875,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_5bc1dfd02153",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8542,
  "model_score": 0.8005,
  "style_score": 0.908,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_f6a5449f9116",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.821,
  "model_score": 0.8814,
  "style_score": 0.7606,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_b05db47fbd71",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7139,
  "model_score": 0.8816,
  "style_score": 0.5462,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_613d7c44588f",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.3223,
  "style_score": 0.8252,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_74d9b55a27ca",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5577,
  "model_score": 0.4625,
  "style_score": 0.653,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_2b19c3b5da8d",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.3839,
  "model_score": 0.2044,
  "style_score": 0.5633,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_24d291b4c9f0",
  "creator_id": "attacker_PI03",
  "guess": "ai",
  "confidence": 0.6744,
  "model_score": 0.5943,
  "style_score": 0.7545,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_5f4379a7da5d",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5593,
  "model_score": 0.4998,
  "style_score": 0.6187,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_99fc0058910f",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5182,
  "model_score": 0.6401,
  "style_score": 0.3964,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_f477d98bf8af",
  "creator_id": "attacker_PI06",
  "guess": "ai",
  "confidence": 0.6871,
  "model_score": 0.5583,
  "style_score": 0.8159,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_1b941542c7ef",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_0ea9017ec074",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_4d3601d9193b",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.9988,
  "model_score": 0.9976,
  "style_score": 1.0,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_97756afc96f8",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9985,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_12da7b47d573",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "c_58b07bddb428",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.9083,
  "model_score": 0.9876,
  "style_score": 0.8289,
  "label": "This reads a lot like writing produced by an AI tool. Our check can be wrong, especially about plain, simple writing. If you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_a7dbac6ec758",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2395,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_e68c999c0b64",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0492,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_3c7330dd5c83",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_2862fe25d40a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_4b3376d471a8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_6fe1f03c17a8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_42d4ace148f3",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI tool wrote this. That isn't an accusation: lots of people's writing lands here. If you wrote it yourself, you can tell us, and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
