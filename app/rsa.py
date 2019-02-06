import random
import binascii
from functools import reduce


class RSA:
    def __init__(self, length=None, modulus=None, exponent=None, secret=None):
        if length or not any((modulus, exponent, secret, length)):
            self.generate_rsa_keys(length)
        else:
            self.modulus = modulus
            self.exponent = exponent
            self._secret = secret

    def generate_rsa_keys(self, length):
        p = self._easy_number(length)
        q = self._easy_number(length)
        n = q * p
        oiler = (p - 1) * (q - 1)
        while True:
            e = random.randint(2, oiler)
            if self._gcd(e, oiler) == 1:
                break

        d = self._bezout_recursive(e, oiler)[0]
        if d < 0:
            d = oiler + d

        self.modulus, self.exponent = n, e
        self._secret = d

    def encrypt(self, text):
        value = self._text_to_value(text)
        encrypted = pow(value, self.exponent, self.modulus)
        # hex(encrypted)[2:]
        return format(encrypted, 'x')

    def decrypt(self, text):
        text = pow(text, self._secret, self.modulus)
        return self._value_to_text(text)

    def sign(self, text):
        value = self._text_to_value(text)
        encrypted = pow(value, self._secret, self.modulus)
        return hex(encrypted)[2:]

    @staticmethod
    def verify(modulus, exponent, message, signature):
        to_check = RSA._text_to_value(message)
        return True if pow(signature, exponent, modulus) == to_check else False

    def send_key(self, modulus, exponent):
        while modulus < self.modulus:
            length = len(bin(modulus)[2:]) / 2 - 1
            self.generate_rsa_keys(length)
        k = random.randint(1, self.modulus)
        k1 = pow(k, exponent, modulus)
        s = pow(k, self._secret, self.modulus)
        s1 = pow(s, exponent, modulus)
        return hex(k1)[2:], hex(s1)[2:]

    def receive_key(self, modulus, exponent, key, signature):
        k = pow(key, self._secret, self.modulus)
        s = pow(signature, self._secret, self.modulus)
        return hex(k)[2:], True if k == pow(s, exponent, modulus) else False

    @property
    def secret(self):
        return self._secret

    @staticmethod
    def _text_to_value(text):
        tmp = binascii.hexlify(bytes(text, 'utf-8'))
        return int(tmp, 16)

    @staticmethod
    def _value_to_text(value):
        number = hex(value)[2:]
        represented = bytes(number, 'utf-8')
        result = binascii.unhexlify(represented)
        return result.decode('utf-8')

    @staticmethod
    def _easy_number(n0=None):
        if n0 is None:
            n0 = 128
        while True:
            test = random.randint(2 ** (n0 - 1), 2 ** n0)
            if RSA._pascal(test):
                if RSA._miller_test(test):
                    break
        return test

    @staticmethod
    def _gcd(a, b):
        if a < 0:
            tmp = str(a)
            a = int(tmp[1:])
        while a != 0 and b != 0:
            if a > b:
                a -= b
            else:
                b -= a
        return a if a != 0 else b

    @staticmethod
    def _pascal(n, limit=256):
        eratos = [i for i in range(2, limit + 1)]
        for i in eratos:
            if i in eratos:
                eratos = list(filter(lambda x: x % i != 0 or x == i, eratos))

        numbers = list(str(n))
        for i in eratos:
            length = len(numbers) - 1
            decaded_list = []
            for j in numbers:
                decaded_list.append((int(j), pow(10, length, i)))
                length -= 1
            temp = reduce(lambda x, y: x + y[0] * y[1], decaded_list, 0)
            if temp % i == 0:
                return False
        return True

    @staticmethod
    def _miller_test(p):
        d = p - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        x = random.randint(2, p - 1)
        if RSA._gcd(x, p) != 1:
            return False
        r = pow(x, d, p)
        if r != 1:
            for i in range(1, s):
                if r == 1:
                    return False
                else:
                    r *= r
                    r %= p
            if r != -1:
                return False
        return True

    @staticmethod
    def _bezout_recursive(a, b):
        if not b:
            return 1, 0, a
        y, x, g = RSA._bezout_recursive(b, a % b)
        return x, y - (a // b) * x, g

    @staticmethod
    def _to_int(**kwargs):
        for key, value in kwargs.items():
            new_value = int('0x' + value, 16)
            kwargs[key] = new_value
        return kwargs
