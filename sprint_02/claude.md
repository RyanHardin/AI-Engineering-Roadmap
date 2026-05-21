# Sprint 2 — Deeper API Skills

## Overview

Duration: 3 weeks — May 20 to June 9, 2026
Focus: Streaming, structured outputs, and function calling

## Scripts

- streaming_report.py — streams Claude's response token-by-token to the terminal
- structured_classifier.py — rebuilds classifier.py using Claude's structured output feature instead of prompting for JSON
- tool_use_agent.py — Claude autonomously decides when to call Python functions based on a user's question

## Carried Over from Sprint 1

- Add error handling to sprint_01/scripts/interview_chat.py
- Add error handling to sprint_01/scripts/classifier.py
- Write sprint_01/README.md with what was built and a sample terminal session

## Acceptance Criteria

### streaming_report.py

- Response streams token-by-token to the terminal
- Handles API errors gracefully with a clear error message
- Handles missing or unset ANTHROPIC_API_KEY before making any API call
- Model has a fallback default if .env value is missing

### structured_classifier.py

- Claude returns a guaranteed typed JSON schema on every call
- Handles API errors gracefully with a clear error message
- Handles missing or unset ANTHROPIC_API_KEY before making any API call
- Handles FileNotFoundError if the CSV is missing
- Handles empty CSV gracefully before sending to Claude
- Output directory is created if it doesn't exist
- Model has a fallback default if .env value is missing

### tool_use_agent.py

- Claude autonomously decides when to call a tool based on the user's question
- At least 3 callable Python functions defined
- Handles API errors gracefully with a clear error message
- Handles missing or unset ANTHROPIC_API_KEY before making any API call
- Handles empty user input without crashing
- Handles cases where Claude doesn't call a tool and responds directly
- Model has a fallback default if .env value is missing

## Key Concepts

- Streaming: receiving and displaying Claude's response incrementally\, chunk by chunk
- Structured outputs: API-enforced JSON schemas — Claude always returns the exact shape you define
- Function/tool calling: defining Python functions Claude can invoke autonomously
- Agentic behavior: Claude deciding when and how to act\, not just responding to prompts

## Resources

- Streaming: https://docs.anthropic.com/en/api/messages-streaming
- Structured outputs: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-consistency
- Tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
