from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from config import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import os


# Load environment variables
load_dotenv()
db = SQLAlchemy()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = "db/dnd_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "db/dnd_database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

# Route to render the index.html page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def table_details():
    try:
        # Debugging: Log headers and raw data to check the incoming request
        print("Headers:", request.headers)
        print("Raw Data:", request.data)

        # Get JSON data from the POST request
        data = request.get_json()

        # Debugging: Check if the data was successfully parsed
        if data is None:
            print("No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400

        # Extract table_name from the JSON data
        table_name = data.get('table_name')

        # Debugging: Log the received table name
        if not table_name:
            print("Table name not provided")
            return jsonify({"error": "Table name is required"}), 400

        print(f"Received table_name: {table_name}")

        # Simulate returning info for now (replace with real logic later)
        return jsonify({"info": f"Received table name: {table_name}"}), 200

    except Exception as e:
        # Log the exception and return an error response
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "Internal server error occurred"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)