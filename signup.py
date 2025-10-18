import streamlit as st
from utils.auth import create_user, verify_password
from utils.database import get_users_collection


def show():
    st.title("📝 Create Your Account")
    
    # Back to login button
    if st.button("← Back to Login"):
        st.session_state["show_signup"] = False
        st.rerun()
    
    st.divider()
    
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
    
    if st.button("Create Account", type="primary", use_container_width=True):
        # Validation
        if not name or not email or not password:
            st.error("Please fill in all fields")
            return
        
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        
        # Create user
        user_id, error = create_user(name, email, password)
        
        if error:
            st.error(error)
        else:
            st.success(f"Account created successfully! Welcome, {name}!")
            
            # Auto-login the user
            users_collection = get_users_collection()
            user = users_collection.find_one({"email": email})
            
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["user_id"] = str(user["_id"])
            st.session_state["user_name"] = user["name"]
            st.session_state["show_signup"] = False
            st.session_state["current_page"] = "Dashboard"
            
            st.rerun()


if __name__ == "__main__":
    show()
