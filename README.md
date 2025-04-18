# LLM
📚 Book Knowledge Graph RAG Assistant
This project implements an LLM-powered Book Recommendation and Exploration Assistant using a Neo4j knowledge graph and Google's Gemini API. It supports natural language queries to explore book metadata, author relationships, and genre tags through dynamically generated Cypher queries.

🚀 Features
🔎 Ask questions like:

“Books tagged with fantasy”

“Books by J.K. Rowling”

“Books similar to Harry Potter”

🧠 Gemini LLM dynamically generates Cypher queries based on user input

📘 Interactive Streamlit UI for user input and result display

🕸️ Neo4j graph stores structured book-author-tag relationships

📁 Project Structure
├── app.py                  # Streamlit app UI
├── graph_query.py         # Gemini LLM prompt + Cypher generation logic
├── load_books.py          # Loads `bookkg_clean_10000.csv` into Neo4j
├── test.py                # Validates Gemini API and model support
├── bookkg_clean_10000.csv # Cleaned dataset for knowledge graph
├── requirements.txt       # Python package dependencies


📊 Graph Schema
(:Book {book_id, title, year})
(:Author {name})
(:Tag {name})
(:Book)-[:WRITTEN_BY]->(:Author)
(:Book)-[:HAS_TAG]->(:Tag)

🔮 Future Roadmap
Add vector search with FAISS for hybrid retrieval

Support multi-hop graph reasoning

User chat history with context-aware query improvement

Analyze user sentiment or preferences over time


