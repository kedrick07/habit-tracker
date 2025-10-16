import streamlit as st
from utils.database import get_user_habits, get_completions_collection
from bson import ObjectId
from datetime import datetime, date

def is_completed_today(habit_id: str, check_date: date):
    """Check if habit was completed on specific date"""
    completions = get_completions_collection()
    record = completions.find_one({
        "habit_id": ObjectId(habit_id),
        "completion_date": check_date,
        "completed": True
    })
    return record is not None

def mark_completion(habit_id: str, user_id: str, completion_date: date, completed: bool, note: str = ""):
    """Mark habit as complete or incomplete for a specific date"""
    completions = get_completions_collection()
    
    # Check if completion already exists
    existing = completions.find_one({
        "habit_id": ObjectId(habit_id),
        "completion_date": completion_date
    })
    
    if existing:
        completions.update_one(
            {"_id": existing["_id"]},
            {"$set": {"completed": completed, "note": note, "logged_at": datetime.now()}}
        )
    else:
        completions.insert_one({
            "habit_id": ObjectId(habit_id),
            "user_id": ObjectId(user_id),
            "completion_date": completion_date,
            "completed": completed,
            "note": note,
            "logged_at": datetime.now()
        })

def is_completed_today(habit_id: str, check_date: date):
    """Check if habit was completed on specific date"""
    completions = get_completions_collection()
    record = completions.find_one({
        "habit_id": ObjectId(habit_id),
        "completion_date": check_date,
        "completed": True
    })
    return record is not None

def show():
    if "user_id" not in st.session_state:
        st.error("Please login first")
        return
    
    st.title("📅 Today's Check-In")
    today = date.today()
    st.subheader(today.strftime("%A, %B %d, %Y"))
    
    habits = get_user_habits(st.session_state["user_id"])
    
    if not habits:
        st.info("You don't have any habits yet. Create one in the 'My Habits' page!")
        return
    
    completed_count = 0
    
    for habit in habits:
        habit_id = str(habit['_id'])
        is_done = is_completed_today(habit_id, today)
        
        if is_done:
            completed_count += 1
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{habit['name']}** ({habit['category']})")
        
        with col2:
            checked = st.checkbox("✓ Done", value=is_done, key=f"check_{habit_id}")
        
        if checked != is_done:
            mark_completion(habit_id, st.session_state["user_id"], today, checked)
            st.rerun()
    
    # Progress indicator
    total = len(habits)
    progress = completed_count / total if total > 0 else 0
    st.progress(progress)
    st.write(f"**Progress:** {completed_count} out of {total} habits completed today ({int(progress * 100)}%)")
