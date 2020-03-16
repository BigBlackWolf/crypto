from string import ascii_lowercase


class Cesar:
    def __init__(self, shift: int = 2):
        self._shift = shift

    @property
    def shift(self) -> int:
        return self._shift

    @shift.setter
    def shift(self, shift: int):
        self._shift = shift

    def _logic(self, string: str, encrypt: bool = True) -> str:
        shift = self._shift
        if not encrypt:
            shift = -shift
        list_string = list(string.lower())
        for i in range(len(list_string)):
            index = ascii_lowercase.index(list_string[i])
            new_letter = ascii_lowercase[(index + shift) % len(ascii_lowercase)]
            list_string[i] = new_letter
        return ''.join(list_string)

    def encrypt(self, string: str) -> str:
        return self._logic(string, encrypt=True)

    def decrypt(self, string: str) -> str:
        return self._logic(string, encrypt=False)
