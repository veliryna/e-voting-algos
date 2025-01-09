import pickle
from elgamal import *
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from utils import *

def send_to_cec(cipher, key_el, signature, key_dsa):
    decrypted_msg = eval(decrypt(key_el, cipher))
    reg_number, voter_id, candidate = decrypted_msg
    public_key_dsa = load_pem_public_key(key_dsa.encode())
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(chosen_hash)
    hasher.update(pickle.dumps(decrypted_msg))
    digest = hasher.finalize()
    try:
        public_key_dsa.verify(signature, digest, utils.Prehashed(chosen_hash))
    except InvalidSignature:
        print("Your digital signature is invalid.")
    if not check_voter_reg_num(reg_number):
        raise Exception("Registration number is not in the system.")
    else:
        remove_number_from_file('reg_numbers.txt', reg_number)
    print("CEC received your message and counted vote.")
    write_id_to_file('voted_voters.txt', voter_id)
    add_vote_to_result(voter_id, candidate)
