from llm_utils import summarize_text
import streamlit as st
from db import create_tables
from auth_ui import login_ui, signup_ui


# Create database tables when app starts
create_tables()

def main():
    st.title("Login System with SQLite")

    # Initialize session_state user if missing
    if "user" not in st.session_state:
        st.session_state["user"] = None

    # If NOT logged in
    if st.session_state["user"] is None:
        option = st.radio("Select an option:", ["Login", "Sign up"])

        if option == "Login":
            login_ui()
        else:
            signup_ui()

    # If logged in
    else:
        st.success(f"Welcome, {st.session_state['user']}!")
        # LLM Feature
        st.subheader("AI Text Summarizer")

        user_text = st.text_area("Write or paste text to summarize:")

        if st.button("Summarize"):
            if user_text.strip():
                summary = summarize_text(user_text)
                st.subheader("Summary:")
                st.write(summary)
            else:
                st.warning("Please enter some text to summarize.")

        # Logout button
        if st.button("Logout"):
            st.session_state["user"] = None
            st.info("You have been logged out.")

if __name__ == "__main__":
    main()
