from config import *
import requests


def pixel(matrix_ip, x, y, colors: dict):
    request = f'http://{matrix_ip}/api?function=pixel&x={x}&y={y}'
    for color in list(colors):
        request += f'&{color}={colors[color]}'
    requests.get(request, timeout=1000)


if __name__ == '__main__':
    pixel(MATRIX_IP, 0, 0, {'r': 255, 'b': 64}) 
