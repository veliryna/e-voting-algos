from elgamal import *
import pickle
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import dsa, utils
from cvk import *
def voter_security(message):
    # ElGamal
    keys = generate_keys()
    encrypted_msg = encrypt(keys['publicKey'], str(message))
    public_key_el = keys['privateKey']

    # DSA signature
    private_key_dsa = dsa.generate_private_key(key_size=2048)
    public_key_dsa = private_key_dsa.public_key()
    pk_dsa_to_send = public_key_dsa.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode()
    my_hash = hashes.SHA256()
    hasher = hashes.Hash(my_hash)
    hasher.update(pickle.dumps(message))
    signature = private_key_dsa.sign(hasher.finalize(), utils.Prehashed(my_hash))

    send_to_cec(encrypted_msg, public_key_el, signature, pk_dsa_to_send)
