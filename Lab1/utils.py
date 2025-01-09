def string_to_binary_array(string):
    binary_array = []
    for char in string:
        char_code = ord(char)
        binary_string = format(char_code, '08b')
        binary_array.extend(map(int, binary_string))
    return binary_array


def binary_array_to_string(binary_array):
    result = ""
    for i in range(0, len(binary_array), 8):
        byte = "".join(map(str, binary_array[i:i+8]))
        char_code = int(byte, 2)
        result += chr(char_code)
    return result


def public_key_to_binary_array(public_key):
    public_key_bits = int_to_binary_array(public_key['e']) + int_to_binary_array(public_key['n'])
    return public_key_bits


def private_key_to_binary_array(private_key):
    private_key_bits = int_to_binary_array(private_key['d']) + int_to_binary_array(private_key['n'])
    return private_key_bits


def int_to_binary_array(num):
    binary_string = bin(num)[2:]
    return list(map(int, binary_string))


def quadratic_hash(input_list, n):
    hash_val = 0
    H = 0
    for M in input_list:
        H = (H + M) % n
        hash_val = (hash_val + H * H) % n
    return hash_val
