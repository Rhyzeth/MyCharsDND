import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db', 'dnd_database.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
