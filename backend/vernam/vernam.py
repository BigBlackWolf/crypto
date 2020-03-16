from string import ascii_lowercase


class Vernam:
    def __init__(self, source: str):
        self._key = source

    def _logic(self, text: str, encrypt: bool = True) -> str:
        key_list = list(self._key)
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
        if len(text) > len(self._key):
            return "Set longer key or shorter message"
        return self._logic(text, encrypt=True)

    def decrypt(self, text: str) -> str:
        if len(text) > len(self._key):
            return "Wrong input"
        return self._logic(text, encrypt=False)
