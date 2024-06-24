import socket
import copy

IP = "10.157.150.7"
PORT = 50005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))


def send(msg):
    sock.send(msg)


def rec():
    return sock.recv(1024)


# first rec is only smalltalk
rec()
iv_and_c = rec()
# print(iv_and_c)
split = iv_and_c.decode().split("\n")
iv = split[0].split(" ")[-1]
cipher = split[1].split(" ")[-1]
# print(iv, cipher)

# Blocksize in HEX STR LEN! 2 hex digits == 1 byte
BLOCK_SIZE_HEX = len(iv)
BLOCK_SIZE_BYTES = len(iv)//2
BLOCK_NUM = len(cipher)//BLOCK_SIZE_HEX
PADDING_INCORRECT = b'Incorrect padding!'
PADDING_CORRECT = b'Thanks for your message.'
PADDING_BYTE = ...


def bytify_hex_message(ciphertext):
    blcok_number = len(ciphertext)//BLOCK_SIZE_HEX
    c_blocks = [ciphertext[i * BLOCK_SIZE_HEX:(i + 1) * BLOCK_SIZE_HEX] for i in range(blcok_number)]
    blocks_and_bytes = [[] for _ in range(blcok_number)]
    for block_index in range(len(c_blocks)):
        block = c_blocks[block_index]
        for i in range(0, BLOCK_SIZE_HEX, 2):
            block_byte_hex_str = block[i:i+2]
            block_byte_int = int(block_byte_hex_str, 16)
            blocks_and_bytes[block_index].append(block_byte_int)
    return blocks_and_bytes


def hexify_byte_array(byte_arr):
    hex_str = ""
    for block_index in range(len(byte_arr)):
        block_bytes = byte_arr[block_index]
        for byte_int in block_bytes:
            hex_str_tmp = hex(byte_int)
            if len(hex_str_tmp) == 3:
                hex_str_tmp = f"0x0{hex_str_tmp[-1]}"
            hex_str += hex_str_tmp
    hex_str = hex_str.replace("0x", "")
    return hex_str


def find_padding_index(arr):
    for i in range(BLOCK_SIZE_BYTES):
        hex_m = hexify_byte_array(arr)
        send(hex_m.encode())
        _res = rec()
        # print(f"i = {i}, res = {_res}")
        if _res == PADDING_INCORRECT:
            return i
    return -1


def xor_int_list(l1, l2):
    list_length = len(l1)
    assert list_length == len(l2)
    l3 = []
    for i in range(list_length):
        l3.append(l1[i] ^ l2[i])
    return l3



print("Padding Orcale Attack running... (may take a minute or 1000...)")

c = bytify_hex_message(cipher)

cleartext_bytes = [[] for _ in range(BLOCK_NUM)]
max_hex_size = 16**2

iv_bytes = bytify_hex_message(iv)[0]
c.insert(0, iv_bytes)

for blocks_bruteforced in range(BLOCK_NUM):
    c_prime = copy.deepcopy(c)
    d_n = [0x00] * BLOCK_SIZE_BYTES
    padding_ctr = 1
    for byte_index in range(BLOCK_SIZE_BYTES-1, -1, -1):
        c_prime_byte = c_prime[-2][byte_index]
        for evil_byte in range(max_hex_size):
            # if we hit c_prime_byte, we would basically just send c which automatically leads to correct padding,
            # as there was no manipulation of the original message
            if evil_byte == c_prime_byte:
                continue
            c_prime[-2][byte_index] = evil_byte
            hexified_message = hexify_byte_array(c_prime)
            send(hexified_message.encode())
            res = rec()

            if res == PADDING_CORRECT:
                d_n[byte_index] = evil_byte ^ padding_ctr
                bl = c[-2]
                cleartext_b = d_n[byte_index] ^ c[-2][byte_index]
                cleartext_bytes[-1-blocks_bruteforced].insert(0, cleartext_b)
                # increase padding and set all evil_vec bytes left from index to new padding
                padding_ctr += 1
                # traverse vector from the right side and update c_n-1_prime to result in new padding when xored
                for index in range(BLOCK_SIZE_BYTES-1, BLOCK_SIZE_BYTES-padding_ctr-1, -1):
                    c_prime[-2][index] = d_n[index] ^ padding_ctr
                print(f"Found correct padding for block {BLOCK_NUM - blocks_bruteforced} at byte_index {byte_index}")
                # print(f"Cleartext bytes: {cleartext_bytes}")
                break

    c = c[:-1]

# print(cleartext_bytes)

converted = ""
for block in cleartext_bytes:
    for i in range(0, len(block), 2):
        chars = chr(block[i]) + chr(block[i+1])
        converted += chars

print(converted)
