import socket
from time import sleep

IP = "10.157.150.7"
PORT = 50003

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))


def rec():
    return sock.recv(1024)


def send_msg(msg):
    sock.send(msg)


def convert_to_bytes1(msg):
    a = hex(msg)
    a_end = a.encode()
    return a_end


def convert_to_bytes2(msg: int):
    a = f"{msg:x}"
    bts = bytes.fromhex(a)
    return bts


def convert_to_bytes3(msg: int):
    b = msg.to_bytes(byteorder='big', signed=False)
    return b


def convert_to_bytes4(msg: int):
    return msg.to_bytes((msg.bit_length() + 7) // 8, 'big')


def calc(r1, r2):
    e = int(r1.decode()[13:], 16)
    n = int(r2.decode().split(" ")[3], 16)
    signature = 0x10
    message = pow(signature, e, n)
    assert message > 1
    assert signature > 1
    conv = convert_to_bytes1
    m_b = conv(message)
    s_b = conv(signature)
    return m_b, s_b


res_1 = rec()
res_2 = rec()

message_bytes, signature_bytes = calc(res_1, res_2)

rec()
send_msg(message_bytes)
res_3 = rec()

send_msg(signature_bytes)
sleep(0.1)
res_4 = rec()
print(res_4.decode()[8:])


sock.close()
