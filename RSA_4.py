import math
import socket
from time import sleep

IP = "10.157.150.7"
PORT = 50004

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))


# TODO: You may need to run this file a couple of times :)

def rec():
    return sock.recv(1024)


def send_msg(msg):
    sock.send(msg)


def int_to_bytes(i):
    return i.to_bytes((i.bit_length() + 7) // 8, 'big')


def convert_to_bytes1(msg):
    a = hex(msg)
    a_end = a.encode()
    return a_end


def parse_e_and_n(r1, r2):
    e = int(r1.decode()[13:], 16)
    n = int(r2.decode().split(" ")[3], 16)
    return e, n


def get_challenge(response: bytes):
    response = response.decode()
    return response.split("0x")[1].split("\n")[0]


def find_gcd_1(N):
    r = 1
    while True:
        r += 1
        if math.gcd(r, N) == 1:
            return r


def compute_new_msg(msg, e, r, N):
    result = (r ** e) % N
    new_msg = msg * result
    return new_msg


def get_sig(response):
    response = response.decode()
    if not response.count("#") > 0:
        print("Response doesn't contain #, aborting")
        exit(1)
    sig = response.split("#")[1]
    if sig.startswith("0x"):
        sig = sig[2:]
    return sig


res_1 = rec()
res_2 = rec()

e, n = parse_e_and_n(res_1, res_2)

r = find_gcd_1(n)

res_3 = rec()

send_msg("1".encode())
res_4 = rec()
send_msg("aa".encode().hex().encode())
res_5 = rec()
res_6 = rec()

send_msg("2".encode())
res_7 = rec()

challenge_hex = get_challenge(res_4)
challenge_int = int(challenge_hex, 16)

msg_to_sign = compute_new_msg(challenge_int, e, r, n)

send_msg(f"{msg_to_sign:x}".encode())
res_8 = rec()
res_9 = rec()

signature_hex = get_sig(res_8)
signature_int = int(signature_hex, 16)
m_pow_d = (signature_int // r) % n
assert m_pow_d > 1
m_pow_d_hex = f"{m_pow_d:x}"


send_msg("1".encode())
res_9 = rec()

send_msg(m_pow_d_hex.encode())

res_10 = rec()
res_11 = rec()
print(res_11.decode())

sock.close()