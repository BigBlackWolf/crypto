# Example of config file
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
WTF_CSRF_ENABLED = False
SECRET_KEY = os.getenv('SECRET_KEY') or 'this-really-needs-to-be-changed'

DATABASE = {
    'engine': 'postgresql',
    'database': os.getenv('POSTGRES_DB') or 'aiohttp_crypto',
    'user': os.getenv('POSTGRES_USER') or 'crypto_user',
    'password': os.getenv('POSTGRES_PASSWORD') or 'crypto_user',
    'host': os.getenv('POSTGRES_HOST') or 'localhost',
    'port': os.getenv('POSTGRES_PORT') or '5432',
    'minsize': 1,
    'maxsize': 5
}

SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{database}'.format(**DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
