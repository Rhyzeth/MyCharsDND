from flask import Flask, request, jsonify
from dotenv import load_dotenv
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
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

# Query database with pagination and optional search
def query_database(point, page, per_page, search_query=None):
    try:
        query = YourTable.query.filter_by(point_name=point)
        
        if search_query:
            # Apply search filter based on 'info' field
            query = query.filter(YourTable.info.ilike(f"%{search_query}%"))
        
        paginated = query.paginate(page, per_page, False)
        results = [result.info for result in paginated.items]
        total_pages = paginated.pages
        
        return results, total_pages
    except Exception as e:
        print(f"An error occurred while querying the database: {e}")
        return [], 0

# Handle the POST request for getting paginated data
@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    point = data.get('point')
    page = data.get('page', 1)
    search_query = data.get('search', '')
    per_page = 10  # Number of items per page
    
    if not point:
        return jsonify({"error": "Invalid point"}), 400
    
    # Query the database
    results, total_pages = query_database(point, page, per_page, search_query)
    
    if results:
        return jsonify({"results": results, "total_pages": total_pages})
    else:
        return jsonify({"error": "No data found for this point."}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates tables if they don't already exist
    app.run(debug=True, host='0.0.0.0')
