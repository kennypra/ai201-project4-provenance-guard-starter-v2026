# Extra criteria checks — before

- Produced by: `run_eval_extra.py::main`
- 3 trials · 2026-11-10 23:12

## Criterion 2 — checked in code

```json
{
  "label_ranges": [
    [
      "high-confidence human",
      "0.00 \u2013 0.35"
    ],
    [
      "unsure",
      "0.35 \u2013 0.65"
    ],
    [
      "high-confidence AI",
      "0.65 \u2013 1.00"
    ]
  ],
  "label_at_0.51": "unsure",
  "label_at_0.95": "ai"
}
```

## Trial 1

```json
{
  "criterion_3_appeals": {
    "appeals": [
      {
        "submit_status": 200,
        "content_id": "c_f74310247ba0",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_f74310247ba0",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_fcee0807cd42",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_fcee0807cd42",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_e1a9acfc7acb",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_e1a9acfc7acb",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_9628fd65cffa",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_9628fd65cffa",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_3c391ce3360b",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_3c391ce3360b",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      }
    ],
    "unknown": {
      "content_id": "c_eval_missing_t1",
      "status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id \"c_eval_missing_t1\"."
      },
      "new_log_entries": [
        {
          "creator_id": "unknown",
          "detail": "unknown content_id",
          "event": "rejected",
          "reason": "not_found",
          "requested_content_id": "c_eval_missing_t1",
          "route": "/appeal",
          "status": "rejected",
          "timestamp": "2026-11-11T05:12:45+00:00"
        }
      ],
      "appeal_entries_written": 0
    }
  },
  "criterion_4_non_json": {
    "status": 400,
    "response": {
      "error": "bad_request",
      "message": "Send JSON with a non-empty \"text\"."
    },
    "ping_after": 200
  },
  "criterion_5_timed": {
    "chars": 100035,
    "status": 200,
    "seconds": 0.32,
    "error": null,
    "guess": "ai",
    "log_entries_for_creator": [
      {
        "event": null,
        "reason": null,
        "guess": "ai",
        "status": "decided"
      }
    ]
  }
}
```

## Trial 2

```json
{
  "criterion_3_appeals": {
    "appeals": [
      {
        "submit_status": 200,
        "content_id": "c_b5bcf1d538e5",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_b5bcf1d538e5",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_c618451d9edc",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_c618451d9edc",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_f735564cdc13",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_f735564cdc13",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_fd99ca524af7",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_fd99ca524af7",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_ca92dd6ad0a9",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_ca92dd6ad0a9",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      }
    ],
    "unknown": {
      "content_id": "c_eval_missing_t2",
      "status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id \"c_eval_missing_t2\"."
      },
      "new_log_entries": [
        {
          "creator_id": "unknown",
          "detail": "unknown content_id",
          "event": "rejected",
          "reason": "not_found",
          "requested_content_id": "c_eval_missing_t2",
          "route": "/appeal",
          "status": "rejected",
          "timestamp": "2026-11-11T05:12:45+00:00"
        }
      ],
      "appeal_entries_written": 0
    }
  },
  "criterion_4_non_json": {
    "status": 400,
    "response": {
      "error": "bad_request",
      "message": "Send JSON with a non-empty \"text\"."
    },
    "ping_after": 200
  },
  "criterion_5_timed": {
    "chars": 100035,
    "status": 200,
    "seconds": 0.29,
    "error": null,
    "guess": "ai",
    "log_entries_for_creator": [
      {
        "event": null,
        "reason": null,
        "guess": "ai",
        "status": "decided"
      }
    ]
  }
}
```

## Trial 3

```json
{
  "criterion_3_appeals": {
    "appeals": [
      {
        "submit_status": 200,
        "content_id": "c_f5824379a177",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_f5824379a177",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_5277f1fa40b8",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_5277f1fa40b8",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_475ec1bba245",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_475ec1bba245",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_5944a4c5e69a",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_5944a4c5e69a",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      },
      {
        "submit_status": 200,
        "content_id": "c_2849df4e3ffa",
        "appeal_status": 200,
        "appeal_response": {
          "content_id": "c_2849df4e3ffa",
          "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
          "original_guess": "unsure",
          "status": "under_review"
        },
        "log_entries_for_id": 2,
        "appeal_entry_after_decision": true,
        "appeal_entry_status": "under_review",
        "decision_status_unchanged": "decided"
      }
    ],
    "unknown": {
      "content_id": "c_eval_missing_t3",
      "status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id \"c_eval_missing_t3\"."
      },
      "new_log_entries": [
        {
          "creator_id": "unknown",
          "detail": "unknown content_id",
          "event": "rejected",
          "reason": "not_found",
          "requested_content_id": "c_eval_missing_t3",
          "route": "/appeal",
          "status": "rejected",
          "timestamp": "2026-11-11T05:12:46+00:00"
        }
      ],
      "appeal_entries_written": 0
    }
  },
  "criterion_4_non_json": {
    "status": 400,
    "response": {
      "error": "bad_request",
      "message": "Send JSON with a non-empty \"text\"."
    },
    "ping_after": 200
  },
  "criterion_5_timed": {
    "chars": 100035,
    "status": 200,
    "seconds": 0.35,
    "error": null,
    "guess": "ai",
    "log_entries_for_creator": [
      {
        "event": null,
        "reason": null,
        "guess": "ai",
        "status": "decided"
      }
    ]
  }
}
```
