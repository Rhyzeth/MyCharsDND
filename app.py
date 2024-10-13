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

def table_details():
    try:
        # Get JSON data from the POST request
        data = request.get_json()
        table_name = data.get('table_name')

        if not table_name:
            return jsonify({"error": "Table name is required"}), 400

        # For now, return the table name (replace this with actual table querying logic)
        return jsonify({"info": f"Received table name: {table_name}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)