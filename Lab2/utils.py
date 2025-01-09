import random
from math import gcd

def generate_prime():
    while True:
        num = random.randint(2, 1024)
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            return num

def find_e(euler):
    while True:
        e = random.randint(1, euler - 1)
        if gcd(e, euler) == 1 and e % 2 != 0:
            return e

def euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = euclid(b % a, a)
        return gcd, y - (b // a) * x, x

def find_d(e, euler):
    gcd, x, y = euclid(e, euler)
    if gcd != 1:
        raise Exception("RSA error")
    else:
        return x % euler

def find_r(n):
    while True:
        r = random.randint(1, n - 1)
        if gcd(r, n) == 1:
            return r


def generate_rsa_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    euler = (p - 1) * (q - 1)
    while True:
        e = random.randint(1, euler - 1)
        if gcd(e, euler) == 1 and e % 2 != 0:
            break
    _gcd, x, y = euclid(e, euler)
    if _gcd != 1:
        raise Exception("RSA error")
    else:
        d = x % euler
    return n, e, d

def encrypt(message, public_key, mask):
    n, e = public_key
    numeric_message = [ord(char) for char in message]
    cipher_text = [(pow((char * mask), e, n)) for char in numeric_message]
    return cipher_text


def decrypt(cipher_text, private_key, mask):
    n, d = private_key
    decrypted_message = [(pow(char, d, n) * pow(mask, -1, n)) % n for char in cipher_text]
    original_message = ''.join([chr(char) for char in decrypted_message])
    return original_message

def cvk_signature(cipher_text, private_key):
    n, d = private_key
    message = [pow(char, d, n) for char in cipher_text]
    return message


def remove_mask(str1, mask, public_key):
    n, e = public_key
    s_int = [(char * pow(mask, -1, n)) % n for char in str1]
    str_result = ''.join([chr(char) for char in s_int])
    return str_result

def formatting(ballots):
    data_array = []
    for ballot in ballots:
        lines = ballot.split("\n")
        data = {}
        for line in lines:
            parts = line.split(", ")
            for part in parts:
                if ": " in part:
                    key, value = part.split(": ", 1)  # Розділити лише на першому входженні ": "
                    data[key] = value
        data_array.append(data)
    return data_array
