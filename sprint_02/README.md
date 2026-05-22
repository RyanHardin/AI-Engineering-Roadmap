# Sprint 2 — Deeper API Skills

**Duration:** 3 weeks
**Focus:** Streaming, function calling, and structured outputs

---

## Structure

```
sprint_02/
├── scripts/
│   ├── streaming_report.py        # Week 1 — Script 1
│   ├── structured_classifier.py   # Week 2 — Script 2
│   └── tool_use_agent.py          # Week 3 — Script 3
├── data/
│   └── (input files used by scripts)
├── outputs/
│   └── (generated files)
└── README.md
```

---

## Scripts

### Script 1 — Live streaming report generator
Streams Claude's response token-by-token to the terminal instead of waiting for the full response.

---

### Script 2 — Structured output classifier
Rebuilds `classifier.py` from Sprint 1 using Claude's structured output feature — Claude returns a guaranteed, typed JSON schema on every call.

**Output:** `outputs/interviews_classified.csv`

---

### Script 3 — Tool-use agent
A script where Claude autonomously decides when to call Python functions you define based on a user's question.

---

## Setup

1. Activate the virtual environment from the project root: `source .venv/bin/activate`
2. Ensure `.env` is configured with `ANTHROPIC_API_KEY` and `ANTHROPIC_API_MODEL`
3. Run any script from the `sprint_02/` directory

---

## Learnings

*To be filled in as each script is completed — see sprint doc for full notes.*
