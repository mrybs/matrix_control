from config import *
from make_image import make_image
from send_image import send_image


def makeNsend_image(width, height, photo_path, image_path, matrix_ip):
    make_image(width, height, photo_path, image_path)
    send_image(image_path, matrix_ip)

if __name__ == '__main__':
    makeNsend_image(WIDTH, HEIGHT, PHOTO_PATH, IMAGE_PATH, MATRIX_IP)