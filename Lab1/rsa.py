import random
import math

def generate_rsa_key_pair():

    def generate_prime_number(bit_length):
        max_val = 2 ** bit_length - 1
        while True:
            random_number = random.randint(2**(bit_length-1), max_val)
            if is_prime(random_number):
                return random_number

    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def generate_public_key_exponent(phi):
        public_key_exponent = 65537
        if math.gcd(public_key_exponent, phi) == 1:
            return public_key_exponent
        else:
            raise ValueError('RSA error')

    def generate_private_key_exponent(e, phi):
        d = 0
        x1, x2, y1 = 0, 1, 1
        temp_phi = phi

        while e > 0:
            quotient = temp_phi // e
            remainder = temp_phi % e
            temp_phi = e
            e = remainder
            x = x2 - quotient * x1
            y = d - quotient * y1
            x2, x1 = x1, x
            d, y1 = y1, y
        if temp_phi == 1:
            if d < 0:
                d += phi
            return d
        else:
            raise ValueError('RSA error')

    p = generate_prime_number(8)
    q = generate_prime_number(8)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_public_key_exponent(phi)
    d = generate_private_key_exponent(e, phi)
    public_key = {'e': e, 'n': n}
    private_key = {'d': d, 'n': n}

    return {'publicKey': public_key, 'privateKey': private_key}
