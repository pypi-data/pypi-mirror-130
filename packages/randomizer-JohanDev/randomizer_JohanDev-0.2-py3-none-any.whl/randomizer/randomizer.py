import string
import random

letters = list(string.ascii_letters)
digits = list(string.digits)


def generate(mode, length, num1=None, num2=None):
    value = str("")
    if mode == "letter":
        for _ in range(length):
            value = value + str(random.choice(letters))
        return value
    elif mode == "digit":
        for _ in range(length):
            value = value + str(random.choice(digits))
        return value
    elif mode == "numtonum":
        if num1 is None:
            print("Error, please apply argument.")
            if num2 is None:
                print("Error, please apply argument.")
        else:
            if num2 is None:
                print("Error, please apply argument.")
            else:
                # Good we know the user has all arguments
                for _ in range(length):
                    value = value + str(random.randint(num1, num2))
                return value
