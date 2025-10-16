from pymongo import MongoClient
from dotenv import load_dotenv
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