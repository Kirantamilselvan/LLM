import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import json
from agent import run_agent
import os

st.set_page_config(page_title="BookMeta", page_icon="📚", layout="wide")

# 🌑 DARK MODE CSS
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .stApp {
        background-color: #121212;
    }
    .top-bar {
        background-color: #1f1f1f !important;
        color: white;
    }
    .css-1d391kg { color: white !important; }
    .stTextInput > div > input {
        background-color: #1e1e1e;
        color: white;
    }
    .stButton > button {
        background-color: #333;
        color: white;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- File to persist users ----------
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(user_db):
    with open(USER_FILE, "w") as f:
        json.dump(user_db, f, indent=2)

# ---------- Session defaults ----------
if "user_db" not in st.session_state:
    st.session_state.user_db = load_users()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_user" not in st.session_state:
    st.session_state.show_user = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- LOGIN / REGISTER ----------
if not st.session_state.logged_in:
    st.title("🔐 Welcome to BookMeta")
    user_type = st.radio("**Are you a new or returning user?**", ["New User", "Returning User"])

    if user_type == "New User":
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            age = st.number_input("Age", min_value=15, max_value=100, step=1)
            how_heard = st.selectbox("How did you hear about us?", ["Friend", "Social Media", "Advertisement", "Search Engine", "Other"])
            genres = st.multiselect("Favorite Genre(s)", ["Fiction", "Mystery", "Romance", "Fantasy", "Non-fiction", "Thriller", "Sci-Fi", "Historical"])
            password = st.text_input("Create Password", type="password")
            register = st.form_submit_button("Register")

            if register:
                if not all([name, email, password]):
                    st.warning("Please fill all required fields.")
                elif email in st.session_state.user_db:
                    st.warning("User already exists! Try logging in.")
                else:
                    st.session_state.user_db[email] = {
                        "name": name,
                        "age": age,
                        "heard_from": how_heard,
                        "genres": genres,
                        "password": password
                    }
                    save_users(st.session_state.user_db)
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()

    if user_type == "Returning User":
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Login")

            if login:
                user_db = st.session_state.user_db
                if email in user_db and user_db[email].get("password") == password:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Oops!Seems like we don't have your account. Try registering!!")
    st.stop()

# ---------- FIXED TOP HEADER BAR ----------
st.markdown('<div class="top-bar">', unsafe_allow_html=True)
top_col1, top_col2 = st.columns([11, 1])
with top_col1:
    st.markdown("## 📚 BookMeta")
    st.markdown("_**Discover books · Ask questions · Get smarter recommendations**_")
with top_col2:
    if st.button("👤", help="View Profile"):
        st.session_state.show_user = not st.session_state.get("show_user", False)

# ---------- USER PROFILE SECTION ----------
if st.session_state.get("show_user", False) and st.session_state.get("user_email") in st.session_state.user_db:
    user = st.session_state.user_db[st.session_state.user_email]
    name = user.get("name", "")
    age = user.get("age", "Not provided")
    heard_from = user.get("heard_from", "Not specified")
    genres = ", ".join(user.get("genres", []))

    st.markdown("#### 👤 User Profile")
    st.markdown(f"**Name:** {name}")
    st.markdown(f"**Age:** {age}")
    st.markdown(f"**Email:** [{st.session_state.user_email}](mailto:{st.session_state.user_email})")
    st.markdown(f"**Heard About Us From:** {heard_from}")
    st.markdown(f"**Favorite Genres:** {genres}")

    if st.button("Sign Out", key="signout_button"):
        st.session_state.logged_in = False
        st.session_state.show_user = False
        st.session_state.user_email = ""
        st.session_state.chat_history = []
        st.rerun()

else:
    selected = st.radio(
        "Navigate", ["Home", "Bookbot", "About"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if selected == "Home":
        st.markdown("## Welcome to the Book Universe 🪐")
        st.markdown("_**Explore some of our popular books:**_")

        book_images = {
            "Fault in our Stars": "assets/fault in our stars.jpg",
            "Pride and Prejudice": "assets/pride and prejudice.jpg",
            "Little Women":"assets/little women.jpg",
            "A Court of Thorns and Roses": "assets/acotar.jpeg",
            "A Court of Mist and Fury": "assets/acomaf.jpeg",
            "A Court of Wings and Ruin": "assets/acowar.jpeg",
            "Throne of Glass": "assets/throne of glass.jpg",
            "Empire of Storms":"assets/empire of storms.jpg",
            "The Devil wears Prada": "assets/the devil wears prada.jpg",
            "A Diary of a Young Girl": "assets/a diary of a young girl.jpg",
            "Harry Potter": "assets/harry potter.jpg",
            "Crooked Kingdom":"assets/Crooked Kingdom.jpg",
            "The Hunger Games": "assets/hunger games.jpg",
            "Twilight": "assets/twilight.jpeg",
            "Time Traveller's Wife": "assets/ttw.jpeg",
            "The Hate U Give": "assets/the hate u give.jpeg",
            "Breakfast at Tiffany's": "assets/breakfast at tiffany's.jpg",
            "Fifty Shades of Grey":"assets/fifty shades of grey.jpeg",
            "A Song of Ice and Fire": "assets/asoiaf.jpeg",
            "To Kill a Mockingbird": "assets/to kill a mockingbird.jpeg",
            "The Authoritative Calvin and Hobbes": "assets/calvin and hobbes.jpeg",
            "Life of Pi":"assets/life of pi.jpg",
            "The Lovely Bones": "assets/the lovely bones.jpeg",
            "Gone Girl": "assets/gone girl.jpeg"
        }

        cols = st.columns(4)
        for i, (title, path) in enumerate(book_images.items()):
            with cols[i % 4]:
                st.image(path, width=220)

    elif selected == "Bookbot":
        st.markdown("## 💬 Your Bookbot")
        st.markdown("_**Ask anything about books, genres, authors, or recommendations!**_")

        query = st.chat_input("💬 Ask something about books...")

        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.spinner("Thinking..."):
                response = run_agent(query)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

        if st.button("🗑️ Reset Chat"):
            st.session_state.chat_history = []
            st.rerun()

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"🧑‍💬 **You:** {msg['content']}")
            else:
                st.markdown(f"🤖 **Bookbot:** {msg['content']}")

    elif selected == "About":
        st.markdown("## 🔖 About this application")
        st.markdown("""
        This is an interactive book knowledge assistant built using:
        - Agentic AI (LLMs + Neo4j Knowledge Graph)
        - Python, Streamlit, and Graph-based retrieval
        - Purpose: Help you discover books based on tags, themes, authors, and more!
        """)
