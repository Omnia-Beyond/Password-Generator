from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choice

class Generator:
    def __init__(self, len, choices):
        self.__len = len
        self.__choices = choices
        self.__alphabet = {
            0: ascii_lowercase,
            1: ascii_uppercase,
            2: digits,
            3: punctuation
        }

    def generatePwd(self):
        alphabet = ""
        pwd = ""
        for pos,i in enumerate(self.__choices):
            if i == 1: alphabet += self.__alphabet[pos]
        
        for i in range(self.__len):
            pwd += choice(alphabet)

        return pwd