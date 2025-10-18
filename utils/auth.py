import bcrypt
import re
from utils.database import get_users_collection
from datetime import datetime, timezone


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_str = hashed_bytes.decode('utf-8')
    return hashed_str


def verify_password(password: str, hashed: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_user(name: str, email: str, password: str):
    # Validate email format with regex
    email_pattern = r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return None, "Invalid email format"
    
    users_collection = get_users_collection()
    
    # Check if email already exists
    if users_collection.find_one({"email": email}):
        return None, "Email already registered"
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Create user document
    user_doc = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "createdAt": datetime.now(timezone.utc)
    }
    
    # Insert into MongoDB users collection
    result = users_collection.insert_one(user_doc)
    
    # Return the ObjectId of the new user as a string
    return str(result.inserted_id), None
