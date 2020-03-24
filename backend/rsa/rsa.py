import random
import binascii
import ctypes
from functools import reduce

gen_lib = ctypes.CDLL("./gen_lib.so")
gen_lib.gcd.restype = ctypes.c_uint64
gen_lib.gcd.argtypes = [ctypes.c_uint64, ctypes.c_uint64]


class RSA:
    def __init__(self, length: int=None, modulus: int=None, exponent: int=None, secret: int=None):
        """Initialise an instance.

        Require length OR (modulus, exponent and secret).
        If specified length will be generated keys with such length,
        in other way will be initialised custom keys.
        """
        if length or not any((modulus, exponent, secret, length)):
            self.generate_rsa_keys(length)
        else:
            self.modulus = modulus
            self.exponent = exponent
            self._secret = secret

    def generate_rsa_keys(self, length: int):
        """Generate RSA keys.

        Getting required argument length and generating numbers with such length,
        using RSA keys generating algorithm. Then setting values to instance.
        """
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
            d += oiler

        self.modulus, self.exponent = n, e
        self._secret = d

    @staticmethod
    def encrypt(message: str, exponent: int, modulus: int) -> str:
        """Encrypt message, using RSA encryption algorithm. Return value in hex."""
        new_message = RSA._text_to_value(message)
        encrypted = pow(*new_message, exponent, modulus)
        return format(encrypted, 'x')

    def decrypt(self, text: str) -> str:
        """Decrypt message, using RSA decryption algorithm. Return value in hex."""
        dict_text = self._hex_to_int(text=text)
        text = pow(dict_text['text'], self._secret, self.modulus)
        return self._value_to_text(text)

    def sign(self, text: str) -> str:
        """Creating signature of message, using RSA signature creation algorithm.
        Return value in hex.
        """
        value = self._text_to_value(text)
        encrypted = pow(*value, self._secret, self.modulus)
        return format(encrypted, 'x')

    @staticmethod
    def verify(modulus: int, exponent: int, message: str, signature: int) -> bool:
        """Decrypt message, using RSA decryption algorithm. Return value in hex."""
        to_check = RSA._text_to_value(message)
        return True if pow(signature, exponent, modulus) == next(to_check) else False

    def send_key(self, modulus: int, exponent: int) -> (str, str):
        """Generating key and signature to second user.
         Return value in hex.
         """
        while modulus < self.modulus:
            length = round(len(format(modulus, 'b')) / 2) - 1
            self.generate_rsa_keys(length)
        k = random.randint(1, self.modulus)
        k1 = pow(k, exponent, modulus)
        s = pow(k, self._secret, self.modulus)
        s1 = pow(s, exponent, modulus)
        return format(k1, 'x'), format(s1, 'x')

    def receive_key(self, modulus: int, exponent: int, key: int, signature: int) -> (str, bool):
        """Check received credentials and generate own key."""
        k = pow(key, self._secret, self.modulus)
        s = pow(signature, self._secret, self.modulus)
        return format(k, 'x'), True if k == pow(s, exponent, modulus) else False

    @property
    def secret(self) -> int:
        return self._secret

    @staticmethod
    def _text_to_value(*args):
        """Get text values to be formatted to hex-view.
        Return generator of hexes.
        """
        hexed = [binascii.hexlify(bytes(item, 'utf-8')) for item in args]
        result = map(lambda x: int(x, 16), hexed)
        return result

    @staticmethod
    def _value_to_text(value: int) -> str:
        """Get integer value (not hex) and transform it to `utf-8`."""
        number = format(value, 'x')
        represented = bytes(number, 'utf-8')
        result = binascii.unhexlify(represented)
        return result.decode('utf-8')

    @staticmethod
    def _easy_number(n0: int=None) -> int:
        """Generate pseudo-simple number with n0 base."""
        if n0 is None:
            n0 = 128
        while True:
            test = random.randint(2 ** (n0 - 1), 2 ** n0)
            if RSA._pascal(test):
                if RSA._miller_test(test):
                    break
        return test

    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """Greatest common division of two numbers."""
        return gen_lib.gcd(a, b)

    @staticmethod
    def _pascal(n: int, limit: int=128) -> bool:
        """Pre-checks for simplicity by division on first simple numbers."""
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
    def _miller_test(p: int) -> bool:
        """Simplicity check by Miller-Rabin test."""
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
    def _bezout_recursive(a: int, b: int) -> (int, int, int):
        """Advanced euclidean algorithm."""
        # TODO: fix max recursion error for 2048+ keys
        if not b:
            return 1, 0, a
        y, x, g = RSA._bezout_recursive(b, a % b)
        return x, y - (a // b) * x, g

    @staticmethod
    def _hex_to_int(**kwargs) -> dict:
        """Get dict of hex values (without 0x) and format them to integer."""
        for key, value in kwargs.items():
            new_value = int(''.join(('0x', value)), 16)
            kwargs[key] = new_value
        return kwargs
