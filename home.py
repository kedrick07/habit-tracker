import streamlit as st
import signup
import login
import dashboard
import manage_habits
import checkin

def main():
    st.sidebar.title("Navigation")
    
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        # Logged in menu
        page = st.sidebar.radio("Go to", [
            "Dashboard",
            "Today's Check-In",
            "My Habits",
            "Profile"
        ])
        
        if st.sidebar.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if page == "Dashboard":
            dashboard.show()
        elif page == "Today's Check-In":
            checkin.show()
        elif page == "My Habits":
            manage_habits.show()
        elif page == "Profile":
            st.write("Profile page coming soon!")
    else:
        # Not logged in menu
        page = st.sidebar.radio("Go to", ["Home", "Sign Up", "Login"])
        
        if page == "Home":
            st.title("Welcome to Habit Tracker!")
            st.write("Build better habits, one day at a time.")
        elif page == "Sign Up":
            signup.show()
        elif page == "Login":
            login.show()

if __name__ == "__main__":
    main()
