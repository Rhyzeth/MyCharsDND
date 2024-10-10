from flask import Flask, request, jsonify
from dotenv import load_dotenv
from config import config
from flask_sqlalchemy import SQLAlchemy
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure the Flask app based on the environment
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])
db = SQLAlchemy(app)

# Define the model
class YourTable(db.Model):
    __tablename__ = 'your_table'
    
    id = db.Column(db.Integer, primary_key=True)
    point_name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<YourTable {self.point_name}>"

# Query database
def query_database(point):
    try:
        result = YourTable.query.filter_by(point_name=point).first()
        if result:
            return result.info
        else:
            return None
    except Exception as e:
        print(f"An error occurred while querying the database: {e}")
        return None

# Handle the POST request
@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    point = data.get('point')
    
    if not point:
        return jsonify({"error": "Invalid point"}), 400
    
    # Query the database
    info = query_database(point)
    if info:
        return jsonify({"info": info})
    else:
        return jsonify({"error": "No data found for this point."}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates tables if they don't already exist
    app.run(debug=True, host='0.0.0.0')
