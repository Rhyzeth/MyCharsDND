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
def table_details(table_name):
    return table_name
    #return (select(table_name.c["id", "name"]))
if __name__ == '__main__':
    app.run(debug=True)