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
            st.success("Logged in")
            st.rerun()
        else:
            st.error("Incorrect password")

