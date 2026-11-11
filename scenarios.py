"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

def _sample(name: str) -> str:
    """The text of one of the sample/*.json files criterion 1 and 2 name."""
    import json
    from pathlib import Path
    path = Path(__file__).parent / "sample" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))["text"]


SCENARIOS = [
    {
        # Criterion 1: clearly_ai must score ≥ 0.30 above clearly_human in every
        # trial, and clearly_human must never get the AI label.
        "name": "score spread",
        "criterion": 1,
        "texts": [
            _sample("clearly_ai"),
            _sample("clearly_human"),
        ],
    },
    {
        # Criterion 2: 9 fixed inputs — the 3 sample files plus 6 chosen before
        # this run (2 from the unit 7 calibration notes, 4 new). Each label must
        # appear at least twice in every trial. The ranges/0.51/0.95 half of
        # the criterion is checked in code by run_eval_extra.py.
        "name": "label coverage",
        "criterion": 2,
        "texts": [
            _sample("clearly_ai"),
            _sample("clearly_human"),
            _sample("borderline"),
            # plain human writing (notes/m4-calibration.md)
            "My job is at a store. I work there five days a week. I like my boss. "
            "She is kind to me. The work is not hard but my feet hurt at the end of "
            "the day. I take the bus home. The bus is late most days. When I get "
            "home I cook dinner for my sister. Then I study English for one hour. "
            "I want to get a better job next year.",
            # lightly-edited AI (notes/m4-calibration.md)
            "Good time management really matters in today's fast-paced work "
            "environment. People who build strong organizational habits are better "
            "at meeting deadlines and they get less stressed. There are a few "
            "strategies that help. First, prioritize. Figure out the most important "
            "tasks and do them first so the critical stuff gets done. Second, cut "
            "down on distractions. Setting aside blocks of time for focused work is "
            "widely considered helpful. Finally, take regular breaks to keep your "
            "performance up.",
            # AI-style product copy
            "Our new water bottle combines sleek design with everyday practicality. "
            "Crafted from durable stainless steel, it keeps drinks cold for up to "
            "twenty-four hours and hot for up to twelve. The leak-proof lid ensures "
            "worry-free transport, while the ergonomic shape fits comfortably in any "
            "bag. Whether you are heading to the gym, the office, or the trail, this "
            "bottle is designed to keep up with your active lifestyle.",
            # casual human note
            "ok so the dishwasher is doing the thing again — the beeping, three "
            "times, then nothing. I tried the reset (hold start for like ten "
            "seconds?) and it worked for one load. One! Landlord says he'll 'send "
            "someone,' which last time meant his nephew, a YouTube video, and a "
            "wet floor. Anyway: if you're home Thursday, can you let them in? "
            "I'll owe you a coffee. Or two.",
            # AI-style explainer
            "Climate change is one of the most pressing challenges facing the world "
            "today. Rising global temperatures are causing more frequent extreme "
            "weather events, melting polar ice, and rising sea levels. Addressing "
            "this issue requires coordinated action from governments, businesses, "
            "and individuals. Key strategies include transitioning to renewable "
            "energy, improving energy efficiency, and protecting natural ecosystems. "
            "By working together, we can build a more sustainable future.",
            # human personal anecdote
            "My grandfather kept bees for forty years and never once wore the suit. "
            "He said they could smell fear, and that he'd run out of it around 1971. "
            "I believed him until I was twelve, when I watched him get stung on the "
            "eyelid, say a word I wasn't allowed to repeat, and keep working. That "
            "was the summer I understood he was brave, and also that bravery mostly "
            "looks like being too stubborn to stop.",
        ],
    },
    {
        # Criterion 4: these four must each return 400 bad_request, never 500.
        # Each has its own creator_id so the rate limit counts them per creator,
        # not against one shared address. The fifth case — a body that isn't
        # JSON — can't be written as a dict; run_eval_extra.py sends it.
        "name": "bad input",
        "criterion": 4,
        "bodies": [
            {"creator_id": "eval_bad_missing"},               # no text field
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   ", "creator_id": "eval_bad_spaces"},
            {"text": 12345, "creator_id": "eval_bad_number"},
        ],
    },
    {
        # Criterion 5: 100,000 characters must get 413 too_large; 20,000 must
        # still be accepted. Timing and the log entry are checked by
        # run_eval_extra.py.
        "name": "enormous text",
        "criterion": 5,
        "bodies": [
            {"text": "The quick brown fox jumps over the lazy dog. " * 2223,  # ~100,000 chars
             "creator_id": "eval_huge_100k"},
            {"text": "The quick brown fox jumps over the lazy dog. " * 445,   # ~20,000 chars
             "creator_id": "eval_huge_20k"},
        ],
    },

    # Criterion 3 (the appeal path) needs a submission and then an appeal
    # against the content_id that came back, so it can't be a scenario here.
    # run_eval_extra.py tests it, three trials, against the same service.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
