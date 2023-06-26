IMAGE_PATH = 'photos/photo.txt'
MATRIX_IP = '192.168.50.77'


import config
import requests
def send_image(image_path, matrix_ip):
	image = open(image_path, 'r').read()
	requests.get(f'http://{matrix_ip}/api?function=image&image={image}')

if __name__ == '__main__':
	send_image(IMAGE_PATH, MATRIX_IP)