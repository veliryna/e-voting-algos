import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils


def generate_random_string(length=4):
    random_bytes = os.urandom(length)
    random_hex_string = random_bytes.hex()
    return random_hex_string


def add_random_string(message, random_string):
    if isinstance(message, int):
        message = str(message)
        return message.encode('utf-8') + random_string.encode('utf-8')
    elif isinstance(message, bytes):
        return message + random_string.encode('utf-8')
    elif isinstance(message, str):
        return message.encode('utf-8') + random_string.encode('utf-8')
    else:
        raise ValueError("Error: cannot add random string")


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt(message, public_key):
    max_block_size = 100
    blocks = [message[i:i + max_block_size] for i in range(0, len(message), max_block_size)]
    encrypted_blocks = []
    for block in blocks:
        ciphertext = public_key.encrypt(
            block,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_blocks.append(ciphertext)
    return b''.join(encrypted_blocks)


def decrypt(ciphertext, private_key):
    max_block_size = 256
    encrypted_blocks = [ciphertext[i:i + max_block_size] for i in range(0, len(ciphertext), max_block_size)]
    decrypted_blocks = []
    for block in encrypted_blocks:
        plaintext = private_key.decrypt(
            block,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        decrypted_blocks.append(plaintext)
    return b''.join(decrypted_blocks)


def remove_string(byte_string, num_bytes):
    return byte_string[:-num_bytes]


def check_own_random_string(string, strings):
    if string.encode('utf-8') in strings:
        print('Random strings for Voter X are valid')
    else:
        raise Exception('Invalid check: random strings')


def check_own_ballots(m1, m2):
    try:
        for i in range(4):
            for j in range(4):
                if m1[i] == m2[j]:
                    print('Ballot check for Voter X is valid')
    except Exception:
        raise Exception('Invalid check: ballots')


def generate_keys_elgamal():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key


def sign_message(private_key, message):
    return private_key.sign(message, ec.ECDSA(hashes.SHA256()))


def hash_message(message):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(message)
    return digest.finalize()


def verify_signature(public_key, signature, hashed_message):
    try:
        public_key.verify(signature, hashed_message, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        print('Elgamal signature verification was successful')
    except Exception:
        raise Exception('Elgamal signature verification failed')


def extract_last_8_bytes(data):
    return data[-8:]


def check_amount_of_messages(voters, votes):
    if len(voters) == len(votes):
        print('Number of ballots is correct')
    else:
        raise Exception('Number of received ballots is not correct')


def shuffle_ballots(lst, idx):
    return [lst[i] for i in idx]
