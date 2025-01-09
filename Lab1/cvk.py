from rsa import generate_rsa_key_pair
from utils import binary_array_to_string, public_key_to_binary_array, quadratic_hash

class Vote:
    def __init__(self, encrypted_vote, signature, public_key):
        self.encrypted_vote = encrypted_vote
        self.signature = signature
        self.public_key = public_key

class Cvk:
    def __init__(self, candidates):
        key_pair = generate_rsa_key_pair()
        self.public_key = key_pair['publicKey']
        self.private_key = key_pair['privateKey']
        self.candidates = candidates
        self.voter_public_keys = []
        self.votes = []

    def add_vote(self, vote, name):
        verify_signature = self.verify_signature(
            vote.encrypted_vote,
            vote.signature,
            vote.public_key
        )
        if not verify_signature:
            print('Invalid signature')
            return

        if vote.public_key not in self.voter_public_keys:
            print(f'{name} cannot vote in this elections.')
            return

        if any(v.public_key == vote.public_key for v in self.votes):
            print(f'{name} has already voted.')
            return

        decrypted_vote = self.decrypt_vote(vote.encrypted_vote)
        if decrypted_vote not in self.candidates:
            print('This candidate does not exist in this elections.')
            return

        self.votes.append(vote)
        return vote

    def register_voter(self, voter_public_key):
        self.voter_public_keys.append(voter_public_key)

    def check_my_vote(self, voter_public_key, name):
        vote = next((v for v in self.votes if v.public_key == voter_public_key), None)
        if vote is None:
            return f'{name}: your vote was not counted'
        return f'{name}: your vote is valid and counted in elections'

    def verify_signature(self, encrypted_vote, signature, public_voter_key):
        decrypted_signature = pow(signature, public_voter_key['e'], public_voter_key['n'])
        hash_value = quadratic_hash(encrypted_vote, public_voter_key['n'])
        return hash_value == decrypted_signature

    def decrypt_vote(self, encrypted_vote):
        cvk_public_key_bits = public_key_to_binary_array(self.public_key)
        decrypted_vote = [bit ^ cvk_public_key_bits[index % len(cvk_public_key_bits)] for index, bit in enumerate(encrypted_vote)]
        candidate_name = binary_array_to_string(decrypted_vote)
        return candidate_name
