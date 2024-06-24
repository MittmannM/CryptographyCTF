import socket

IP = "10.157.150.7"
PORT = 50007


def send_message(message):
    sock.send(message.encode())


def receive_message():
    res = sock.recv(1024)
    return res


packet_from_server = "2ccedc2e51bc179708dd661c760932ec96afeba7cfbd708338d9abde0836ea79fa22c3b4e7c65fcc265612fa11711e79d79f416ffeeab83c8254"
codes = "2ccedc2e51bc179708dd661c760932ec96afeba7cfbd708338d9abde0836ea79fa22c3b4e7c65fcc26"


flag = ""
for k in range(0, len(codes), 2):
    for i in range(256):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        receive_message()
        receive_message()
        send_message("2")
        receive_message()
        msg_for_server = flag + chr(i)
        print("Sending to server: " + msg_for_server)
        send_message(msg_for_server.encode().hex())
        encrypted_by_server = receive_message().decode()
        print("Got back from server: " + encrypted_by_server)
        encrypted_flag = codes[:k+2]
        print("Should be: " + encrypted_flag)
        if encrypted_by_server == encrypted_flag:
            print("Match: " + chr(i))
            flag += chr(i)
            sock.close()
            break
        sock.close()
print("FLAG: " + flag)
