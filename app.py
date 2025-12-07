from llm_utils import summarize_text
import streamlit as st
from db import create_tables
from auth_ui import login_ui, signup_ui


# Create database tables when app starts
create_tables()

def is_authenticated():
    # Email/password OR Google login
    return (
        st.session_state.get("user") is not None
        or st.user.is_logged_in
    )

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Sign up", "Text summarizer"])

    # Logout button (works for both methods)
    if is_authenticated():
        if st.sidebar.button("Logout"):
            st.session_state["user"] = None  # clear local user
            try:
                st.logout()  # ends Google/OIDC session if active
            except Exception:
                # st.logout only exists in new Streamlit;
                # ignore errors if any
                pass
            st.success("Logged out")

    if page == "Login":
        login_ui()

    elif page == "Sign up":
        signup_ui()

    elif page == "Text summarizer":
        if not is_authenticated():
            st.warning("Please log in (email/password or Google) to use the summarizer.")
            return

        st.header("Text summarizer")
        user_text = st.text_area("Enter text to summarize")
        if st.button("Summarize"):
            if user_text.strip():
                summary = summarize_text(user_text)
                st.subheader("Summary")
                st.write(summary)
            else:
                st.error("Please enter some text first.")

if __name__ == "__main__":
    main()
