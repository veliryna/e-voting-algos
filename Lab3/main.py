from utils import *
from bureau import *
from voter import *

candidates = []
print("List of candidates in this elections:")
with open("candidates.txt", 'r') as file:
    for line in file:
        print(line.strip("\n"))
        candidates.append([int(i) for i in line.split() if i.isdigit()][0])

name = input("Enter your name: ")
reg_number = registration_bureau(name)
if reg_number is None:
    exit(0)

chosen_voter_id = random.randint(10 ** 5, 10 ** 6 - 1)

chosen_candidate = choose_candidate(candidates)

voter_msg = (reg_number, chosen_voter_id, chosen_candidate)
print("Voter's message to CEC: ", voter_msg)

voter_security(voter_msg)

print()
print("Results in format (Candidate Number, Vote Count):")
print(count_votes('result.txt', candidates))
