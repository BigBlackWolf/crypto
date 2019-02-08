from flask import Flask

from app.extensions import db, migrate, cache, cors
from app.routes import setup_routes
from app.models import RSAKeys


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    setup_routes(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    return app
