from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, User, NotificationPreferences

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    # Get the logged-in user from the session
    username = session.get('username')
    if not username:
        flash('Please log in first.', 'danger')
        return redirect(url_for('home'))

    # Find the user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    # Create notification preferences if not present
    if not user.notification_preferences:
        preferences = NotificationPreferences(user_id=user.id)
        db.session.add(preferences)
        db.session.commit()

    if request.method == 'POST':
        # Get the first (and only) notification preferences object for this user
        preferences = user.notification_preferences[0]
        
        # Update preferences based on form submission
        preferences.weather_enabled = 'weather' in request.form
        preferences.pollution_enabled = 'pollution' in request.form
        preferences.traffic_enabled = 'traffic' in request.form
        
        try:
            db.session.commit()
            flash('Preferences updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating preferences: {str(e)}', 'danger')
        
        return redirect(url_for('settings.settings'))

    return render_template('settings.html', user=user)

@settings_bp.route('/delete_account', methods=['POST'])
def delete_account():
    # Get the logged-in user from the session
    username = session.get('username')
    if not username:
        flash('Please log in first.', 'danger')
        return redirect(url_for('home'))

    # Find the user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    try:
        # Delete associated notification preferences first
        NotificationPreferences.query.filter_by(user_id=user.id).delete()
        
        # Then delete the user
        db.session.delete(user)
        db.session.commit()
        
        # Clear the session
        session.clear()
        
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting account: {str(e)}', 'danger')
        return redirect(url_for('settings.settings'))