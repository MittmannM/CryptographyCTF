import socket

IP = "10.157.150.7"
PORT = 50002

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))


def send(msg):
    sock.send(msg)


def rec():
    return sock.recv(1024)


def parse_response(response: bytes, chop_index: int):
    return response.decode()[chop_index:].split("\n")[0]


def convert_to_readable(hex_str: str):
    concat = ""
    for i in range(0, len(hex_str), 2):
        concat += chr(int(hex_str[i:i+2], 16))
    return concat


rec()
res = rec()
ID = parse_response(res, 5)
BLOCK_SIZE = 32
encrypted_flag = ""

for i in range(3):
    send("2".encode())
    rec()
    send(ID[BLOCK_SIZE*i:BLOCK_SIZE*(i+1)].encode())
    response = rec()
    encrypted_flag += parse_response(response, 10)
    rec()

print(convert_to_readable(encrypted_flag))
