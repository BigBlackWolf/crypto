import datetime
from app import db


class RSAKeys(db.Model):
    __tablename__ = 'rsa_keys'
    __table_args__ = (
        db.UniqueConstraint('key_size', 'secret', name='unique_secret_key'),
    )

    id = db.Column(db.Integer, primary_key=True)
    key_size = db.Column(db.Integer, nullable=False, default=256)
    module = db.Column(db.Text, nullable=False)
    public_exponent = db.Column(db.Text, nullable=False)
    secret = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.Text, nullable=False)
    expire_date = db.Column(db.DateTime, default=datetime.datetime.now() + datetime.timedelta(hours=24))
    keys = db.relationship('RSAKeys', backref='keys')
