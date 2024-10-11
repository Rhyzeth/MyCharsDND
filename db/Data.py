import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import time
from fractions import Fraction

# Create a new Flask app specifically for populating the database
app = Flask(__name__)

# Get the absolute path to the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the SQLite database (absolute path)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "dnd_database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Monster model
class Monster(db.Model):
    __tablename__ = 'monsters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    challenge_rating = db.Column(db.Float, nullable=False)
    hit_points = db.Column(db.Integer, nullable=False)
    armor_class = db.Column(db.Integer, nullable=False)
    abilities = db.Column(db.Text)
    actions = db.Column(db.Text)

# Define the 
class Spell(db.Model):
    __tablename__ = 'spells'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    school = db.Column(db.String(50), nullable=False)
    casting_time = db.Column(db.String(50), nullable=False)
    range = db.Column(db.String(50), nullable=False)
    components = db.Column(db.String(100))
    duration = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class Background(db.Model):
    __tablename__ = 'backgrounds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Plane(db.Model):
    __tablename__ = 'planes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Feat(db.Model):
    __tablename__ = 'feats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Condition(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Race(db.Model):
    __tablename__ = 'races'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    speed = db.Column(db.Integer)
    ability_score_increases = db.Column(db.String(100))
    description = db.Column(db.Text)

class CharacterClass(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hit_die = db.Column(db.String(10))
    primary_ability = db.Column(db.String(50))
    spellcasting_ability = db.Column(db.String(50))
    description = db.Column(db.Text)

class MagicItem(db.Model):
    __tablename__ = 'magic_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    description = db.Column(db.Text)

class Weapon(db.Model):
    __tablename__ = 'weapons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    damage = db.Column(db.String(50))
    properties = db.Column(db.String(100))
    description = db.Column(db.Text)

class Armor(db.Model):
    __tablename__ = 'armor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    armor_class = db.Column(db.String(50))
    properties = db.Column(db.String(100))
    description = db.Column(db.Text)

# Function to fetch and populate data from an API endpoint
def fetch_and_populate(endpoint, model, data_mapper, start_page=1):
    current_page = start_page
    next_url = f"{endpoint}?page={current_page}"

    while next_url:
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            entries = data['results']
            next_url = data['next']
            
            for entry in entries:
                mapped_data = data_mapper(entry)
                if mapped_data:
                    db.session.add(model(**mapped_data))
            db.session.commit()
            print(f"{model.__tablename__.capitalize()} populated successfully for this page {current_page}.")

            current_page += 1
            next_url = f"{endpoint}?page={current_page}" if next_url else None
        
        elif response.status_code == 500:
            print(f"Server error on page {current_page}. Skipping this page.")
            current_page += 1
            next_url = f"{endpoint}?page={current_page}"
        else:
            print(f"Failed to fetch monsters on page {current_page}, at {endpoint}. Status code: {response.status_code}")
            return


# Data mapping functions
def map_monster_data(data):
    challenge_rating_str = data.get('challenge_rating', '0')
    try:
        if '/' in challenge_rating_str:
            challenge_rating = float(Fraction(challenge_rating_str))
        else:
            challenge_rating = float(challenge_rating_str)
    except ValueError:
        challenge_rating = 0.0

    abilities = data.get('special_abilities')
    actions = data.get('actions')

    abilities_text = '; '.join([f"{ability['name']}: {ability['desc']}" for ability in abilities]) if abilities else ''
    actions_text = '; '.join([f"{action['name']}: {action['desc']}" for action in actions]) if actions else ''

    return {
        'name': data.get('name'),
        'challenge_rating': challenge_rating,
        'hit_points': int(data.get('hit_points', 0)),
        'armor_class': int(data.get('armor_class', 0)),
        'abilities': abilities_text,
        'actions': actions_text
    }

def map_spell_data(data):
    # Extract the school name from the dictionary, default to an empty string if it's not there
    school_data = data.get('school', {})
    school_name = school_data.get('name', '') if isinstance(school_data, dict) else school_data
    
    return {
        'name': data.get('name'),
        'level': int(data.get('level_int', 0)),
        'school': school_name,
        'casting_time': data.get('casting_time', ''),
        'range': data.get('range', ''),
        'components': data.get('components', ''),
        'duration': data.get('duration', ''),
        'description': data.get('desc', '')
    }

def map_background_data(data):
    return {
        'name': data.get('name'),
        'description': data.get('desc', '')
    }

def map_plane_data(data):
    return {
        'name': data.get('name'),
        'description': data.get('desc', '')
    }

def map_feat_data(data):
    return {
        'name': data.get('name'),
        'description': data.get('desc', '')
    }

def map_condition_data(data):
    return {
        'name': data.get('name'),
        'description': data.get('desc', '')
    }

def map_race_data(data):
    speed_data = data.get('speed', {})
    speed = int(speed_data.get('walk', 0)) if isinstance(speed_data, dict) else int(speed_data)
    return {
        'name': data.get('name'),
        'speed': speed,
        'ability_score_increases': data.get('asi_desc', ''),
        'description': data.get('desc', '')
    }

def map_class_data(data):
    return {
        'name': data.get('name'),
        'hit_die': data.get('hit_dice', ''),
        'primary_ability': data.get('primary_ability', ''),
        'spellcasting_ability': data.get('spellcasting_ability', ''),
        'description': data.get('desc', '')
    }

def map_magic_item_data(data):
    return {
        'name': data.get('name'),
        'type': data.get('type', ''),
        'rarity': data.get('rarity', ''),
        'description': data.get('desc', '')
    }

def map_weapon_data(data):
    return {
        'name': data.get('name'),
        'category': data.get('weapon_category', ''),
        'damage': data.get('damage_dice', ''),
        'properties': ', '.join(data.get('properties', [])),
        'description': data.get('desc', '')
    }

def map_armor_data(data):
    return {
        'name': data.get('name'),
        'category': data.get('armor_category', ''),
        'armor_class': data.get('armor_class', ''),
        'properties': data.get('properties', ''),
        'description': data.get('desc', '')
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created before populating

        # Fetch and populate each type of data
        fetch_and_populate('https://api.open5e.com/v1/monsters/', Monster, map_monster_data)
        fetch_and_populate('https://api.open5e.com/v2/spells/', Spell, map_spell_data)
        fetch_and_populate('https://api.open5e.com/v2/backgrounds/', Background, map_background_data)
        fetch_and_populate('https://api.open5e.com/v1/planes/', Plane, map_plane_data)
        fetch_and_populate('https://api.open5e.com/v2/feats/', Feat, map_feat_data)
        fetch_and_populate('https://api.open5e.com/v2/conditions/', Condition, map_condition_data)
        fetch_and_populate('https://api.open5e.com/v2/races/', Race, map_race_data)
        fetch_and_populate('https://api.open5e.com/v1/classes/', CharacterClass, map_class_data)
        fetch_and_populate('https://api.open5e.com/v1/magicitems/', MagicItem, map_magic_item_data)
        fetch_and_populate('https://api.open5e.com/v2/weapons/', Weapon, map_weapon_data)
        fetch_and_populate('https://api.open5e.com/v2/armor/', Armor, map_armor_data)
