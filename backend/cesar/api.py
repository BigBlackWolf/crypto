from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify, request, Blueprint

from cesar import forms
from cesar.cesar import Cesar


API = Blueprint('cesar_api', __name__, url_prefix='/cesar')


@API.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.EncryptForm(test)
    response = {}
    if form.validate():
        cesar = Cesar(form.length.data)
        encrypted = cesar.encrypt(form.message.data)
        response['encrypted'] = encrypted
    return jsonify(response)


@API.route('/api/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.DecryptForm(test)
    response = {}
    if form.validate():
        cesar = Cesar(form.length.data)
        decrypted = cesar.decrypt(form.ciphertext.data)
        response['decrypted'] = decrypted
    return jsonify(response)


