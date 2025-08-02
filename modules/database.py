# modules/database.py

import pymongo
import streamlit as st
import streamlit_authenticator as stauth
import certifi # Required for MongoDB Atlas connection
import os # To access environment variables

# --- MongoDB Connection ---

def connect_db():
    """
    Connects to the MongoDB database using an environment variable
    from a .env file.
    """
    # Get the connection string directly from environment variables
    connection_string = os.getenv("MONGO_URI")

    if not connection_string:
        # If the connection string is not found, show an error
        st.error("MongoDB connection string not found. Please set the MONGO_URI in your .env file.")
        return None

    try:
        # Establish the connection to the MongoDB cluster
        client = pymongo.MongoClient(connection_string, tlsCAFile=certifi.where())
        # You can name your database anything you like
        db = client.user_database 
        return db
    except pymongo.errors.ConnectionFailure as e:
        st.error(f"Could not connect to MongoDB: {e}")
        return None
    except Exception as e:
        # This will catch other errors like the DNS error
        st.error(f"An error occurred during database connection: {e}")
        return None

# --- User Management Functions ---

def fetch_users():
    """
    Fetches all users from the database and formats them for the
    streamlit-authenticator library.
    """
    db = connect_db()
    if db is not None:
        users_collection = db.users.find()
        
        credentials = {'usernames': {}}
        for user in users_collection:
            # The key for each user in the dictionary must be their username
            credentials['usernames'][user['username']] = {
                'name': user['name'],
                'email': user['email'],
                'password': user['password'] # This is the hashed password from the DB
            }
        return credentials
    # Return an empty structure if the database connection fails
    return {'usernames': {}}

def register_new_user(username, name, email, password):
    """
    Adds a new user to the database. Hashes the password before storing.
    Returns True on success, False on failure (e.g., username exists).
    """
    db = connect_db()
    if db is not None:
        users_collection = db.users
        
        # Check if the username already exists to prevent duplicates
        if users_collection.find_one({'username': username}):
            st.error("Username already exists. Please choose a different one.")
            return False

        # Hash the password before storing it in the database
        hashed_password = stauth.Hasher([password]).generate()[0]
        
        # Insert the new user document into the collection
        users_collection.insert_one({
            'username': username,
            'name': name,
            'email': email,
            'password': hashed_password
        })
        return True
    return False

