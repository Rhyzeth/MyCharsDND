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
        # Get JSON data from the POST request
        data = request.get_json()

        # If JSON data is not received, log an error and return response
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        # Extract table_name from the received JSON data
        table_name = data.get('table_name')

        if not table_name:
            return jsonify({"error": "Table name is required"}), 400

        # Log the received table_name for debugging purposes
        print(f"Received table_name: {table_name}")

        # Return a success response with the received table name
        return jsonify({"info": f"Received table name: {table_name}"}), 200

    except Exception as e:
        # If any error occurs, log the error and return a 500 response
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)