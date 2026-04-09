# Conversation Nervousness Analyzer

An AI agent that analyzes interview transcripts for nervousness signals using the Claude API. It detects filler words, deflection, and word repetition to produce a nervousness score with supporting evidence.

## Demo link: https://conversation-nervousness-analyzer-xtcp6vxsxu9zprife8pwnd.streamlit.app/

## How It Works

The analyzer uses a structured, three-step prompt sent to `claude-sonnet-4-6` at `temperature=0` for deterministic results:

**Step 1 — Context detection**: The model first identifies the type of conversation (e.g. technical interview, casual chat) to calibrate expectations.

**Step 2 — Signal analysis** across three dimensions:

| Signal | Weight | What counts |
|---|---|---|
| Filler words | 45% | *um, uh, like, you know, kind of, sort of,* etc. |
| Deflection | 10% | Intentionally avoiding a question without returning to answer it |
| Repeated words | 45% | Content words (nouns, verbs, adjectives) repeated enough to disrupt flow |

**Step 3 — Scoring**: Each signal is scored 0–1 relative to the identified context. A weighted average produces the final nervousness percentage.

The model returns structured JSON, parsed by `analyzer_transcript()` in [analyzer.py](analyzer.py) into a Python dict displayed via Streamlit.

## Running Locally

**Prerequisites**: Python 3.x and an [Anthropic API key](https://console.anthropic.com/) set as `ANTHROPIC_API_KEY` in your environment.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
├── app.py          # Streamlit UI
├── analyzer.py     # Claude API calls, scoring logic
├── test_data.py    # Sample transcripts: nervous, confident, ambiguous
└── requirement.txt
```

## Limitations

- The model sometimes conflates signal types (e.g. classifying clarification questions as deflection).
- Analysis is context-aware but not infallible — unusual contexts may produce miscalibrated scores.
- Test transcripts in `test_data.py` are made-up by me and may not reflect the full range of real interview speech patterns.

## Tech Stack

Python · Streamlit · Anthropic Claude API
