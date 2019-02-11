from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify, request, Blueprint

from app import forms
from app.rsa import RSA


API = Blueprint('api', __name__)


@API.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.GenerateKeyForm(test)
    response = {}
    if form.validate():
        length = form.length.data
        rsa = RSA(length)
        response = {'modulus': format(rsa.modulus, 'x'),
                    'exponent': format(rsa.exponent, 'x'),
                    'secret': format(rsa.secret, 'x')}
    return jsonify(response)


@API.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.EncryptForm(test)
    response = {}
    if form.validate():
        values = RSA._hex_to_int(exponent=form.exponent.data, modulus=form.modulus.data)
        encrypted = RSA.encrypt(message=form.message.data, **values)
        response['encrypted'] = encrypted
    return jsonify(response)


@API.route('/api/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.DecryptForm(test)
    response = {}
    if form.validate():
        variables = {'modulus': data['userStuff']['modulus'],
                     'exponent': data['userStuff']['exponent'],
                     'secret': data['userStuff']['secret']}
        transformed = RSA._hex_to_int(**variables)
        rsa = RSA(**transformed)
        decrypted = rsa.decrypt(form.ciphertext.data)
        response['decrypted'] = decrypted
    return jsonify(response)


@API.route('/api/sign', methods=['POST'])
def sign():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.SignatureForm(test)
    response = {}
    if form.validate():
        variables = {'modulus': data['userStuff']['modulus'],
                     'exponent': data['userStuff']['exponent'],
                     'secret': data['userStuff']['secret']}
        transformed = RSA._hex_to_int(**variables)
        rsa = RSA(**transformed)
        signature = rsa.sign(form.message.data)
        response['signature'] = signature
    return jsonify(response)


@API.route('/api/verify', methods=['POST'])
def verify():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.VerificationForm(test)
    response = {}
    if form.validate():
        variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data, 'signature': form.signature.data}
        transformed = RSA._hex_to_int(**variables)
        transformed['message'] = form.message.data
        verified = RSA.verify(**transformed)
        response['verified'] = verified
    return jsonify(response)


@API.route('/api/send', methods=['POST'])
def send():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.SendKeyForm(test)
    response = {}
    if form.validate():
        parameters = {'modulus': data['userStuff']['modulus'],
                      'exponent': data['userStuff']['exponent'],
                      'secret': data['userStuff']['secret']}
        keys = RSA._hex_to_int(**parameters)
        rsa = RSA(**keys)

        variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data}
        transformed = RSA._hex_to_int(**variables)
        key, signature = rsa.send_key(**transformed)
        response['key'] = key
        response['signature'] = signature
    return jsonify(response)


@API.route('/api/receive', methods=['POST'])
def receive():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.ReceiveKeyForm(test)
    response = {}
    if form.validate():
        parameters = {'modulus': data['userStuff']['modulus'],
                      'exponent': data['userStuff']['exponent'],
                      'secret': data['userStuff']['secret']}
        keys = RSA._hex_to_int(**parameters)
        rsa = RSA(**keys)

        variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data}
        transformed = RSA._hex_to_int(**variables)
        key, signature = rsa.send_key(**transformed)
        response['key'] = key
        response['signature'] = signature
    return jsonify(response)



