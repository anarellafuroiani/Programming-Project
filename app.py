from llm_utils import summarize_text, chat_with_tutor
import streamlit as st
from db import create_tables
from auth_ui import login_ui, signup_ui

# Create database tables when app starts
create_tables()


def show_logged_in_area():
    """Main app area shown after the user logs in."""
    st.success(f"Welcome, {st.session_state['user']}!")

    # Tabs for different AI tools
    tab1, tab2 = st.tabs(["AI Text Summarizer", "Programming Tutor Chatbot 💬"])

    # --- Summarizer tab ---
    with tab1:
        st.subheader("AI Text Summarizer")
        user_text = st.text_area("Write or paste text to summarize:")

        if st.button("Summarize"):
            if user_text.strip():
                summary = summarize_text(user_text)
                st.subheader("Summary:")
                st.write(summary)
            else:
                st.warning("Please enter some text to summarize.")

    # --- Chatbot tab ---
    with tab2:
        st.subheader("Ask the Programming Tutor")

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Show previous chat messages
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input for the next user message
        user_message = st.chat_input(
            "Ask a question about Python, SQLite or this app..."
        )

        if user_message:
            # Add the new user message to the history and show it
            st.session_state["chat_history"].append(
                {"role": "user", "content": user_message}
            )
            with st.chat_message("user"):
                st.markdown(user_message)

            # Get reply from the LLM
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    reply = chat_with_tutor(
                        user_message, st.session_state["chat_history"]
                    )
                    st.markdown(reply)

            # Save assistant reply to history
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": reply}
            )

        # Optional: button to clear the chat
        if st.button("Clear chat history"):
            st.session_state["chat_history"] = []
            st.experimental_rerun()

    # Logout button below the tabs
    if st.button("Logout"):
        st.session_state["user"] = None
        st.info("You have been logged out.")
        # Also clear chat
        st.session_state["chat_history"] = []


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
        show_logged_in_area()


if __name__ == "__main__":
    main()
