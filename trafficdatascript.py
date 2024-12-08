
import sqlite3
import csv


# Path to your database
DATABASE = 'instance/database.db'
CSV_FILE = 'data/bay_area_traffic_data.csv' 


def initialize_db():
   """Set up database and insert traffic data from the CSV file."""
   # Connect to database
   conn = sqlite3.connect(DATABASE)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()


   # Create the table if it doesn't already exist
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS TrafficData (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       Timestamp TEXT NOT NULL,
       Route TEXT NOT NULL,
       TypeOfCollision TEXT NOT NULL,
       Description TEXT NOT NULL
   )
   ''')


   # Open CSV file and insert data into the database
   with open(CSV_FILE, 'r') as file:
       reader = csv.DictReader(file)  # Parse CSV as a dictionary
       for row in reader:
           # Extract the data
           timestamp = row.get('Timestamp')
           route = row.get('Route')
           collision_type = row.get('TypeOfCollision')
           description = row.get('Description')


           # Insert data into the database
           cursor.execute('''
           INSERT INTO TrafficData (Timestamp, Route, TypeOfCollision, Description)
           VALUES (?, ?, ?, ?)
           ''', (timestamp, route, collision_type, description))


   # Commit changes and close connection
   conn.commit()
   conn.close()
   print("All traffic data has been added to the database successfully!")


# Run the script to set up the database
initialize_db()
