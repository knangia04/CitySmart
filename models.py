import sqlite3
import bcrypt  # Use bcrypt directly for password hashing
import os
from flask import current_app

# Initialize SQLite database
db = 'instance/database.db'

# Utility functions to initialize and interact with the database
def init_db():
    """Initialize the database and create tables."""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        # Create Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            location TEXT NOT NULL
        );
        """)

        # Create NotificationPreferences table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS NotificationPreferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weather_enabled INTEGER DEFAULT 0,
            pollution_enabled INTEGER DEFAULT 0,
            traffic_enabled INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE
        );
        """)

        conn.commit()

def add_user(username, email, password, location):
    """Add a new user to the Users table."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Users (username, email, password, location)
        VALUES (?, ?, ?, ?);
        """, (username, email, hashed_password, location))
        conn.commit()

def get_user_by_username(username):
    """Retrieve a user by username."""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, username, email, password, location 
        FROM Users WHERE username = ?;
        """, (username,))
        return cursor.fetchone()

def check_password(username, password):
    """Check if the given password matches the stored hash for a user."""
    user = get_user_by_username(username)
    if not user:
        return False
    stored_password = user[3]
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

def add_notification_preferences(user_id, weather, pollution, traffic):
    """Add notification preferences for a user."""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO NotificationPreferences (user_id, weather_enabled, pollution_enabled, traffic_enabled)
        VALUES (?, ?, ?, ?);
        """, (user_id, int(weather), int(pollution), int(traffic)))
        conn.commit()

def get_notification_preferences(user_id):
    """Retrieve notification preferences for a user."""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT weather_enabled, pollution_enabled, traffic_enabled 
        FROM NotificationPreferences WHERE user_id = ?;
        """, (user_id,))
        return cursor.fetchone()
