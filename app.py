import streamlit as st
from analyzer import analyzer_transcript, overall_score

st.title("Conversation Nervousness Analyzer")

transcript = st.text_area("Input interview transcript to analyze", height = 400)

if st.button("Analyze"):
    if transcript == "":
        st.warning("Please paste a transcript first.")
    else:
        result = analyzer_transcript(transcript)
        st.caption("Context detected: " + result["context"])
        score, verdict = overall_score(result)
        st.header("Nervousness chance: " + str(int(score * 100)) + "%")
        st.header("Proof: ")
        st.text('Filler words: '  + ", ".join(result["filler"]["words"]))
        st.text('Deflection: ' + ", ".join(result["deflection"]["words"]))
        st.text('Repeated words: ' + ", ".join(result["repeated_words"]["words"]))