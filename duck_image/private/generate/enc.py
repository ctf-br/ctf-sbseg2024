import sys
from PIL import Image

flag = sys.argv[1]

def enc(old_matrix,new_matrix, flag):
    flag = ''.join(format(ord(i), '08b') for i in flag)
    index = 0
    
    for i in range(width):
        for j in range(height):
            a, b, c = old_matrix[i,j]
            if i % 11 == 0 and j % 11 == 0 and b % 2 == 0:
                if(index >= len(flag)):
                    new_matrix[i,j] = (137, 137, 137)
                    return
                if int(flag[index]) == 0:
                    if old_matrix[i,j][2] % 2 != 0:
                        new_matrix[i,j] = (a, b, c - 1)
                else:
                    if old_matrix[i,j][2] % 2 != 1:
                        new_matrix[i,j] = (a, b, c + 1)
                index += 1
    
    return

old_image = Image.open("./in.png").convert("RGB")

width, height = old_image.size
print(width,height)

new_image = Image.new("RGB", (width, height))

old_matrix = old_image.load()
new_matrix = new_image.load()

for i in range(width):
    for j in range(height):
        new_matrix[i,j] = old_matrix[i,j]

enc(old_matrix,new_matrix,flag)

new_image.save("./out.png")

old_image.close()
new_image.close()

print('done!')
