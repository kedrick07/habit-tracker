import streamlit as st
import signup
import dashboard
import manage_habits
import checkin
from utils.auth import verify_password
from utils.database import get_users_collection


def show_login():
    """Display login form on home page"""
    st.title("🎯 Habit Tracker")
    st.subheader("Welcome Back!")
    
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login", type="primary", use_container_width=True):
            if not email or not password:
                st.error("Please fill in all fields")
                return
            
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
            st.session_state["current_page"] = "Dashboard"
            st.success(f"Welcome back, {user['name']}!")
            st.rerun()
    
    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state["show_signup"] = True
            st.rerun()


def main():
    # Check if user is logged in
    if st.session_state.get("logged_in", False):
        # Show sidebar navigation for logged in users
        st.sidebar.title("Navigation")
        
        page = st.sidebar.radio("Go to", [
            "Dashboard",
            "Today's Check-In",
            "My Habits",
            "Profile"
        ], key="nav_radio")
        
        if st.sidebar.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Route to appropriate page
        if page == "Dashboard":
            dashboard.show()
        elif page == "Today's Check-In":
            checkin.show()
        elif page == "My Habits":
            manage_habits.show()
        elif page == "Profile":
            st.write("Profile page coming soon!")
    
    elif st.session_state.get("show_signup", False):
        # Show signup page
        signup.show()
    
    else:
        # Show login page (home)
        show_login()


if __name__ == "__main__":
    main()
