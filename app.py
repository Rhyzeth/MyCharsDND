from flask import Flask, request, jsonify
from dotenv import load_dotenv
from config import config
from flask_sqlalchemy import SQLAlchemy
import os

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Set up SQLAlchemy with the app config
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])
db = SQLAlchemy(app)

# Define your database model
class YourTable(db.Model):
    __tablename__ = 'your_table'
    
    id = db.Column(db.Integer, primary_key=True)
    point_name = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<YourTable {self.point_name}>"

# Query database using SQLAlchemy
def query_database(point):
    result = YourTable.query.filter_by(point_name=point).first()
    if result:
        return result.info
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
    app.run(debug=True, host='0.0.0.0')  # Ensure it's accessible from outside the container
