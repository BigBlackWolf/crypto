# Example of config file
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
WTF_CSRF_ENABLED = False
SECRET_KEY = 'this-really-needs-to-be-changed'

DATABASE = {
    'engine': 'postgresql',
    'database': 'aiohttp_crypto',
    'user': 'crypto_user',
    'password': 'crypto_user',
    'host': 'db',
    'port': '5432',
    'minsize': 1,
    'maxsize': 5
}

SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{database}'.format(**DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
