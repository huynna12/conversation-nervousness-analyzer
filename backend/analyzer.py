import anthropic, json
import streamlit as st
import os

api_key = st.secrets.get("ANTHROPIC_API_KEY") if hasattr(st, "secrets") else os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)
msg_content = """
You are a conversation analyst.

Step 1 — Identify Context
First, determine the context of the conversation based on the transcript. 

Step 2 — Analyze Signals

1. Filler words
Count only these: like, you know, ah, oh, uh, um, hmm, basically, in fact, sort of, kind of, well.
Do NOT count: really, just, very, or anything outside the list.
Mid-sentence fillers weigh much more than sentence-start fillers.

2. Deflection
Count only cases where the speaker intentionally avoids the question and does not return to answer it.
Do NOT count:
- Clarification questions (e.g. "From like a friend?")
- Scope-checking responses

3. Repeated words
Count only content words (nouns, verbs, adjectives, adverbs) that repeat enough to disrupt flow.
Do NOT count:
- Topic-related repetition

Step 3 — Scoring
For each signal, give a score from 0 to 1:
- 0 = not nervous (normal frequency for this context)
- 1 = clearly nervous (disruptive/excessive even for this context)

IMPORTANT:
- Scores MUST be relative to the identified context
- Do NOT treat all transcripts equally

Return JSON only (no markdown):
{
  "context": "job interview",
  "filler": {"score": 0.5, "count": 8, "words": ["um", "like"]},
  "deflection": {"score": 0.1, "count": 0, "words": []},
  "repeated_words": {"score": 0.3, "count": 3, "words": ["connect"]}
}
"""

def analyzer_transcript(transcript: str) -> dict:
    res = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens =1024,
    system=msg_content,
    temperature=0,
    messages=[{
        "role":"user",
        "content": transcript
    }])
    text = res.content[0].text
    text = text.replace("```json", "").replace("```", "")
    return json.loads(text.strip())

def overall_score(dict: dict) -> tuple:
    score = (dict['filler']['score']*45 + dict['deflection']['score']*10 + dict['repeated_words']['score']*45) / 100 
    verdict = "nervous" if score > 0.5 else "not nervous"
    return score, verdict


"""
For test_data_short.py 
which is hand-written and made up by me
"""
# result = analyzer_transcript(nervous_transcript)
# score, verdict = overall_score(result)
# print(f"{score:.2f} — {verdict}")
# result = analyzer_transcript(confident_transcript)
# score, verdict = overall_score(result)
# print(f"{score:.2f} — {verdict}")
# result = analyzer_transcript(ambiguous_transcript)
# score, verdict = overall_score(result)
# print(f"{score:.2f} — {verdict}")
