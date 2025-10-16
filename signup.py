import streamlit as st
from utils.auth import create_user

def show():
    st.title("Sign Up")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
            return

        user_id, error = create_user(name, email, password)
        if error:
            st.error(error)
        else:
            st.success(f"Account created! Your user ID is {user_id}")

if __name__ == "__main__":
    show()
