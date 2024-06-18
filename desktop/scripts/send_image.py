from config import *
import requests


def send_image(image_path, matrix_ip):
    image = open(image_path, 'rb').read()
    r = requests.post(f'http://{matrix_ip}/api', data=image, timeout=1000)
    print("Responded message:", r.text)

if __name__ == '__main__':
    send_image(IMAGE_PATH, MATRIX_IP)
