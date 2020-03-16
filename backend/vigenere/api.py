from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify, request, Blueprint

from vigenere import forms
from vigenere.vigenere import Vigenere


API = Blueprint('vigenere_api', __name__, url_prefix='/vigenere')


@API.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.EncryptForm(test)
    response = {}
    if form.validate():
        cesar = Vigenere(form.key.data)
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
        cesar = Vigenere(form.key.data)
        decrypted = cesar.decrypt(form.ciphertext.data)
        response['decrypted'] = decrypted
    return jsonify(response)


