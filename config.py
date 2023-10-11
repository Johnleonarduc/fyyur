import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Stop SQLAlchemy warnings on console
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database

DB_NAME = os.getenv("DB_NAME", 'fyyur')
DB_USER = os.getenv("DB_USER", 'postgres')
DB_PASSWORD = os.getenv("DB_PASSWORD", 'your_password')
DB_HOST = os.getenv("DB_HOST", 'localhost')
DB_PORT = os.getenv("DB_PORT", '5432')
#IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

