from wtforms import IntegerField, validators, StringField
from flask_wtf import FlaskForm


class EncryptForm(FlaskForm):
    message = StringField()
    key = StringField()


class DecryptForm(FlaskForm):
    ciphertext = StringField()
    key = StringField()
