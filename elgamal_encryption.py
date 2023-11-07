import random
from key_database import KeysDatabase

db = KeysDatabase()


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# Generating random numbers
def gen_key(q):
    key = random.randint(2048, q)
    while gcd(q, key) != 1:
        key = random.randint(2048, q)

    return key


# Modular exponentiation
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)

    return x % c


def keys_initializer():
    global db
    q = random.randint(pow(5, 10), pow(10, 10))
    g = random.randint(2, q)
    receiver_key = gen_key(q)
    sender_h = power(g, receiver_key, q)
    sender_key = gen_key(q)
    s = power(sender_h, sender_key, q)
    p = power(g, sender_key, q)
    receiver_h = power(p, receiver_key, q)
    key_id = db.insert_keys(s, receiver_h)
    return key_id


def _get_keys(user_id):
    global db
    return db.get_keys(user_id)


# Asymmetric encryption
def encrypt(msg, user_id):
    encrypt_key, decrypt_key = _get_keys(user_id)
    en_msg = []
    for i in range(0, len(msg)):
        en_msg.append(msg[i])
    for i in range(0, len(en_msg)):
        en_msg[i] = encrypt_key * ord(en_msg[i])
    encrypted_msg_str = ",".join(str(x) for x in en_msg)
    return encrypted_msg_str


def decrypt(en_msg, user_id):
    encrypted_msg_list = en_msg.split(",")
    encrypt_key, decrypt_key = _get_keys(user_id)
    dr_msg = []
    for i in range(0, len(encrypted_msg_list)):
        dr_msg.append(chr(int(float(encrypted_msg_list[i]) / decrypt_key)))
    return ''.join(dr_msg)
