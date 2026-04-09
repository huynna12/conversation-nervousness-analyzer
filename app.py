import streamlit as st
from analyzer import analyzer_transcript, overall_score

st.title("Conversation Nervousness Analyzer")

transcript = st.text_area("Input interview transcript to analyze")

if transcript != "":
    score, verdict = overall_score(analyzer_transcript(transcript))

    st.header("Result: " + verdict)
    st.header("Proof:")
    st.text()