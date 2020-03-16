from rsa import api as rsa
from cesar import api as cesar
from vigenere import api as vigenere


def setup_routes(app):
    app.register_blueprint(rsa.API)
    app.register_blueprint(cesar.API)
    app.register_blueprint(vigenere.API)
