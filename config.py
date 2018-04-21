import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Connect to the database(relative path)
SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db' 

# upload photos
UPLOADED_PHOTOS_DEST = 'static/img'
