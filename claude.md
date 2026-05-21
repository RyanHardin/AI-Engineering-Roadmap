# AI Engineering Roadmap

## About

Full stack developer transitioning to AI engineering. Working through a 12-18 month roadmap broken into structured sprints. The goal is to build real AI engineering skills while validating and building different software products.

## Repo

https://github.com/RyanHardin/AI-Engineering-Roadmap

## Stack

- Language: Python
- Editor: VS Code
- LLM: Claude via Anthropic SDK
- One .venv at the repo root shared across all sprints
- API keys stored in .env at the repo root — never committed

## Structure

```
ai-engineering/
├── .venv/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── CLAUDE.md
├── sprint_01/
├── sprint_02/
└── resources/
```

## How to Work With Me

- I write all scripts myself — do not write code unless I explicitly ask
- When I share code for review\, give honest feedback on bugs\, code quality\, naming conventions\, and patterns I should know
- Be direct and specific — I am learning and need real feedback\, not validation
- When I am stuck\, help me understand the why behind the fix\, not just the fix itself
- Ask questions if something is unclear before giving advice

## Conventions

- Python file and folder names use snake_case
- One .venv at the root — no separate environments per sprint
- Error handling on every script
- No hardcoded API keys — always use os.getenv() with a fallback default for model names
