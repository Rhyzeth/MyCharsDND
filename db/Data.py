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
    size = db.Column(db.String(20))
    type = db.Column(db.String(50))
    subtype = db.Column(db.String(50))
    alignment = db.Column(db.String(50))
    armor_class = db.Column(db.Integer)
    armor_desc = db.Column(db.String(100))
    hit_points = db.Column(db.Integer)
    hit_dice = db.Column(db.String(20))
    speed = db.Column(db.String(100))
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    perception = db.Column(db.Integer)
    skills = db.Column(db.String(200))
    damage_vulnerabilities = db.Column(db.String(200))
    damage_resistances = db.Column(db.String(200))
    damage_immunities = db.Column(db.String(200))
    condition_immunities = db.Column(db.String(200))
    senses = db.Column(db.String(200))
    languages = db.Column(db.String(200))
    challenge_rating = db.Column(db.Float)
    abilities = db.Column(db.Text)
    actions = db.Column(db.Text)
    legendary_actions = db.Column(db.Text)
    description = db.Column(db.Text)

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
    higher_level = db.Column(db.Text)
    target_type = db.Column(db.String(50))
    ritual = db.Column(db.Boolean)
    reaction_condition = db.Column(db.String(100))
    verbal = db.Column(db.Boolean)
    somatic = db.Column(db.Boolean)
    material = db.Column(db.Boolean)
    material_specified = db.Column(db.Text)
    material_cost = db.Column(db.Integer)
    material_consumed = db.Column(db.Boolean)
    target_count = db.Column(db.Integer)
    saving_throw_ability = db.Column(db.String(50))
    attack_roll = db.Column(db.Boolean)
    damage_roll = db.Column(db.String(50))
    damage_types = db.Column(db.String(100))
    shape_type = db.Column(db.String(50))
    shape_size = db.Column(db.String(50))
    concentration = db.Column(db.Boolean)
    classes = db.Column(db.String(200))

class Background(db.Model):
    __tablename__ = 'backgrounds'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    benefits = db.Column(db.Text)  # Stores the formatted benefits as text

class Plane(db.Model):
    __tablename__ = 'planes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Feat(db.Model):
    __tablename__ = 'feats'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    has_prerequisite = db.Column(db.Boolean)
    prerequisite = db.Column(db.String(100))
    benefits = db.Column(db.Text)  # Stores the formatted benefits as text

class Condition(db.Model):
    __tablename__ = 'conditions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Race(db.Model):
    __tablename__ = 'races'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    traits = db.Column(db.Text)  # Stores the formatted traits as text

class CharacterClass(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    hit_dice = db.Column(db.String(10))
    hp_at_1st_level = db.Column(db.String(100))
    hp_at_higher_levels = db.Column(db.String(100))
    prof_armor = db.Column(db.String(200))
    prof_weapons = db.Column(db.String(200))
    prof_tools = db.Column(db.String(200))
    prof_saving_throws = db.Column(db.String(200))
    prof_skills = db.Column(db.String(200))
    equipment = db.Column(db.Text)
    table = db.Column(db.Text)
    spellcasting_ability = db.Column(db.String(50))
    subtypes_name = db.Column(db.String(100))
    archetypes = db.Column(db.Text)  # Stores the formatted archetypes as text

class MagicItem(db.Model):
    __tablename__ = 'magic_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    description = db.Column(db.Text)
    requires_attunement = db.Column(db.String(100))

class Weapon(db.Model):
    __tablename__ = 'weapons'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    damage_dice = db.Column(db.String(50))
    versatile_dice = db.Column(db.String(50))
    reach = db.Column(db.Float)
    range = db.Column(db.Float)
    long_range = db.Column(db.Float)
    is_versatile = db.Column(db.Boolean)
    is_martial = db.Column(db.Boolean)
    is_finesse = db.Column(db.Boolean)
    is_thrown = db.Column(db.Boolean)
    is_two_handed = db.Column(db.Boolean)
    requires_ammunition = db.Column(db.Boolean)
    requires_loading = db.Column(db.Boolean)
    is_heavy = db.Column(db.Boolean)
    is_light = db.Column(db.Boolean)
    is_lance = db.Column(db.Boolean)
    is_net = db.Column(db.Boolean)
    is_simple = db.Column(db.Boolean)
    is_improvised = db.Column(db.Boolean)

class Armor(db.Model):
    __tablename__ = 'armor'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ac_display = db.Column(db.String(100))
    ac_base = db.Column(db.Integer)
    ac_add_dexmod = db.Column(db.Boolean)
    ac_cap_dexmod = db.Column(db.Integer)
    grants_stealth_disadvantage = db.Column(db.Boolean)
    strength_score_required = db.Column(db.Integer)


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
    # Convert challenge rating to float, handling fractional values
    challenge_rating_str = data.get('challenge_rating', '0')
    try:
        if '/' in challenge_rating_str:
            challenge_rating = float(Fraction(challenge_rating_str))
        else:
            challenge_rating = float(challenge_rating_str)
    except ValueError:
        challenge_rating = 0.0

    # Extract and format fields
    name = data.get('name', '')
    description = data.get('desc', '')
    size = data.get('size', '')
    monster_type = data.get('type', '')
    subtype = data.get('subtype', '')
    alignment = data.get('alignment', '')
    armor_class = data.get('armor_class', 0)
    hit_points = int(data.get('hit_points', 0))
    speed = ', '.join([f"{k}: {v}" for k, v in data.get('speed', {}).items()])
    abilities = data.get('special_abilities', [])
    actions = data.get('actions', [])
    legendary_actions = data.get('legendary_actions', [])
    skills = ', '.join([f"{k}: {v}" for k, v in data.get('skills', {}).items()])

    abilities_text = '; '.join([f"{ability['name']}: {ability['desc']}" for ability in abilities]) if abilities else ''
    actions_text = '; '.join([f"{action['name']}: {action['desc']}" for action in actions]) if actions else ''
    legendary_actions_text = '; '.join([f"{action['name']}: {action['desc']}" for action in legendary_actions]) if legendary_actions else ''

    return {
        'name': name,
        'description': description,  # Changed 'desc' to 'description' to match model field
        'size': size,
        'type': monster_type,
        'subtype': subtype,
        'alignment': alignment,
        'armor_class': armor_class,
        'hit_points': hit_points,
        'speed': speed,
        'strength': data.get('strength', 0),
        'dexterity': data.get('dexterity', 0),
        'constitution': data.get('constitution', 0),
        'intelligence': data.get('intelligence', 0),
        'wisdom': data.get('wisdom', 0),
        'charisma': data.get('charisma', 0),
        'perception': data.get('perception', 0),
        'skills': skills,
        'damage_vulnerabilities': data.get('damage_vulnerabilities', ''),
        'damage_resistances': data.get('damage_resistances', ''),
        'damage_immunities': data.get('damage_immunities', ''),
        'condition_immunities': data.get('condition_immunities', ''),
        'senses': data.get('senses', ''),
        'languages': data.get('languages', ''),
        'challenge_rating': challenge_rating,
        'abilities': abilities_text,
        'actions': actions_text,
        'legendary_actions': legendary_actions_text,
    }

def map_spell_data(data):
    # Extract and format fields
    school_data = data.get('school', {})
    school_name = school_data.get('key', '') if isinstance(school_data, dict) else school_data

    return {
        'name': data.get('name', ''),
        'description': data.get('desc', ''),
        'level': int(data.get('level', 0)),
        'school': school_name,
        'higher_level': data.get('higher_level', ''),
        'target_type': data.get('target_type', ''),
        'range': data.get('range_text', ''),
        'ritual': data.get('ritual', False),
        'casting_time': data.get('casting_time', ''),
        'reaction_condition': data.get('reaction_condition', ''),
        'verbal': data.get('verbal', False),
        'somatic': data.get('somatic', False),
        'material': data.get('material', False),
        'material_specified': data.get('material_specified', ''),
        'material_cost': data.get('material_cost', None),
        'material_consumed': data.get('material_consumed', False),
        'target_count': data.get('target_count', 0),
        'saving_throw_ability': data.get('saving_throw_ability', ''),
        'attack_roll': data.get('attack_roll', False),
        'damage_roll': data.get('damage_roll', ''),
        'damage_types': ', '.join(data.get('damage_types', [])),
        'duration': data.get('duration', ''),
        'shape_type': data.get('shape_type', ''),
        'shape_size': data.get('shape_size', ''),
        'concentration': data.get('concentration', False),
        'classes': ', '.join(data.get('classes', []))
    }

def map_background_data(data):
    # Extract and format fields
    benefits = data.get('benefits', [])

    # Map benefits to a formatted string
    benefits_text = '; '.join([f"{benefit['name']}: {benefit['desc']}" for benefit in benefits]) if benefits else ''

    return {
        'name': data.get('name', ''),
        'description': data.get('desc', ''),
        'benefits': benefits_text
    }

def map_plane_data(data):
    return {
        'name': data.get('name'),
        'description': data.get('desc', '')
    }

def map_feat_data(data):
    # Extract and format fields
    benefits = data.get('benefits', [])

    # Map benefits to a formatted string
    benefits_text = '; '.join([benefit['desc'] for benefit in benefits]) if benefits else ''

    return {
        'name': data.get('name', ''),
        'description': data.get('desc', ''),
        'has_prerequisite': data.get('has_prerequisite', False),
        'prerequisite': data.get('prerequisite', ''),
        'benefits': benefits_text
    }

def map_condition_data(data):
    return {
        'name': data.get('name'),
        'description': data.get('desc', '')
    }

def map_race_data(data):
    # Extract and format fields
    traits = data.get('traits', [])

    # Map traits to a formatted string
    traits_text = '; '.join([f"{trait['name']}: {trait['desc']}" for trait in traits]) if traits else ''

    return {
        'name': data.get('name', ''),
        'description': data.get('desc', ''),
        'traits': traits_text
    }

def map_class_data(data):
    # Extract and format fields
    archetypes = data.get('archetypes', [])

    # Map archetypes to a formatted string
    archetypes_text = '; '.join([f"{archetype['name']}: {archetype['desc']}" for archetype in archetypes]) if archetypes else ''

    return {
        'name': data.get('name', ''),
        'description': data.get('desc', ''),
        'hit_dice': data.get('hit_dice', ''),
        'hp_at_1st_level': data.get('hp_at_1st_level', ''),
        'hp_at_higher_levels': data.get('hp_at_higher_levels', ''),
        'prof_armor': data.get('prof_armor', ''),
        'prof_weapons': data.get('prof_weapons', ''),
        'prof_tools': data.get('prof_tools', ''),
        'prof_saving_throws': data.get('prof_saving_throws', ''),
        'prof_skills': data.get('prof_skills', ''),
        'equipment': data.get('equipment', ''),
        'table': data.get('table', ''),
        'spellcasting_ability': data.get('spellcasting_ability', ''),
        'subtypes_name': data.get('subtypes_name', ''),
        'archetypes': archetypes_text
    }

def map_magic_item_data(data):
    return {
        'name': data.get('name', ''),
        'type': data.get('type', ''),
        'description': data.get('desc', ''),
        'rarity': data.get('rarity', ''),
        'requires_attunement': data.get('requires_attunement', '')
    }

def map_weapon_data(data):
    return {
        'name': data.get('name', ''),
        'damage_dice': data.get('damage_dice', ''),
        'versatile_dice': data.get('versatile_dice', ''),
        'reach': data.get('reach', 0.0),
        'range': data.get('range', 0.0),
        'long_range': data.get('long_range', 0.0),
        'is_versatile': data.get('is_versatile', False),
        'is_martial': data.get('is_martial', False),
        'is_finesse': data.get('is_finesse', False),
        'is_thrown': data.get('is_thrown', False),
        'is_two_handed': data.get('is_two_handed', False),
        'requires_ammunition': data.get('requires_ammunition', False),
        'requires_loading': data.get('requires_loading', False),
        'is_heavy': data.get('is_heavy', False),
        'is_light': data.get('is_light', False),
        'is_lance': data.get('is_lance', False),
        'is_net': data.get('is_net', False),
        'is_simple': data.get('is_simple', False),
        'is_improvised': data.get('is_improvised', False)
    }

def map_armor_data(data):
    return {
        'name': data.get('name', ''),
        'ac_display': data.get('ac_display', ''),
        'ac_base': data.get('ac_base', 0),
        'ac_add_dexmod': data.get('ac_add_dexmod', False),
        'ac_cap_dexmod': data.get('ac_cap_dexmod', None),
        'grants_stealth_disadvantage': data.get('grants_stealth_disadvantage', False),
        'strength_score_required': data.get('strength_score_required', None)
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
