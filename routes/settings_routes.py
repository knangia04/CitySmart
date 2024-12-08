from flask import Blueprint, render_template, redirect, url_for, flash, request, session
import sqlite3

settings_bp = Blueprint('settings', __name__)

def get_notification_preferences(user_id):
    """Fetch notification preferences for a user."""
    with sqlite3.connect('instance/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT weather_enabled, pollution_enabled, traffic_enabled
            FROM notification_preferences
            WHERE user_id = ?;
        """, (user_id,))
        return cursor.fetchone()

def update_notification_preferences(user_id, weather, pollution, traffic):
    """Update notification preferences for a user."""
    with sqlite3.connect('instance/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE notification_preferences
            SET weather_enabled = ?, pollution_enabled = ?, traffic_enabled = ?
            WHERE user_id = ?;
        """, (weather, pollution, traffic, user_id))
        conn.commit()

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    username = session.get('username')
    if not username:
        flash('Please log in first.', 'danger')
        return redirect(url_for('home'))

    try:
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('home'))

        user_id = user[0]

        # Handle POST request to update preferences
        if request.method == 'POST':
            weather = 1 if 'weather' in request.form else 0
            pollution = 1 if 'pollution' in request.form else 0
            traffic = 1 if 'traffic' in request.form else 0

            update_notification_preferences(user_id, weather, pollution, traffic)
            flash('Preferences updated successfully!', 'success')
            return redirect(url_for('settings.settings'))

        # Fetch notification preferences
        preferences = get_notification_preferences(user_id)
        return render_template('settings.html', preferences=preferences)

    except sqlite3.Error as e:
        flash(f"Error fetching settings: {str(e)}", "danger")
        return redirect(url_for('home'))
    finally:
        conn.close()

@settings_bp.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    if not username:
        flash('Please log in first.', 'danger')
        return redirect(url_for('home'))

    try:
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()

        # Find user ID
        cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('home'))

        user_id = user[0]

        # Delete associated preferences and user
        cursor.execute("DELETE FROM notification_preferences WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
        conn.commit()

        session.clear()
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('home'))

    except sqlite3.Error as e:
        flash(f"Error deleting account: {str(e)}", "danger")
        return redirect(url_for('settings.settings'))
    finally:
        conn.close()
