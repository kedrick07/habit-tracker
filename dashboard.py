import streamlit as st
from utils.database import get_user_habits, get_completions_collection
from bson import ObjectId
from datetime import date, timedelta

def calculate_current_streak(habit_id: str):
    """Calculate current consecutive streak"""
    completions = get_completions_collection()
    today = date.today()
    streak = 0
    
    # Check if completed today
    check_date = today
    while True:
        record = completions.find_one({
            "habit_id": ObjectId(habit_id),
            "completion_date": check_date,
            "completed": True
        })
        
        if record:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    return streak

def show():
    if "user_id" not in st.session_state:
        st.warning("Please login to view dashboard")
        return
    
    st.title("🎯 Habit Tracker Dashboard")
    st.write(f"Welcome back, {st.session_state.get('user_name', 'User')}!")
    
    habits = get_user_habits(st.session_state["user_id"])
    
    if not habits:
        st.info("Start your journey by creating your first habit!")
        return
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Habits", len(habits))
    
    with col2:
        today = date.today()
        completed_today = sum(1 for h in habits if is_completed_today(str(h['_id']), today))
        st.metric("Completed Today", f"{completed_today}/{len(habits)}")
    
    with col3:
        active_streaks = sum(1 for h in habits if calculate_current_streak(str(h['_id'])) > 0)
        st.metric("Active Streaks", active_streaks)
    
    # Habit list with streaks
    st.subheader("Your Habits")
    
    for habit in habits:
        streak = calculate_current_streak(str(habit['_id']))
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{habit['name']}**")
                st.caption(habit['category'])
            
            with col2:
                if streak > 0:
                    st.write(f"🔥 {streak} day{'s' if streak != 1 else ''}")
                else:
                    st.write("—")
            
            with col3:
                if st.button("View", key=f"view_{habit['_id']}"):
                    st.session_state['selected_habit'] = str(habit['_id'])
                    st.switch_page("pages/habit_details.py")
            
            st.divider()
