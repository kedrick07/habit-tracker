import streamlit as st
from utils.database import get_user_habits, get_completions_collection
from bson import ObjectId
from datetime import datetime, date, time, timedelta


def is_completed_today(habit_id: str, check_date: date):
    """Check if habit was completed on specific date"""
    completions = get_completions_collection()
    
    # ✅ Convert date to datetime for MongoDB query
    if isinstance(check_date, date) and not isinstance(check_date, datetime):
        check_date = datetime.combine(check_date, time.min)
    
    record = completions.find_one({
        "habit_id": ObjectId(habit_id),
        "completion_date": check_date,
        "completed": True
    })
    return record is not None


def calculate_current_streak(habit_id: str):
    """Calculate current consecutive streak"""
    completions = get_completions_collection()
    today = date.today()
    streak = 0
    
    check_date = today
    while True:
        # ✅ Convert to datetime before querying MongoDB
        check_date_dt = datetime.combine(check_date, time.min)
        
        record = completions.find_one({
            "habit_id": ObjectId(habit_id),
            "completion_date": check_date_dt,
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
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"**{habit['name']}**")
                st.caption(f"{habit['category']}")
            
            with col2:
                if streak > 0:
                    st.write(f"🔥 {streak} day{'s' if streak != 1 else ''}")
                else:
                    st.write("—")
            
            st.divider()
