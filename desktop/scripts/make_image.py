from config import *
from PIL import Image


def make_image(width, heigth, photo_path, image_path):
    original = Image.open(photo_path)
    resized = original.resize((width, heigth), Image.NEAREST)
    resized.load()
    photo = open(image_path, "wb")


    for i in range(0, width*heigth):
        pixel=resized.getpixel((i%width, int(i/heigth)))
        photo.write(pixel[0].to_bytes()+pixel[1].to_bytes()+pixel[2].to_bytes())

    photo.close()

if __name__ == '__main__': 
    make_image(WIDTH, HEIGHT, PHOTO_PATH, IMAGE_PATH)
