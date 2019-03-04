from rsa import api


def setup_routes(app):
    app.register_blueprint(api.API)
