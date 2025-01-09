import random
from utils import *

voters = ['A', 'B', 'C', 'D']
candidates = [0, 1]  # Candidates A and B

'''
Кожен виборець формує свій Е-бюлетень, після чого робить наступне:
Додає до свого Е-бюлетеня довільний рядок, зберігає рядок.
'''
ballot_a = 0
random_strings_a = [generate_random_string() for _ in range(5)]
message_a = add_random_string(ballot_a, random_strings_a[0])
private_key_a, public_key_a = generate_key_pair()

ballot_b = 0
random_strings_b = [generate_random_string() for _ in range(5)]
message_b = add_random_string(ballot_b, random_strings_b[0])
private_key_b, public_key_b = generate_key_pair()

ballot_c = 1
random_strings_c = [generate_random_string() for _ in range(5)]
message_c = add_random_string(ballot_c, random_strings_c[0])
private_key_c, public_key_c = generate_key_pair()

ballot_d = 0
random_strings_d = [generate_random_string() for _ in range(5)]
message_d = add_random_string(ballot_d, random_strings_d[0])
private_key_d, public_key_d = generate_key_pair()

public_keys = [public_key_d, public_key_c, public_key_b, public_key_a]

'''
o Шифрує результати попереднього етапу відкритим ключем D.
o Шифрує результати попереднього етапу відкритим ключем C.
o Шифрує результати попереднього етапу відкритим ключем B.
o Шифрує результати попереднього етапу відкритим ключем A.
o Додає новий випадковий рядок до результату попереднього
етапу та шифрує отримане відкритим ключем D. 
o Додає новий випадковий рядок до результату попереднього
етапу та шифрує отримане відкритим ключем C. 
o Додає новий випадковий рядок до результату попереднього
етапу та шифрує отримане відкритим ключем B. 
o Додає новий випадковий рядок до результату попереднього
етапу та шифрує отримане відкритим ключем A.
'''
encrypted_messages_for_check_a = []
encrypted_message_a = message_a
for key in public_keys:
    encrypted_message_a = encrypt(encrypted_message_a, key)
    encrypted_messages_for_check_a.append(encrypted_message_a)
encrypted_message_with_string_a = encrypted_message_a
for i in range(4):
    encrypted_message_with_string_a = encrypt(add_random_string(encrypted_message_with_string_a, random_strings_a[i+1]), public_keys[i])

encrypted_messages_for_check_b = []
encrypted_message_b = message_b
for key in public_keys:
    encrypted_message_b = encrypt(encrypted_message_b, key)
    encrypted_messages_for_check_b.append(encrypted_message_b)
encrypted_message_with_string_b = encrypted_message_b
for i in range(4):
    encrypted_message_with_string_b = encrypt(add_random_string(encrypted_message_with_string_b, random_strings_b[i+1]), public_keys[i])

encrypted_messages_for_check_c = []
encrypted_message_c = message_c
for key in public_keys:
    encrypted_message_c = encrypt(encrypted_message_c, key)
    encrypted_messages_for_check_c.append(encrypted_message_c)
encrypted_message_with_string_c = encrypted_message_c
for i in range(4):
    encrypted_message_with_string_c = encrypt(add_random_string(encrypted_message_with_string_c, random_strings_c[i+1]), public_keys[i])

encrypted_messages_for_check_d = []
encrypted_message_d = message_d
for key in public_keys:
    encrypted_message_d = encrypt(encrypted_message_d, key)
    encrypted_messages_for_check_d.append(encrypted_message_d)
encrypted_message_with_string_d = encrypted_message_d
for i in range(4):
    encrypted_message_with_string_d = encrypt(add_random_string(encrypted_message_with_string_d, random_strings_d[i+1]), public_keys[i])

encrypted_messages_with_strings = [encrypted_message_with_string_a, encrypted_message_with_string_b, encrypted_message_with_string_c, encrypted_message_with_string_d]

'''
Кожен виборець надсилає отримане повідомлення до А.
- А розшифровує всі бюлетені за допомогою свого закритого ключа та
видаляє випадкові рядки на даному рівні.
- А перемішує зашифровані бюлетені та надсилає їх B.
'''
decrypted_messages_without_string_a = []
for i in range(4):
    decrypted_messages_without_string_a.append(remove_string(decrypt(encrypted_messages_with_strings[i], private_key_a), 8))
random.shuffle(decrypted_messages_without_string_a)

'''
B розшифровує всі бюлетені своїм закритим ключем та перевіряє чи є
серед них його бюлетень. Після чого він видаляє всі випадкові рядки
на даному рівні, перемішує ці, все ще зашифровані, бюлетені та
надсилає результат C.
C розшифровує всі бюлетені своїм закритим ключем та перевіряє чи є
серед них його бюлетень. Після чого він видаляє всі випадкові рядки
на даному рівні, перемішує ці, все ще зашифровані, бюлетені та
надсилає результат D.
D розшифровує всі бюлетені своїм закритим ключем та перевіряє чи є
серед них його бюлетень. Після чого він видаляє всі випадкові рядки
на даному рівні, перемішує ці, все ще зашифровані, бюлетені та
надсилає результат А.
'''
decrypted_messages_without_string_b = []
voters_random_strings_b = []
for encoded_message in decrypted_messages_without_string_a:
    decrypted_message = decrypt(encoded_message, private_key_b)
    voters_random_strings_b.append(extract_last_8_bytes(decrypted_message))
    decrypted_messages_without_string_b.append(remove_string(decrypted_message, 8))
check_own_random_string(random_strings_b[3], voters_random_strings_b)
random.shuffle(decrypted_messages_without_string_b)

decrypted_messages_without_string_c = []
voters_random_strings_c = []
for encoded_message in decrypted_messages_without_string_b:
    decrypted_message = decrypt(encoded_message, private_key_c)
    voters_random_strings_c.append(extract_last_8_bytes(decrypted_message))
    decrypted_messages_without_string_c.append(remove_string(decrypted_message, 8))
check_own_random_string(random_strings_c[2], voters_random_strings_c)
random.shuffle(decrypted_messages_without_string_c)

decrypted_messages_without_string_d = []
voters_random_strings_d = []
for encoded_message in decrypted_messages_without_string_c:
    decrypted_message = decrypt(encoded_message, private_key_d)
    voters_random_strings_d.append(extract_last_8_bytes(decrypted_message))
    decrypted_messages_without_string_d.append(remove_string(decrypted_message, 8))
check_own_random_string(random_strings_d[1], voters_random_strings_d)
random.shuffle(decrypted_messages_without_string_d)

'''
ElGamal keys for every voter
'''
private_key_elgamal_a, public_key_elgamal_a = generate_keys_elgamal()
private_key_elgamal_b, public_key_elgamal_b = generate_keys_elgamal()
private_key_elgamal_c, public_key_elgamal_c = generate_keys_elgamal()
private_key_elgamal_d, public_key_elgamal_d = generate_keys_elgamal()
'''
А розшифровує всі бюлетені своїм закритим ключем та перевіряє чи є
серед них його бюлетень. Після чого він підписує результат,
перемішує бюлетені та надсилає результат B, С та D. 
'''
idx = [0, 1, 2, 3]
random.shuffle(idx)

decrypted_messages_a = []
for message in decrypted_messages_without_string_d:
    decrypted_messages_a.append(decrypt(message, private_key_a))
check_own_ballots(encrypted_messages_for_check_a, decrypted_messages_a)

signed_messages_a = []
for message in decrypted_messages_a:
    signature = sign_message(private_key_elgamal_a, message)
    signed_messages_a.append(signature)
shuffle_ballots(signed_messages_a, idx)

'''
B перевіряє та видаляє ЕЦП А, потім розшифровує всі бюлетені своїм
закритим ключем та перевіряє чи є серед них його бюлетень. Після
чого він підписує результат, перемішує бюлетені та надсилає результат
A, C та D.
'''
random.shuffle(idx)
check_amount_of_messages(voters, signed_messages_a)
for i in range(4):
    hashed_message = hash_message(decrypted_messages_a[i])
    verify_signature(public_key_elgamal_a, signed_messages_a[i], hashed_message)

decrypted_messages_b = []
for message in decrypted_messages_a:
    decrypted_messages_b.append(decrypt(message, private_key_b))
check_own_ballots(encrypted_messages_for_check_b, decrypted_messages_b)

signed_messages_b = []
for message in decrypted_messages_b:
    signature = sign_message(private_key_elgamal_b, message)
    signed_messages_b.append(signature)
shuffle_ballots(signed_messages_b, idx)

'''
C перевіряє та видаляє ЕЦП B, потім розшифровує всі бюлетені своїм
закритим ключем та перевіряє чи є серед них його бюлетень. Після
чого він підписує результат, перемішує бюлетені та надсилає результат
A, В та D.
'''
random.shuffle(idx)
check_amount_of_messages(voters, signed_messages_b)
for i in range(4):
    hashed_message = hash_message(decrypted_messages_b[i])
    verify_signature(public_key_elgamal_b, signed_messages_b[i], hashed_message)

decrypted_messages_c = []
for message in decrypted_messages_b:
    decrypted_messages_c.append(decrypt(message, private_key_c))
check_own_ballots(encrypted_messages_for_check_c, decrypted_messages_c)

signed_messages_c = []
for message in decrypted_messages_c:
    signature = sign_message(private_key_elgamal_c, message)
    signed_messages_c.append(signature)
shuffle_ballots(signed_messages_c, idx)

'''
D перевіряє та видаляє ЕЦП C, потім розшифровує всі бюлетені своїм
закритим ключем та перевіряє чи є серед них його бюлетень. Після
чого він підписує результат, перемішує бюлетені та надсилає результат
A, B та С. 
'''
random.shuffle(idx)
check_amount_of_messages(voters, signed_messages_c)

for i in range(4):
    hashed_message = hash_message(decrypted_messages_c[i])
    verify_signature(public_key_elgamal_c, signed_messages_c[i], hashed_message)

decrypted_messages_d = []
for message in decrypted_messages_c:
    decrypted_messages_d.append(decrypt(message, private_key_d))
check_own_ballots(encrypted_messages_for_check_d, decrypted_messages_d)

signed_messages_d = []
for message in decrypted_messages_d:
    signature = sign_message(private_key_elgamal_d, message)
    signed_messages_d.append(signature)
shuffle_ballots(signed_messages_d, idx)

'''
A, B та С перевіряють та видаляють ЕЦП D. Всі впевнюються, що їх
бюлетені все ще присутні у цьому наборі.
'''
check_own_ballots(decrypted_messages_d, encrypted_messages_for_check_a)
check_own_ballots(decrypted_messages_d, encrypted_messages_for_check_b)
check_own_ballots(decrypted_messages_d, encrypted_messages_for_check_c)
for i in range(4):
    hashed_message = hash_message(decrypted_messages_d[i])
    verify_signature(public_key_elgamal_d, signed_messages_d[i], hashed_message)

final_result = []
for message in decrypted_messages_d:
    vote = remove_string(message, 8)
    if vote == b'0':
        final_result.append("Candidate A")
    elif vote == b'1':
        final_result.append("Candidate B")
final_result = sorted(final_result)
print()
print("Election results:")
print(final_result)
