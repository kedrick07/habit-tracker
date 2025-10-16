import streamlit as st
from utils.database import create_habit, get_user_habits, update_habit, delete_habit
from datetime import datetime

def show():
    if "user_id" not in st.session_state:
        st.error("Please login first")
        return
    
    st.title("My Habits")

    #Tabs for different actions
    tab1, tab2 = st.tabs(["View Habits", "Add New Habit"])

    with tab1:
        habits = get_user_habits(st.session_state["user_id"])

        if not habits:
            st.info("No habits yet. Create your first babit in the 'Add New Habit' tab!")
        else:
            for habit in habits:
                with st.expander(f"{habit['name']} ({habit['category']})"):
                    st.write(f"**Description:** {habit['description']}")
                    st.write(f"**Started:** {habit['start_date']}")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Edit", key=f"edit_{habit['_id']}"):
                            st.session_state[f"editing_{habit['_id']}"] = True
                    
                    with col2:
                        if st.button("Delete", key=f"del_{habit['_id']}"):
                            if delete_habit(str(habit['_id']), st.session_state["user_id"]):
                                st.success("Habit deleted!")
                                st.rerun()

                    #edit form
                    if st.session_state.get(f"editing_{habit['_id']}", False):
                        with st.form(key=f"edit_form_{habit['_id']}"):
                            new_name = st.text_input("Name", value=habit['name'])
                            new_category = st.selectbox(
                                "Category",
                                ["Health", "Productivity", "Finance", "Learning", "Fitness", "Mindfulness", "Other"].index(habit['category'])
                            )
                            new_desc = st.text_area("Description", value=habit['description'])

                            if st.form_submit_button("Update"):
                                updates = {
                                    "name": new_name,
                                    "category": new_category,
                                    "description": new_desc
                                }
                                if update_habit(str(habit['_id']), st.session_state["user_id"], updates):
                                    st.success("Habit updated!")
                                    st.session_state[f"editing_{habit['_id']}"] = False
                                    st.rerun()
    with tab2:
        with st.form("new_habit_form"):
            name = st.text_input("Habit Name *", placeholder="e.g., Morning Exercise")
            category = st.selectbox("Category *",
                ["Health", "Productivity", "Finance", "Learning", "Fitness", "Mindfulness", "Other"])
            description = st.text_area("Description", placeholder="Optional details about this habit")
            start_date = st.date_input("Start Date", value=datetime.now())

            if st.form_submit_button("Create Habit"):
                if not name:
                    st.error("Habitr name is required")
                else:
                    habit_id = create_habit(
                        st.session_state["user_id"],
                        name,
                        category,
                        description,
                        start_date
                    )
                    st.success(f"Habit '{name}' created successfully!")
                    st.rerun()