from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, User, NotificationPreferences

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        flash('Please log in to access the settings page.', 'danger')
        return redirect(url_for('home'))

    # Fetch user from session
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    # Create notification preferences if not present
    if not user.notification_preferences:
        preferences = NotificationPreferences(user_id=user.id)
        db.session.add(preferences)
        db.session.commit()

    if request.method == 'POST':
        preferences = user.notification_preferences
        preferences.weather_enabled = 'weather' in request.form
        preferences.pollution_enabled = 'pollution' in request.form
        preferences.traffic_enabled = 'traffic' in request.form
        db.session.commit()
        flash('Preferences updated successfully!', 'success')
        return redirect(url_for('settings.settings'))

    return render_template('settings.html', user=user)

@settings_bp.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' not in session:
        flash('Please log in to delete your account.', 'danger')
        return redirect(url_for('home'))

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    db.session.delete(user)
    db.session.commit()
    session.pop('username', None)  # Clear session
    flash('Your account has been deleted successfully.', 'success')
    return redirect(url_for('home'))
