import string
from collections import Counter
from utils import *

'''
- Виборча комісія (ВК) формує список виборців та кандидатів.
- Кожен виборець створює 10 наборів повідомлень, кожен набір містить
правильно оформлений бюлетень для кожного можливого результату (Candidate A, Candidate B). 
Крім цього, кожне повідомлення і бюлетень містить випадковий ID виборця, який
повинен бути достатньо великим, щоб уникнути збігів з іншими
виборцями.
'''
candidates = [
    {'id': 0, 'name': 'Candidate A', 'votes': 0},
    {'id': 1, 'name': 'Candidate B', 'votes': 0}
]
def generate_voter_id():
    return ''.join(random.choice(string.digits) for _ in range(15))
def one_voter_message_sets(voter_id):
    message_sets = []
    for _ in range(10):
        message_sets.append([{"voter_id": voter_id, "candidate": candidate["id"]}
                             for candidate in candidates])
    return message_sets

voters = []
n, e, d = generate_rsa_keys()
cvk_public_key = (n, e)
cvk_private_key = (n, d)

for i in range(4):
    r = find_r(n)
    voter_id = generate_voter_id()
    voter = {
        "name": f'Voter {i+1}',
        "id": voter_id,
        "message_sets": one_voter_message_sets(voter_id),
        "r": r
    }
    voters.append(voter)

'''
Кожен виборець маскує (шифрує) всі свої повідомлення (з усього
свого пакету) та надсилає їх до ВК разом з множником маскування
(ключем), щоби ВК могла розкрити їх частину на свій вибір.
'''
cvk_data = []
for voter in voters:
    encrypted_ballots = []
    for ballot in voter['message_sets']:
        for i in ballot:
            string_ballot = ', '.join([f"{key}: {value}" for key, value in i.items()])
            encrypted_ballot = encrypt(string_ballot, cvk_public_key, voter['r'])
            encrypted_ballots.append({
                "id": voter['id'],
                "encrypted_ballot": encrypted_ballot,
                "r": voter['r']
            })
    cvk_data.append(encrypted_ballots)

all_sent_bulletins = []
for voter in cvk_data:
    for ballot in voter:
        all_sent_bulletins.append(ballot['id'])

'''ВК перевіряє за ID чи виборець раніше не надсилав їй бюлетені для
підпису.'''

id_counts = Counter(all_sent_bulletins)
for voter_id, count in id_counts.items():
    if count > 20:
        print(f"Voter {voter_id} cannot vote more than once.")
        all_sent_bulletins = [id for id in all_sent_bulletins if id != voter_id]
'''
ВК відкриває 9 з 10 наборів, на свій вибір, та перевіряє чи всі
вони правильно сформовані.Після цього ВК індивідуально підписує
кожне повідомлення (в нашому випадку їх 2) з одного набору, що вона
не розкривала (з 10-го, наприклад) та надсилає їх назад виборцю
підписаними її е-підписом.
'''
def decrypt_9_ballots_for_every_voter(voter_data, private_key):
    decrypted_ballots = []
    ballots_for_cvk = []
    for voter in voter_data:
        for i, data in enumerate(voter):
            if i != 19 and i != 18:
                decrypted_ballot = decrypt(data['encrypted_ballot'], private_key, data['r'])
                decrypted_ballots.append(decrypted_ballot)
            else:
                ballots_for_cvk.append(data)
    return decrypted_ballots, ballots_for_cvk

decrypted_ballots, ballots_for_cvk = decrypt_9_ballots_for_every_voter(cvk_data, cvk_private_key)
signed_ballots_by_cvk = []
for voter in ballots_for_cvk:
    signed_ballots_by_cvk.append(cvk_signature(voter['encrypted_ballot'], cvk_private_key))


'''Виборець знімає своє маскування з повідомлень та отримує один набір
бюлетенів, підписаний ВК. Оскільки вони не були зашифровані ВК, а
лише підписані, то виборець одразу розуміє який з них «1», а який «2».'''

ballots_unmasked = []
for i, voter in enumerate(ballots_for_cvk):
    ballots_unmasked.append(remove_mask(signed_ballots_by_cvk[i], voter['r'], cvk_public_key))

chosen_for_final = []
for i in range(0, len(ballots_unmasked), 2):
    chosen_for_final.append([ballots_unmasked[i], ballots_unmasked[i+1]])
'''
Кожен виборець обирає лише один з отриманих бюлетенів та шифрує
його відкритим ключем ВК. Виборець відправляє свій один обраний ним бюлетень до ВК.
'''
final_ballots = []
for i, voter in enumerate(chosen_for_final):
    if i == 2:
        final_ballots.append(encrypt(voter[1], cvk_public_key, voters[i]['r']))
    else:
        final_ballots.append(encrypt(voter[0], cvk_public_key, voters[i]['r']))

result_ballots = []
for i, ballot in enumerate(final_ballots):
    result_ballots.append(decrypt(ballot, cvk_private_key, cvk_data[i][i]['r']))

'''ВК розшифровує бюлетені своїм приватним ключем, перевіряє
підписи, перевіряє унікальність ідентифікаційного номера, зберігає
послідовний (за порядком надходження) номер та підбиває підсумки.
ВК публікує результати голосування разом з кожним ID виборця і
відповідним бюлетенем.'''

res = formatting(result_ballots)
voters_id = set()
for vote in res:
    if vote["voter_id"] in all_sent_bulletins:
        if vote['voter_id'] in voters_id:
            raise Exception("Duplicate voter IDs. Someone tried to sabotage the election.")
        voters_id.add(vote["voter_id"])
        print(vote)
        for candidate in candidates:
            if int(vote['candidate']) == candidate['id']:
                candidate['votes'] += 1
    else:
        print("You are not eligible to vote in this elections.")
print(candidates)
