#!/usr/bin/env python3
"""
The parts of my five criteria that run_eval.py can't send.  <- UNIT 8, MILESTONE 3

    python app.py                                  # in one terminal
    python run_eval_extra.py --label before        # in another

run_eval.py only POSTs JSON bodies to /submit. Three of my checks need more:

    criterion 2   label_ranges() has no gaps; 0.51 and 0.95 get different
                  labels — checked in code, no service needed
    criterion 3   submit, then appeal the content_id that came back; check
                  /log shows the appeal after the decision, decision unchanged;
                  an unknown content_id gets 404 and no appeal entry
    criterion 4   a body that isn't JSON at all
    criterion 5   how long the 100,000-character request takes, and whether a
                  rejection entry appears in the log

Like run_eval.py, this records what came back and leaves the verdict to me.
"""

import argparse
import datetime as dt
import json
import sys
import time

import config
import scoring

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

APPEAL_TEXTS = [
    "I wrote this paragraph about my weekend myself. We went to the lake and it rained the whole time.",
    "This is my own summary of the chapter. The main character leaves home and regrets it by the end.",
    "Here is a short note I wrote for class about why I like cooking with my family on Sundays.",
    "My cover letter opening, written by me: I have worked in retail for three years and I am ready for more.",
    "A reflection I wrote: the group project was hard because we never agreed on a plan until the last day.",
]


def appeal_trial(requests, url, trial):
    """Criterion 3: 5 real appeals and 1 unknown one, then read the log."""
    results = {"appeals": [], "unknown": None}

    for i, text in enumerate(APPEAL_TEXTS, 1):
        creator = f"eval_appeal_t{trial}_{i}"
        sub = requests.post(f"{url}/submit", json={"text": text, "creator_id": creator}, timeout=90)
        content_id = sub.json().get("content_id") if sub.ok else None
        app = requests.post(f"{url}/appeal", json={
            "content_id": content_id,
            "reasoning": f"I wrote this myself (eval trial {trial}, appeal {i}).",
        }, timeout=30)
        entries = [e for e in requests.get(f"{url}/log", timeout=30).json()["entries"]
                   if e.get("content_id") == content_id]
        decision = next((e for e in entries if "event" not in e), None)
        appeal = next((e for e in entries if e.get("event") == "appeal"), None)
        results["appeals"].append({
            "submit_status": sub.status_code,
            "content_id": content_id,
            "appeal_status": app.status_code,
            "appeal_response": app.json() if app.content else None,
            "log_entries_for_id": len(entries),
            "appeal_entry_after_decision": bool(decision and appeal
                                                and entries.index(appeal) > entries.index(decision)),
            "appeal_entry_status": appeal.get("status") if appeal else None,
            "decision_status_unchanged": decision.get("status") if decision else None,
        })

    unknown_id = f"c_eval_missing_t{trial}"
    before = len(requests.get(f"{url}/log", timeout=30).json()["entries"])
    resp = requests.post(f"{url}/appeal", json={"content_id": unknown_id, "reasoning": "x"}, timeout=30)
    after_entries = requests.get(f"{url}/log", timeout=30).json()["entries"]
    new = after_entries[before:]
    results["unknown"] = {
        "content_id": unknown_id,
        "status": resp.status_code,
        "response": resp.json() if resp.content else None,
        "new_log_entries": new,
        "appeal_entries_written": sum(1 for e in new if e.get("event") == "appeal"),
    }
    return results


def non_json_trial(requests, url):
    """Criterion 4, fifth case: a body that isn't JSON."""
    resp = requests.post(f"{url}/submit", data="this is not json",
                         headers={"Content-Type": "text/plain"}, timeout=30)
    try:
        body = resp.json()
    except ValueError:
        body = resp.text[:200]
    ping = requests.post(f"{url}/ping", json={"message": "still up?"}, timeout=10)
    return {"status": resp.status_code, "response": body, "ping_after": ping.status_code}


def huge_trial(requests, url, trial):
    """Criterion 5: time the 100,000-character request and look for its log entry."""
    text = "The quick brown fox jumps over the lazy dog. " * 2223
    creator = f"eval_huge_timed_t{trial}"
    start = time.monotonic()
    resp = requests.post(f"{url}/submit", json={"text": text, "creator_id": creator}, timeout=90)
    seconds = round(time.monotonic() - start, 2)
    body = resp.json() if resp.content else {}
    entries = [e for e in requests.get(f"{url}/log", timeout=30).json()["entries"]
               if e.get("creator_id") == creator]
    return {
        "chars": len(text),
        "status": resp.status_code,
        "seconds": seconds,
        "error": body.get("error"),
        "guess": body.get("guess"),
        "log_entries_for_creator": [{k: e.get(k) for k in ("event", "reason", "guess", "status")}
                                    for e in entries],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    import requests

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    code_checks = {
        "label_ranges": scoring.label_ranges(),
        "label_at_0.51": scoring.score_to_label(0.51)[0],
        "label_at_0.95": scoring.score_to_label(0.95)[0],
    }
    print("criterion 2 (code):", json.dumps(code_checks))

    trials = []
    for trial in range(1, args.trials + 1):
        print(f"\ntrial {trial}")
        result = {
            "criterion_3_appeals": appeal_trial(requests, args.url, trial),
            "criterion_4_non_json": non_json_trial(requests, args.url),
            "criterion_5_timed": huge_trial(requests, args.url, trial),
        }
        a = result["criterion_3_appeals"]
        print("  appeals:", [x["appeal_status"] for x in a["appeals"]],
              "unknown:", a["unknown"]["status"])
        print("  non-JSON:", result["criterion_4_non_json"]["status"])
        print("  100k:", result["criterion_5_timed"]["status"],
              f"in {result['criterion_5_timed']['seconds']}s")
        trials.append(result)

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_extra_{stamp}{label}.md"
    lines = [
        f"# Extra criteria checks{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval_extra.py::main`",
        f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Criterion 2 — checked in code",
        "", "```json", json.dumps(code_checks, indent=2), "```", "",
    ]
    for n, result in enumerate(trials, 1):
        lines += [f"## Trial {n}", "", "```json", json.dumps(result, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
