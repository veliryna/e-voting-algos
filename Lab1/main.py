from cvk import Cvk, Vote
from voter import Voter, encrypt_vote

# central election committee
cvk = Cvk(['Candidate A', 'Candidate B'])
# voters creation
voter1 = Voter('Voter1', cvk.public_key)
voter2 = Voter('Voter2', cvk.public_key)
voter3 = Voter('Voter3', cvk.public_key)
voter4 = Voter('Voter4', cvk.public_key)
unregistered_voter = Voter('Unregistered Voter', cvk.public_key)
# registering voters
cvk.register_voter(voter1.public_key)
cvk.register_voter(voter2.public_key)
cvk.register_voter(voter3.public_key)
cvk.register_voter(voter4.public_key)
# voting process
cvk.add_vote(voter1.vote(cvk.candidates[0]), voter1.name)
cvk.add_vote(voter2.vote(cvk.candidates[1]), voter2.name)
cvk.add_vote(voter3.vote(cvk.candidates[1]), voter3.name)

# invalid candidate
cvk.add_vote(voter4.vote("candidate3"), voter4.name)
# have no right to vote / unregistered
cvk.add_vote(unregistered_voter.vote(cvk.candidates[0]), unregistered_voter.name)
# cannot vote several times
cvk.add_vote(voter1.vote(cvk.candidates[0]), voter1.name)
# can someone know who were you voting for
print("Election results: ", [
    cvk.decrypt_vote(vote.encrypted_vote)
    for vote in cvk.votes
])
# voting instead of other voter (voter4)
cvk.add_vote(Vote(
    encrypted_vote=encrypt_vote(candidate_name=cvk.candidates[0],cvk_public_key=cvk.public_key),
    public_key=voter4.public_key,
    signature=243553),
    voter4.name)

# checking your own vote validity
print(cvk.check_my_vote(voter3.public_key, voter3.name))


