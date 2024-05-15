from string import ascii_letters, digits
from random import choice
from log_decorator import log
import logging


@log()
class PasswordGenerator:
    def __init__(self, length, charset, count):
        self.length = length
        self.charset = charset
        self.count = count

    def __iter__(self):
        return self

    def __next__(self):
        if self.count <= 0:
            raise StopIteration()

        password = self.generate_passoword()
        self.count -= 1
        return password

    def generate_passoword(self) -> str:
        return "".join(choice(self.charset) for _ in range(self.length))



if __name__ == "__main__":
    chars = ascii_letters + digits
    gen1 = PasswordGenerator(10, chars, 5)
    gen2 = PasswordGenerator(20, chars, 3)

    for i, psswd in enumerate(gen1):
        print(i, "gen1", psswd)

    try:
        next(gen1)
    except StopIteration:
        print("generator wyczerpany :(")

    for _ in range(10):
        print("gen2", next(gen2))
