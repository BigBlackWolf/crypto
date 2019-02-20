from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify, request, Blueprint

from app import forms
from app import tasks
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
        rsa = tasks.generate.delay(length)
        response = rsa.wait()
    return jsonify(response)


@API.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.EncryptForm(test)
    response = {}
    if form.validate():
        task = tasks.transform.delay(exponent=form.exponent.data, modulus=form.modulus.data)
        values = task.wait()
        task_encrypt = tasks.encrypt.delay(message=form.message.data, **values)
        response = task_encrypt.wait()
    return jsonify(response)


@API.route('/api/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.DecryptForm(test)
    response = {}
    if form.validate():
        variables = data['userStuff']
        task = tasks.transform.delay(**variables)
        transformed = task.wait()
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
        variables = data['userStuff']
        task = tasks.transform.delay(**variables)
        transformed = task.wait()
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
        variables = data['form']
        task = tasks.transform.delay(**variables)
        transformed = task.wait()
        transformed['message'] = form.message.data
        task_verify = tasks.verify.delay(**transformed)
        response = task_verify.wait()
    return jsonify(response)


@API.route('/api/send', methods=['POST'])
def send():
    data = request.get_json()
    test = ImmutableMultiDict(data.get('form').items())
    form = forms.SendKeyForm(test)
    response = {}
    if form.validate():
        parameters = data['userStuff']
        task = tasks.transform.delay(**parameters)
        keys = task.wait()
        rsa = RSA(**keys)

        task = tasks.transform.delay(**data['form'])
        transformed = task.wait()
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
        parameters = data['userStuff']
        task = tasks.transform.delay(**parameters)
        keys = task.wait()
        rsa = RSA(**keys)

        variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data}
        task = tasks.transform.delay(**variables)
        transformed = task.wait()
        key, signature = rsa.receive_key(**transformed)
        response['key'] = key
        response['signature'] = signature
    return jsonify(response)



