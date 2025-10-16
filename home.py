import streamlit as st
import signup
import login

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Sign Up", "Login"])

    if page == "Home":
        st.title("Welcome to Habit Tracker!")
        st.write("Select a page from the sidebar to get started.")
        if "logged_in" in st.session_state and st.session_state["logged_in"]:
            st.write(f"Currently logged in as: {st.session_state.get('user_email')}")
    elif page == "Sign Up":
        signup.show()
    elif page == "Login":
        login.show()

if __name__ == "__main__":
    main()

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_email"] = None
        st.experimental_rerun()
