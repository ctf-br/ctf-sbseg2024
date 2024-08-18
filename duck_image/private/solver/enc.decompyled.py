# decompyle3 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.12.5 (main, Aug  9 2024, 08:20:41) [GCC 14.2.1 20240805]
# Embedded file name: enc.py
# Compiled at: 2024-08-28 17:57:14
# Size of source mod 2**32: 1187 bytes
import sys
from PIL import Image
flag = sys.argv[1]

def enc(old_matrix, new_matrix, flag):
    flag = "".join((format(ord(i), "08b") for i in flag))
    index = 0
    for i in range(width):
        for j in range(height):
            a, b, c = old_matrix[(i, j)]
            if i % 11 == 0:
                if j % 11 == 0:
                    if b % 2 == 0:
                        if index >= len(flag):
                            new_matrix[(i, j)] = (137, 137, 137)
                            return None
                        else:
                            if int(flag[index]) == 0:
                                if old_matrix[(i, j)][2] % 2 != 0:
                                    new_matrix[(i, j)] = (
                                     a, b, c - 1)
                            elif old_matrix[(i, j)][2] % 2 != 1:
                                new_matrix[(i, j)] = (
                                 a, b, c + 1)
                            index += 1


old_image = Image.open("./in.png").convert("RGB")
(width, height) = old_image.size
print(width, height)
new_image = Image.new("RGB", (width, height))
old_matrix = old_image.load()
new_matrix = new_image.load()
for i in range(width):
    for j in range(height):
        new_matrix[(i, j)] = old_matrix[(i, j)]

enc(old_matrix, new_matrix, flag)
new_image.save("./out.png")
old_image.close()
new_image.close()
print("done!")

# okay decompiling ../../public/enc.cpython-38.pyc
