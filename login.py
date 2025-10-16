import streamlit as st
from utils.auth import verify_password, create_user 
from utils.database import get_users_collection

def show():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users_collection = get_users_collection()
        user = users_collection.find_one({"email": email})

        if not user:
            st.error("Email not registered.")
            return

        if not verify_password(password, user["password"]):
            st.error("Invalid password.")
            return

        # Store logged in state
        st.session_state["logged_in"] = True
        st.session_state["user_email"] = email
        st.session_state["user_id"] = str(user["_id"])
        st.session_state["user_name"] = user["name"]
        st.success(f"Welcome back, {user['name']}!")
