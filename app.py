from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from config import config
from flask_sqlalchemy import SQLAlchemy
import os
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure the Flask app based on the environment
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])
db = SQLAlchemy(app)

# Route to render the index.html page
@app.route('/')
def home():
    return render_template('index.html')

# Handle the POST request
@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    table_name = data.get('point')  # The frontend sends the table name
    
    if not table_name:
        return jsonify({"error": "Invalid table name"}), 400

    # Query the database dynamically using SQLAlchemy session
    rows = query_table(table_name)
    if rows is not None:
        return jsonify({"info": rows})
    else:
        return jsonify({"error": f"No data found for table '{table_name}'"}), 404

# Function to query any table by name and get the first 5 rows
def query_table(table_name):
    try:
        # Reflect the table from the database using SQLAlchemy metadata
        table = db.Model.metadata.tables.get(table_name)

        if table is not None:
            # Query the table using the session and limit the result to 5 rows
            query = db.session.query(table).limit(5).all()
            
            # Convert result into a list of dictionaries
            rows = [dict(row) for row in query]
            return rows
        else:
            print(f"Table '{table_name}' does not exist.")
            return None
    except Exception as e:
        print(f"An error occurred while querying the table '{table_name}': {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
