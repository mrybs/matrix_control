from config import *
import requests


def get_info(matrix_ip):
    request = f'http://{matrix_ip}/api?function=getInfo'
    info = []
    for data in requests.get(request, timeout=1000).text.split(';'):
        info.append((data.split(':')[0], ':'.join(data.split(':')[1:])))
    return info


if __name__ == '__main__':
    print(get_info(MATRIX_IP))