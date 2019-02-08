from wtforms import IntegerField, validators, StringField
from flask_wtf import FlaskForm
import re

hex_regexp = re.compile('[0-9a-fA-F]+')


class GenerateKeyForm(FlaskForm):
    length = IntegerField(validators=[validators.NumberRange(64, 1024)])


class EncryptForm(FlaskForm):
    modulus = StringField(validators=[validators.Regexp(hex_regexp)])
    exponent = StringField(validators=[validators.Regexp(hex_regexp)])
    message = StringField(validators=[validators.Length(min=1, max=1024)])


class DecryptForm(FlaskForm):
    ciphertext = StringField(validators=[validators.Regexp(hex_regexp)])


class SignatureForm(FlaskForm):
    message = StringField(validators=[validators.Length(min=1, max=1024)])


class VerificationForm(FlaskForm):
    message = StringField(validators=[validators.Length(min=1, max=1024)])
    signature = StringField(validators=[validators.Length(min=1, max=1024)])
    modulus = StringField(validators=[validators.Regexp(hex_regexp)])
    exponent = StringField(validators=[validators.Regexp(hex_regexp)])


class SendKeyForm(FlaskForm):
    modulus = StringField(validators=[validators.Regexp(hex_regexp)])
    exponent = StringField(validators=[validators.Regexp(hex_regexp)])


class ReceiveKeyForm(FlaskForm):
    key = StringField(validators=[validators.Length(min=1, max=1024)])
    signature = StringField(validators=[validators.Length(min=1, max=1024)])
    modulus = StringField(validators=[validators.Regexp(hex_regexp)])
    exponent = StringField(validators=[validators.Regexp(hex_regexp)])