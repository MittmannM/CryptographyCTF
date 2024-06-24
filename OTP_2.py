import socket
import time
import hashlib
from Crypto.Util.number import long_to_bytes

IP = "10.157.150.7"
PORT = 50006

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

def get_response(message):
    length = sock.send(message)
    res = sock.recv(1024)
    return res

def generate_key(current_time):
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).hexdigest()

def otp(a, b):
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([a[i] ^ b[i]])
    return ciphertext.hex()

def attack_sha256_timestamp(target_hash: bytes):
    current_time = int(time.time())
    i = 0
    possible_messages = []
    while i < 3:
        computed_hash = generate_key(current_time)
        target = int(target_hash.decode(), 16)
        comp_hash = int(computed_hash, 16)
        decrypted_msg = hex(comp_hash ^ target)
        possible_messages.append(decrypted_msg)
        current_time -= 1
        i += 1
    return(possible_messages)

def chr_msg(msg:str):
    a = ""
    for i in range(2, len(msg), 2):
        a += chr(int(msg[i:i+2], 16))
    return a

def main():
    msg_1 = "1"
    res_1 = get_response(msg_1.encode())

    msg_int = 1
    msg_2 = msg_int.to_bytes(length=2, byteorder="big", signed=False)
    res_2 = get_response(msg_2)

    target_hash = res_2[16:-1]
    possible_messages = attack_sha256_timestamp(target_hash)
    possible_messages = [chr_msg(msg) for msg in possible_messages]
    
    for msg in possible_messages:
        print(msg)

main()


