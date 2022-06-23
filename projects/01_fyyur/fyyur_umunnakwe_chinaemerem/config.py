import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Stop SQLAlchemy warnings on console
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database


#IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:7856Julcd07@localhost:5432/fyyur'
