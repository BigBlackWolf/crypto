from flask import render_template, make_response, jsonify
from werkzeug.datastructures import ImmutableMultiDict
from flask.views import MethodView
from flask import request
import logging

from app.rsa import RSA
from app import forms
from app.models import RSAKeys, Users
from app.extensions import db, cache


class GenerateHandler(MethodView):
    template = 'generate.html'

    @cache.cached(timeout=50)
    def get(self):
        form = forms.GenerateKeyForm(request.form)
        response = make_response(render_template(self.template, form=form))
        if not request.cookies.get('user'):
            response.set_cookie('user', '1')
        return response

    def post(self):
        form = forms.GenerateKeyForm(request.form)
        user = request.cookies.get('user')

        logging.info('User: ' + user)
        keys_objs = Users.query.get(user).keys
        keys = {i.key_size for i in keys_objs}
        if form.validate():
            length = form.length.data
            if length in keys:
                result = RSAKeys.query.filter_by(user_id=user, key_size=length)[0]
                modulus = result.module
                exponent = result.public_exponent
            else:
                rsa = RSA(length)
                modulus = hex(rsa.modulus)[2:]
                exponent = hex(rsa.exponent)[2:]
                _secret = hex(rsa.secret)[2:]
                keys = RSAKeys(key_size=length, module=modulus, public_exponent=exponent, secret=_secret, user_id=user)
                db.session.add(keys)
                db.session.commit()
            result = {'modulus': modulus, 'exponent': exponent}
            response = make_response(render_template(self.template, form=form, **result))
            response.set_cookie('length', str(length))
            return response
        return render_template(self.template, form=form)


class EncryptHandler(MethodView):
    template = 'encrypt.html'

    def get(self):
        form = forms.EncryptForm(request.form)
        return render_template(self.template, form=form)

    def post(self):
        form = forms.EncryptForm(request.form)
        if form.validate():
            variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data}
            transformed = RSA._to_int(**variables)
            rsa = RSA(**transformed)
            encrypted = rsa.encrypt(form.message.data)
            return render_template(self.template, form=form, encrypted=encrypted)
        return render_template(self.template, form=form)


class DecryptHandler(MethodView):
    template = 'decrypt.html'

    def get(self):
        form = forms.DecryptForm(request.form)
        return render_template(self.template, form=form)

    def post(self):
        form = forms.DecryptForm(request.form)
        user = request.cookies.get('user')
        length = request.cookies.get('length')
        if form.validate():
            result = RSAKeys.query.filter_by(user_id=user, key_size=length)[0]
            variables = {'modulus': result.module, 'exponent': result.public_exponent, 'secret': result.secret}
            transformed = RSA._to_int(**variables)
            rsa = RSA(**transformed)
            number = RSA._to_int(text=form.ciphertext.data)
            decrypted = rsa.decrypt(**number)
            return render_template(self.template, form=form, decrypted=decrypted)
        return render_template(self.template, form=form)


class SignatureHandler(MethodView):
    template = 'signature.html'

    def get(self):
        form = forms.SignatureForm(request.form)
        return render_template(self.template, form=form)

    def post(self):
        form = forms.SignatureForm(request.form)
        user = request.cookies.get('user')
        length = request.cookies.get('length')
        if form.validate():
            result = RSAKeys.query.filter_by(user_id=user, key_size=length)[0]
            variables = {'modulus': result.module, 'exponent': result.public_exponent, 'secret': result.secret}
            transformed = RSA._to_int(**variables)
            rsa = RSA(**transformed)
            signature = rsa.sign(form.message.data)
            return render_template(self.template, form=form, signature=signature)
        return render_template(self.template, form=form)


class VerifyHandler(MethodView):
    template = 'verify.html'

    def get(self):
        form = forms.VerificationForm(request.form)
        return render_template(self.template, form=form)

    def post(self):
        form = forms.VerificationForm(request.form)
        if form.validate():
            variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data, 'signature': form.signature.data}
            transformed = RSA._to_int(**variables)
            transformed['message'] = form.message.data
            verification = RSA.verify(**transformed)
            return render_template(self.template, form=form, verification=verification)
        return render_template(self.template, form=form)


class SendHandler(MethodView):
    template = 'send_key.html'

    def get(self):
        form = forms.SendKeyForm(request.form)
        return render_template(self.template, form=form)

    def post(self):
        form = forms.SendKeyForm(request.form)
        user = request.cookies.get('user')
        length = request.cookies.get('length')
        if form.validate():
            result = RSAKeys.query.filter_by(user_id=user, key_size=length)[0]
            parameters = {'modulus': result.module, 'exponent': result.public_exponent, 'secret': result.secret}
            keys = RSA._to_int(**parameters)
            sender = RSA(**keys)

            variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data}
            transformed = RSA._to_int(**variables)
            key, signature = sender.send_key(**transformed)
            return render_template(self.template, form=form, key=key, signature=signature)
        return render_template(self.template, form=form)


class ReceiveHandler(MethodView):
    template = 'receive_key.html'

    def get(self):
        form = forms.ReceiveKeyForm(request.form)
        return render_template(self.template, form=form)

    def post(self):
        form = forms.ReceiveKeyForm(request.form)
        user = request.cookies.get('user')
        length = request.cookies.get('length')
        if form.validate():
            result = RSAKeys.query.filter_by(user_id=user, key_size=length)[0]
            parameters = {'modulus': result.module, 'exponent': result.public_exponent, 'secret': result.secret}
            keys = RSA._to_int(**parameters)
            receiver = RSA(**keys)

            variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data,
                         'signature': form.signature.data, 'key': form.key.data}
            transformed = RSA._to_int(**variables)
            key, verification = receiver.receive_key(**transformed)
            return render_template(self.template, form=form, key=key, verification=verification)
        return render_template(self.template, form=form)


class APIView(MethodView):
    def post(self):
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


class EncryptAPIView(MethodView):
    def post(self):
        data = request.get_json()
        test = ImmutableMultiDict(data.get('form').items())
        form = forms.EncryptForm(test)
        response = {}
        if form.validate():
            variables = {'modulus': data['userStuff']['modulus'],
                         'exponent': data['userStuff']['exponent'],
                         'secret': data['userStuff']['secret']}
            transformed = RSA._to_int(**variables)
            rsa = RSA(**transformed)
            encrypted = rsa.encrypt(form.message.data)
            response['encrypted'] = encrypted
        return jsonify(response)


class DecryptAPIView(MethodView):
    def post(self):
        data = request.get_json()
        test = ImmutableMultiDict(data.get('form').items())
        form = forms.DecryptForm(test)
        response = {}
        if form.validate():
            variables = {'modulus': data['userStuff']['modulus'],
                         'exponent': data['userStuff']['exponent'],
                         'secret': data['userStuff']['secret']}
            transformed = RSA._to_int(**variables)
            rsa = RSA(**transformed)
            number = RSA._to_int(text=form.ciphertext.data)
            decrypted = rsa.decrypt(**number)
            response['decrypted'] = decrypted
        return jsonify(response)


class SignatureAPIView(MethodView):
    def post(self):
        data = request.get_json()
        test = ImmutableMultiDict(data.get('form').items())
        form = forms.SignatureForm(test)
        response = {}
        if form.validate():
            variables = {'modulus': data['userStuff']['modulus'],
                         'exponent': data['userStuff']['exponent'],
                         'secret': data['userStuff']['secret']}
            transformed = RSA._to_int(**variables)
            rsa = RSA(**transformed)
            signature = rsa.encrypt(form.message.data)
            response['signature'] = signature
        return jsonify(response)


class VerifyAPIView(MethodView):
    def post(self):
        data = request.get_json()
        test = ImmutableMultiDict(data.get('form').items())
        form = forms.VerificationForm(test)
        response = {}
        if form.validate():
            variables = {'modulus': data['userStuff']['modulus'],
                         'exponent': data['userStuff']['exponent'],
                         'signature': form.signature.data}
            transformed = RSA._to_int(**variables)
            transformed['message'] = form.message.data
            verified = RSA.verify(**transformed)
            response['verified'] = verified
        return jsonify(response)


class SendAPIView(MethodView):
    def post(self):
        data = request.get_json()
        test = ImmutableMultiDict(data.get('form').items())
        form = forms.SendKeyForm(test)
        response = {}
        if form.validate():
            parameters = {'modulus': data['userStuff']['modulus'],
                          'exponent': data['userStuff']['exponent'],
                          'secret': data['userStuff']['secret']}
            keys = RSA._to_int(**parameters)
            rsa = RSA(**keys)

            variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data}
            transformed = RSA._to_int(**variables)
            key, signature = rsa.send_key(**transformed)
            response['key'] = key
            response['signature'] = signature
        return jsonify(response)


class ReceiveAPIView(MethodView):
    def post(self):
        data = request.get_json()
        test = ImmutableMultiDict(data.get('form').items())
        form = forms.ReceiveKeyForm(test)
        response = {}
        if form.validate():
            parameters = {'modulus': data['userStuff']['modulus'],
                          'exponent': data['userStuff']['exponent'],
                          'secret': data['userStuff']['secret']}
            keys = RSA._to_int(**parameters)
            rsa = RSA(**keys)

            variables = {'modulus': form.modulus.data, 'exponent': form.exponent.data}
            transformed = RSA._to_int(**variables)
            key, signature = rsa.send_key(**transformed)
            response['key'] = key
            response['signature'] = signature
        return jsonify(response)
