from flask import Flask, render_template, request, jsonify
from config import config
import sqlite3
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = "db/dnd_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "db/dnd_database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Route to render the index.html page
@app.route('/')
def home():
    return render_template('index.html')

def get_db_connection():
    conn = sqlite3.connect('dnd_database.db')
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)