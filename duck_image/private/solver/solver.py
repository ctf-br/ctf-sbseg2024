from PIL import Image

def dec(pixel_map):
    flag = ''
    
    for i in range(width):
        for j in range(height):
            a, b, c = pixel_map[i,j]
            if(a == 137 and b == 137  and c == 137):
                return flag
            if i % 11 == 0 and j % 11 == 0 and b % 2 == 0:
                if pixel_map[i,j][2] % 2 == 0:
                    flag += '0'
                else:
                    flag += '1'

image = Image.open('./out.png')
width, height = image.size

pixel_map = image.load()

flag = dec(pixel_map)
print(flag)

image.close()