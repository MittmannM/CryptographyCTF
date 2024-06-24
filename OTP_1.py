import os

absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
filepath = os.path.join(directory_name, "flag.enc")

with open(filepath) as flag:
    flag = flag.readline()

pairs_list = [int(flag[i:i+2], 16) for i in range(0, len(flag), 2)]

iterations = max(pairs_list) + 1
for i in range(128):
    i_hex = int(hex(i), 16)
    flag_phrase = ""
    for elem in pairs_list:
        xor = i_hex ^ elem
        flag_phrase += f"{chr(xor)}"
    # This line was added afterwards of course, for ease of reading :)
    if flag_phrase.startswith("OTp_KeyS"):
        print(flag_phrase)