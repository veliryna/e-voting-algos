import random
from utils import *

def registration_bureau(name):
    if check_voter('names_numbers.txt', name):
        number = random.randint(10 ** 10, 10 ** 11 - 1)
        write_to_file('names_numbers.txt', name, number)
        write_to_file('reg_numbers.txt', number)
        print("You've been registered in Registration Bureau.")
        return number
    else:
        raise Exception("Voter with this name is already registered.")

