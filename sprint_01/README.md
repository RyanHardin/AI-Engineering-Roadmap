# Sprint 1 — Foundations

**Focus:** First real API calls, multi-turn conversations, and structured data workflows

Sprint 1 is where everything clicked for the first time. Starting from zero — no prior LLM API experience — I learned how to authenticate with the Anthropic SDK, manage message history for multi-turn conversations, and build scripts that take real CSV input and produce useful output. Each script builds on the last: raw API call → formatted report → interactive chat → automated classifier.

---

## Structure

```
sprint_01/
├── formatted_report_generator/
│   └── report_generator.py        # Script 1 — one-shot report generator
├── interview_chat/
│   └── interview_chat.py          # Script 2 — multi-turn chat over interview data
├── classifier/
│   └── classifier.py              # Script 3 — AI-powered CSV classifier
├── inputs/
│   └── customer_interviews.csv    # Shared input data
└── outputs/
    ├── interview_report_<date>.txt
    ├── interviews_classified.csv
    └── completed_interviews.csv
```

---

## Scripts

### `report_generator.py`

Reads `customer_interviews.csv`, sends the raw data to Claude with a structured prompt, and writes a formatted `.txt` report to `outputs/`. The report includes a date/filename header, a numbered list of top themes identified across interviews, and a one-sentence recommendation. This was the first script — a clean one-shot API call with no conversation history.

---

### `interview_chat.py`

Loads the same interview CSV and opens a persistent multi-turn chat session in the terminal. Claude summarizes the data on startup, then you can ask follow-up questions and dig into specific themes — the full message history is passed on every call, so context carries forward. Type `quit` or `exit` to end the session. This script introduced the concept of stateful conversation management.

---

### `classifier.py`

Sends the raw CSV to Claude and asks it to classify every row by adding three new labels: `category`, `severity`, and `software_opportunity`. Claude returns pure JSON, which is then parsed and written to `outputs/interviews_classified.csv`. This script introduced prompt engineering for structured output — specifically how to coerce Claude into returning machine-readable data with no markdown or explanation.

---

## Setup

1. Activate the shared virtual environment from the project root:
   ```bash
   source .venv/bin/activate
   ```
2. Ensure `.env` at the project root contains:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ANTHROPIC_API_MODEL=claude-opus-4-5
   ```
3. Run any script from its own directory:
   ```bash
   cd sprint_01/interview_chat
   python interview_chat.py
   ```

---

## Sample Terminal Session — `interview_chat.py`

```
$ python interview_chat.py

Here's a brief summary of the customer interviews:

The dataset covers 10 contacts across solar inspection and property management companies.
4 interviews are completed, 4 are scheduled, and 2 have not been contacted yet.
The main pain points cluster around manual report writing, inconsistent documentation quality,
and limited tracking or comparison capabilities. Of those who shared a pain point,
6 are willing to pay for a solution and 2 said maybe.

Enter your response (or 'quit' to exit): Which pain points came up the most?

The most frequently mentioned pain point is **manual report generation** — it showed up
in three separate interviews (John Martinez, Sarah Chen, and Amanda Foster). The common
thread is that creating inspection reports is time-consuming and done from scratch every time,
with no standardization across inspectors. The second cluster is around **client-facing
documentation** — both Lisa Rodriguez and Jennifer Lee mentioned that customers and insurers
are asking for detailed reports that their current process can't deliver.

Enter your response (or 'quit' to exit): Are any of the maybe responses worth following up on?

Yes — both "maybe" responses are worth a follow-up. Mike Thompson (Property Care Solutions)
said there's no good way to track panel performance over time. That's a clear product gap,
not a budget objection — his hesitation likely comes from uncertainty about whether the
solution would actually solve that specific problem. Emily White (Sun Inspect Solutions) needs
before/after comparison features for client reports. Same situation: she's not saying no,
she's saying "show me it does what I need." Both would probably convert with a targeted demo.

Enter your response (or 'quit' to exit): What should I prioritize building first based on this data?

Based on the pattern in the data, I'd prioritize **automated report generation with templates**
first. It's the highest-frequency pain point, it affects the largest segment (operations
managers and owners), and 100% of respondents who mentioned it said they'd pay. It's also
the most concrete — you know exactly what they want: stop writing reports from scratch,
make them consistent, make them fast. Tracking and comparison features are valid but they're
secondary — those respondents hedged on willingness to pay, which is a signal to validate
further before building.

Enter your response (or 'quit' to exit): quit

Ending session. Goodbye!
```

---

## Learnings

- **Message history is what makes a conversation.** Passing the full `messages` list on every API call is what gives Claude context. Without it, every turn would be a fresh request with no memory of what came before. Understanding this was the foundation for everything multi-turn.
- **Prompt engineering for structured output is about removing Claude's options.** When you tell Claude to return JSON with no explanation, no markdown, and no code fences, you're not just asking nicely — you're eliminating the behaviors you don't want. The cleaner the constraint, the more reliable the output.
- **Error handling at the API boundary matters from day one.** Building in `AuthenticationError`, `APIConnectionError`, and `RateLimitError` handling early made the scripts resilient to real-world conditions and set a pattern worth carrying forward.
