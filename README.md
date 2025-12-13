# Programming Project – Streamlit Login + SQLite + LLM

This project is a simple web app built with **Python** and **Streamlit**.

It includes:

- User **Sign-up, Login and Logout**
- User credentials stored in a local **SQLite** database
- An **AI Text Summarizer** using an LLM
- A **Programming Tutor Chatbot** (chat-style interface)
- Basic session management with `st.session_state`

It was created as a group project for the Programming course.

---

## 1. Project Structure

Main files in this repository:

```text
.
├─ app.py           # Streamlit entry point (run this file)
├─ auth_ui.py       # UI components for login and sign-up
├─ db.py            # SQLite database functions (create tables, add users, etc.)
├─ llm_utils.py     # Functions that call the LLM (summarizer + chatbot)
├─ my_secrets.py    # Stores the API key (placeholder only in the repo)
├─ users.db         # SQLite database file with the users table
└─ requirements.txt # Python dependencies
