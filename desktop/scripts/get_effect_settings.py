from pprint import pprint
import config
import requests


def get_effect_settings(matrix_ip=config.MATRIX_IP):
    request = f'http://{matrix_ip}/api?function=getEffectSettings'
    return requests.get(request, timeout=1000).json()


def print_effect_settings(effect_settings):
    for key in effect_settings:
        print(f'{key}: {effect_settings[key]}')


if __name__ == '__main__':
    pprint(get_effect_settings(config.MATRIX_IP))
