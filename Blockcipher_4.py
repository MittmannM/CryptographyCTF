import socket

IP = "10.157.150.7"
PORT = 50001


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))


def send_message(message):
    sock.send(message.encode())


def receive_message():
    res = sock.recv(1024)
    return res


print(receive_message())
BLOCK_SIZE_HEX = 32
BLOCK_SIZE_CHARS = 16
cleartext = ""

for i in range(1, (BLOCK_SIZE_CHARS * 2) + 1):
    message = "a" * (BLOCK_SIZE_CHARS * 2 - i)
    send_message(message.encode().hex())
    reference_block = receive_message().decode()[32:64]
    print(i)
    for l in range(256):
        char = chr(l)
        msg = message + cleartext + char
        assert len(msg) == 32
        print(f"Sending message {msg}")
        send_message(msg.encode().hex())
        answer = receive_message().decode()[32:64]
        if reference_block == answer:
            print("Correct!")
            cleartext += char
            print(cleartext)
            break

print("Flag: " + cleartext)
