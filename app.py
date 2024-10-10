from flask import Flask, request, jsonify
import sqlite3  # or use another database driver such as psycopg2 for PostgreSQL
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Connect to your SQL database
def query_database(point):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    
    # Example SQL query based on the selected point
    cursor.execute("SELECT info FROM your_table WHERE point_name = ?", (point,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    else:
        return "No data found for this point."

# Handle the POST request from the frontend
@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    point = data.get('point')
    
    if point:
        # Query the database
        info = query_database(point)
        return jsonify({"info": info})
    else:
        return jsonify({"error": "Invalid point"}), 400

if __name__ == '__main__':
    app.run(debug=True)
