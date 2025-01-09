from rsa import generate_rsa_key_pair
from utils import string_to_binary_array, public_key_to_binary_array, quadratic_hash
from cvk import Vote


def encrypt_vote(candidate_name, cvk_public_key):
    message = string_to_binary_array(candidate_name)
    cvk_public_key_bits = public_key_to_binary_array(cvk_public_key)
    encrypted_vote = [bit ^ cvk_public_key_bits[index % len(cvk_public_key_bits)] for index, bit in enumerate(message)]
    return encrypted_vote


def create_signature(encrypted_vote, private_key):
    modulus = private_key['n']
    exponent = private_key['d']
    vote_hash = quadratic_hash(encrypted_vote, modulus)
    signature = pow(vote_hash, exponent, modulus)
    return signature


class Voter:
    def __init__(self, name, cvk_public_key):
        self.name = name
        self.cvk_public_key = cvk_public_key
        key_pair = generate_rsa_key_pair()
        self.public_key = key_pair['publicKey']
        self.private_key = key_pair['privateKey']

    def vote(self, candidate_name):
        encrypted_vote = encrypt_vote(candidate_name, self.cvk_public_key)
        signature = create_signature(encrypted_vote, self.private_key)
        return Vote(encrypted_vote=encrypted_vote, signature=signature, public_key=self.public_key)

    def get_public_key(self):
        return self.public_key
