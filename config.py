import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "db/dnd_database.db")}'
    DEBUG = False

config = {
    'development': DevelopmentConfig,
}
