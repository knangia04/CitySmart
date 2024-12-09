import sqlite3
from flask import Blueprint, render_template, request

pollution_bp = Blueprint('pollution', __name__)

def get_db_connection():
  """
  Establish a connection to the SQLite database.
  Returns a connection object.
  """
  connection = sqlite3.connect('instance/database.db') 
  connection.row_factory = sqlite3.Row 
  return connection

@pollution_bp.route('/pollution-data')
def pollution_data():
  conn = get_db_connection()

  locations_query = 'SELECT DISTINCT location FROM PollutionData ORDER BY location'
  locations = [row['location'] for row in conn.execute(locations_query).fetchall()]

  selected_location = request.args.get('location', 'all')

  if selected_location and selected_location != 'all':
      query = 'SELECT * FROM PollutionData WHERE location = ? ORDER BY timestamp'
      pollution_records = conn.execute(query, (selected_location,)).fetchall()
  else:
      query = 'SELECT * FROM PollutionData ORDER BY timestamp'
      pollution_records = conn.execute(query).fetchall()

  conn.close()

  return render_template('pollution-data.html',
                         pollution_records=pollution_records,
                         locations=locations,
                         selected_location=selected_location)

