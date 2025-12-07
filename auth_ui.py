import streamlit as st
import bcrypt
from db import create_user, get_user_by_email

#  Password hashing
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# Sign-up UI
def signup_ui():
    st.subheader("Sign up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    password2 = st.text_input("Repeat Password", type="password", key="signup_password2")

    if st.button("Create account"):
        if not email or not password or not password2:
            st.error("Please fill in all fields.")
            return

        if password != password2:
            st.error("Passwords do not match.")
            return

        password_hash = hash_password(password)
        success = create_user(email, password_hash)

        if success:
            st.success("Account created! Now you can log in.")
        else:
            st.error("This email is already registered.")

# Login UI
def login_ui():
    st.subheader("Login")

    if "login_message" in st.session_state:
        st.success(st.session_state["login_message"])
        st.success(st.session_state["summarizer_message"])

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not email or not password:
            st.error("Please fill in all fields.")
            return

        user = get_user_by_email(email)

        if user is None:
            st.error("User not found.")
            return

        stored_hash = user[2]

        if check_password(password, stored_hash):
            st.session_state["user"] = email
            st.session_state["login_message"] = f"Logged in. Welcome, {email}!"
            st.session_state["summarizer_message"] = f"Now you can use the text summarizer."
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("---")
    st.subheader("Or log in with Google")

    if not st.user.is_logged_in:
        if st.button("Log in with Google"):
            st.login()   # uses config from secrets.toml
    else:
        st.success(f"Logged in with Google as {st.user.name}")
        st.markdown(f"### 👋 Welcome, **{st.user.name}**!")
        st.caption(f"Email: {st.user.email}")
        st.caption(f"Now you can use the text summarizer.")