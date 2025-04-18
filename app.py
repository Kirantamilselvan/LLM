# ✅ File: app.py
import streamlit as st
from agent import run_agent

st.set_page_config(page_title="📘 Book Knowledge Assistant", page_icon="📚")
st.title("📚 Book Knowledge Assistant with Agentic AI")
st.markdown("Ask anything about books, genres, ratings, authors, or recommendations!")

query = st.text_input("🔍 Ask your question")

if query:
    with st.spinner("Thinking..."):
        response = run_agent(query)
        st.success("🧠 Answer:")
        st.markdown(response)
