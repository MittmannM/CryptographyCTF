import os
from collections import defaultdict

absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
filepath = os.path.join(directory_name, "letter.txt")

file = open(filepath, "r")
content = file.read()

print(content)

file.close()

letter_counts = defaultdict(int)

# count different letters in ciphertext
for letters in content:

    if letters.isalpha():
        letter_counts[letters] += 1

sorted_letter_counts = sorted(letter_counts.items(), key=lambda item: item[1], reverse=True)

print(sorted_letter_counts)

translated_text = ""

# dictionary according to given graph for translation
translated_dict = {"k": "e", "r": "t", "l": "a", "t": "h", "z": "o", "g": "n", "o": "i", "e": "s", "u": "r", "x": "d",
                   "w": "l", "i": "m", "n": "u", "m": "w", "q": "f", "j": "g", "h": "y", "f": "c", "c": "b", "d": "p",
                   "s": "v", "y": "k", "p": "x", "v": "j", "a": "q", "b": "z"}

# add letter to output text if ciphertext letter matches with dictionary
for letters in content:
    inserted = False
    for keys, values in translated_dict.items():
        if letters.lower() == keys:
            translated_text += values
            inserted = True
            break
    if not inserted:
        translated_text += letters

print(translated_text)
