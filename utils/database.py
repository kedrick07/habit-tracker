from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime, date
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection string from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

# Check if environment variables are loaded
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in environment variables. Check your .env file!")
if not DB_NAME:
    raise ValueError("DB_NAME not found in environment variables. Check your .env file!")

def get_database():
    """
    Connect to MongoDB and return the database object
    """
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        
        # Test the connection
        client.admin.command('ping')
        
        return db
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        return None

def get_users_collection():
    """
    Returns the users collection
    """
    db = get_database()
    return db['users']

def get_habits_collection():
    """
    Returns the habits collection
    """
    db = get_database()
    return db['habits']

def get_completions_collection():
    """
    Returns the completions collection
    """
    db = get_database()
    return db['completions']

#function to create new habit
def create_habit(user_id: str, name: str, category: str, description: str = "", start_date=None):
    """Create a new habit for the user"""
    habits_collection = get_habits_collection()
    
    # ✅ FIX: Convert date to datetime for MongoDB
    if start_date:
        # If start_date is a datetime.date object, convert to datetime
        if isinstance(start_date, date) and not isinstance(start_date, datetime):
            start_date = datetime.combine(start_date, datetime.min.time())
    else:
        # Use current datetime
        start_date = datetime.now()
    
    habit_doc = {
        "user_id": ObjectId(user_id),
        "name": name,
        "category": category,
        "description": description,
        "start_date": start_date,  # ✅ Now it's datetime, not date
        "created_at": datetime.now()
    }
    
    result = habits_collection.insert_one(habit_doc)
    return str(result.inserted_id)


#function to get user habits
def get_user_habits(user_id: str):
    habits_collection = get_habits_collection()
    habits = habits_collection.find({"user_id": ObjectId(user_id)})
    return list(habits)

#function to update habits
def update_habit(habit_id: str, user_id: str, updates: dict):
    habits_collection = get_habits_collection()
    result = habits_collection.update_one(
        {"_id": ObjectId(habit_id), "user_id": ObjectId(user_id)},
        {"$set": updates}
    )
    return result.modified_count > 0

#function to delete habit and all its components
def delete_habit(habit_id: str, user_id: str):
    habits_collection = get_habits_collection()
    completions_collection = get_completions_collection()

    #delete completions first
    completions_collection.delete_many({"habit_id": ObjectId(habit_id)})

    #delete habit
    result = habits_collection.delete_one(
        {"_id": ObjectId(habit_id), "user_id": ObjectId(user_id)}
    )
    return result.deleted_count > 0