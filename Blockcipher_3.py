import os
import binascii
from Crypto.Cipher import AES

absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)

temp_path = os.path.join(directory_name, "temp_readings.enc")
secr_path = os.path.join(directory_name, "secret_readings.enc")

key = "cbd0fbea6bde2ce95806a6eb2c75cadc"


def get_file_content(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def xor_hex_str(h1, h2):
    assert len(h1) == len(h2)
    return int(h1, 16) ^ int(h2, 16)


def convert_to_readable(hex_str: str):
    concat = ""
    for i in range(0, len(hex_str), 2):
        concat += chr(int(hex_str[i:i+2], 16))
    return concat


def int_to_bytes(i: int):
    return i.to_bytes((i.bit_length() + 7) // 8, 'big')


def decrypt_aes_cbc(ciphertext: bytes, key_hex: str, iv_iv = None) -> bytes:
    key_b = binascii.unhexlify(key_hex)
    block_size = AES.block_size
    # If no IV has been provided, assume IV == first_block
    if iv_iv:
        iv = iv_iv
        actual_ciphertext = ciphertext
    else:
        iv = ciphertext[:block_size]
        actual_ciphertext = ciphertext[block_size:]
    cipher = AES.new(key_b, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(actual_ciphertext)
    return plaintext


temp_content = get_file_content(temp_path)
secr_content = get_file_content(secr_path)

temp_hex_str = binascii.hexlify(temp_content)
secr_hex_str = binascii.hexlify(secr_content)


decrypted_temperature = decrypt_aes_cbc(temp_content, key)
decrypted_temperature_empty_iv = decrypt_aes_cbc(temp_content, key, b"\x00" * 16)
first_temp_block = decrypted_temperature[:16]
first_temp_block_empty_iv = decrypted_temperature_empty_iv[:16]

xor = xor_hex_str(first_temp_block.hex(), first_temp_block_empty_iv.hex())
iv_iv = int_to_bytes(xor)

key_b = binascii.unhexlify(key)

decrypted_secret = decrypt_aes_cbc(secr_content, key, iv_iv)
decrypted_secret = decrypted_secret.decode()[:40]
print(decrypted_secret)
