
def write_to_file(filename, data1, data2=None):
    with open(filename, 'a') as f:
        if data2 is not None:
            f.write(str(data1) + " " + str(data2) + '\n')
        else:
            f.write(str(data1) + '\n')

def check_voter(filename: str, voter: str) -> bool:
    names = []
    with open(filename, 'r') as file:
        for line in file:
            str_split = line.split(" ")
            name = str_split[0]
            names.append(name)
        if voter in names:
            return False
        else:
            return True


def check_voter_reg_num(reg_num: int) -> bool:
    with open("reg_numbers.txt", 'r') as file:
        return str(reg_num) in [line.strip() for line in file.readlines()]


def remove_number_from_file(file_path, reg_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            if str(reg_num) != line.strip():
                file.write(line)
            else:
                print('CEC removed your registration number.')


def write_id_to_file(file_path, new_id):
    with open(file_path, 'a') as file:
        file.write(f'{new_id}\n')


def add_vote_to_result(voter_id, candidate):
    with open("result.txt", 'a') as results:
        results.write(f'{(int(candidate), voter_id)}\n')


def parse_line(line):
    parts = line.strip('()\n').split(', ')
    numbers = [int(part) for part in parts]
    return numbers


def count_votes(filename, candidates):
    vote_counts = {int(candidate): 0 for candidate in candidates}
    with open(filename, 'r') as file:
        for line in file:
            candidate, vote = parse_line(line)
            if candidate in vote_counts:
                vote_counts[candidate] += 1

    vote_counts_tuple = tuple(vote_counts.items())
    return vote_counts_tuple

def choose_candidate(candidates):
    while True:
        candidate = int(input('Choose your candidate (enter their number): '))
        if candidate > len(candidates) or candidate < 1:
            print("Such candidate does not exist.")
            continue
        else:
            return int(candidate)
