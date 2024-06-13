from config import *
from PIL import Image


def make_image(width, heigth, photo_path, image_path):
    original = Image.open(photo_path)
    resized = original.resize((width, heigth), Image.NEAREST)
    resized.load()
    photo = open(image_path, "w", encoding="ASCII")


    for i in range(0, width*heigth):
        pixel=resized.getpixel((i%width, int(i/heigth)))
        r = ''.join(hex(pixel[0])[2:]).upper()
        g = ''.join(hex(pixel[1])[2:]).upper()
        b = ''.join(hex(pixel[2])[2:]).upper()
        if len(r) == 1:
            r = '0'+r
        if len(g) == 1:
            g = '0'+g
        if len(b) == 1:
            b = '0'+b
        photo.write(r+g+b+'FF')

    photo.close()

if __name__ == '__main__': 
    make_image(WIDTH, HEIGHT, PHOTO_PATH, IMAGE_PATH)
