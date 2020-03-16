from string import ascii_lowercase


class Vigenere:
    def __init__(self, word: str):
        self._key = word.lower()

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str):
        self._key = key

    def _equal_key(self, text: str) -> str:
        length = len(text) // len(self._key)
        long_key = self._key * length
        to_add = len(text) - len(long_key)
        long_key += self._key[:to_add]
        return long_key

    def _logic(self, text: str, encrypt: bool = True) -> str:
        key = self._equal_key(text)
        key_list = list(key)
        text_list = list(text.lower())
        for i in range(len(text_list)):
            index = ascii_lowercase.index(text_list[i])
            shift = ascii_lowercase.index(key_list[i])
            if not encrypt:
                shift = -shift
            new_letter = ascii_lowercase[(index + shift) % len(ascii_lowercase)]
            text_list[i] = new_letter
        return ''.join(text_list)

    def encrypt(self, text: str) -> str:
        return self._logic(text, encrypt=True)

    def decrypt(self, text: str) -> str:
        return self._logic(text, encrypt=False)

