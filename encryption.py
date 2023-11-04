import random
from math import pow

# Global variables to store keys
p = None
g = None
key = None


def generate_elgamal_keys():
    global p, g
    p = random.randint(2, 10)
    g = pow(2, p)


def generate_random_key(q):
    return random.randint(q, int(pow(10, 20)))


def modular_exponentiation(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 0:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2
    return result


def initialize_keys():
    global p, g, key
    try:
        # Try to load keys from the file
        keys = load_keys_from_file("elgamal_keys.txt")
        p, g, key = keys[:2], keys[2], keys[3]
    except FileNotFoundError:
        # If the file doesn't exist, generate new keys
        generate_elgamal_keys()
        key = generate_random_key(p)
        keys = [str(p), str(g), str(key)]
        save_keys_to_file(keys, "elgamal_keys.txt")


def encrypt_message(msg):
    if p is None or g is None or key is None:
        initialize_keys()

    ciphertext = []
    random_key = generate_random_key(p)
    s = modular_exponentiation(g, random_key, p)
    r = modular_exponentiation(g, random_key, p)

    for character in msg:
        ciphertext.append(s * ord(character) + r)

    return ciphertext


def decrypt_message(ciphertext):
    if p is None or g is None or key is None:
        initialize_keys()

    plaintext = []

    for i in range(len(ciphertext)):
        plaintext.append(chr((ciphertext[i] - key) // p))

    return plaintext


def save_keys_to_file(keys, key_file):
    with open(key_file, 'w') as f:
        for key in keys:
            f.write(str(key) + '\n')


def load_keys_from_file(key_file):
    keys = []
    with open(key_file, 'r') as f:
        for line in f:
            keys.append(int(line.strip()))
    return keys






# from Crypto.PublicKey import ElGamal
# from Crypto.Cipher import PKCS1_OAEP
# from Crypto import Random
#
#
# def generate_keys():
#     key = ElGamal.generate(1024, Random.new().read)
#     public_key = key.publickey()
#     private_key = key
#     return public_key, private_key
#
#
# def save_keys(public_key, private_key, key_file):
#     with open(key_file, 'w') as f:
#         f.write(f'{public_key.y}\n')
#         f.write(f'{public_key.g}\n')
#         f.write(f'{public_key.p}\n')
#         f.write(f'{private_key.x}\n')
#         f.write(f'{private_key.q}\n')
#
#
# def load_keys(key_file):
#     public_key_data = []
#     private_key_data = []
#
#     with open(key_file, 'r') as f:
#         lines = f.readlines()
#
#     if len(lines) != 6:
#         raise ValueError("Invalid key file format")
#
#     for line in lines[:3]:
#         try:
#             public_key_data.append(int(line.strip()))
#         except ValueError:
#             raise ValueError("Invalid key file format")
#
#     for line in lines[3:]:
#         try:
#             private_key_data.append(int(line.strip()))
#         except ValueError:
#             raise ValueError("Invalid key file format")
#
#     public_key = ElGamal.construct((public_key_data[1], public_key_data[0]))
#     private_key = ElGamal.construct((private_key_data[1], private_key_data[0]))
#
#     return public_key, private_key
#
#
# def encrypt(public_key, plaintext):
#     cipher = PKCS1_OAEP.new(public_key)
#     ciphertext = cipher.encrypt(plaintext)
#     return ciphertext
#
#
# def decrypt(private_key, ciphertext):
#     cipher = PKCS1_OAEP.new(private_key)
#     plaintext = cipher.decrypt(ciphertext)
#     return plaintext
