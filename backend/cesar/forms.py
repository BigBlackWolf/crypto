from wtforms import IntegerField, validators, StringField
from flask_wtf import FlaskForm


class EncryptForm(FlaskForm):
    message = StringField()
    length = IntegerField(validators=[validators.NumberRange(1, 30)])


class DecryptForm(FlaskForm):
    ciphertext = StringField()
    length = IntegerField(validators=[validators.NumberRange(1, 30)])
