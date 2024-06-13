from config import *
import requests


def fill(matrix_ip, colors: dict):
    request = f'http://{matrix_ip}/api?function=fill'
    for color in list(colors):
        request += f'&{color}={colors[color]}'
    requests.get(request, timeout=1000)


if __name__ == '__main__':
    fill(MATRIX_IP, {'r': 255, 'b': 64}) 
