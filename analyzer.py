import anthropic, json
from test_data import transcript1, transcript2, transcript3
from test_data_short import nervous_transcript, confident_transcript, ambiguous_transcript
client = anthropic.Anthropic()

msg_content = """You are a conversation analyst. Given a transcript, analyze it for signs of nervousness across three signals.
1. Filler words
Count only these specific words and phrases: like, you know, ah, oh, uh, um, hmm, basically, in fact, sort of, kind of, well, jeez.
Do NOT count: really, just, very, or any word not in the list above.
Mid-sentence fillers weigh more on the score than fillers at the start of a sentence.

2. Deflection
Count only cases where the speaker clearly or loosely avoids the question AND never circles back to answer it.
Do NOT count:
- Clarification questions (e.g. "From like a friend?")
- Requests for more information before answering
- Brief scope-checking responses aimed at understanding the question
- Tangents where the speaker eventually returns to address the question

3. Repeated words
Count only content words (nouns, verbs, adjectives, adverbs) that recur so frequently they disrupt the flow or suggest the speaker is stuck.
Do NOT count:
- Common function words: and, but, because, so, that, it, this, I, you, we, they, she, he, is, are, was, were, have, had, do, not
- Contractions: it’s, that’s, I’ve, I’m, I don’t, can’t, won’t, didn’t
- Discourse markers: I think, I mean, I guess, you know
- Words that repeat naturally because they are the topic of the conversation (e.g. "gluten" in a conversation about gluten intolerance)

For each signal, give a score from 0 to 1.
- 0 = not nervous; signals appeared a normal/reasonable number of times
- 1 = nervous; signals appeared so frequently the speech feels awkward or disrupted
Return raw JSON only, no markdown:
{"filler":{"score": 0.8, "count": 12, "words": "word1 word2 word3"}, "deflection": {"score": 0.9, "count": 5, "words": "quoted phrase or description"}, "repeated_words": {"score": 0.6, "count": 5, "words": "word1 word2 word3"}}
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

""" 
For the test_data.py
from: https://study.sagepub.com/node/31740/student-resources/chapter-5
      section 4. Three sample interview transcripts
"""
# result = analyzer_transcript(transcript1)
# score, verdict = overall_score(result)
# print(f"{score:.2f} — {verdict}")
# result = analyzer_transcript(transcript2)
# score, verdict = overall_score(result)
# print(f"{score:.2f} — {verdict}")
# result = analyzer_transcript(transcript3)
# score, verdict = overall_score(result)
# print(f"{score:.2f} — {verdict}")