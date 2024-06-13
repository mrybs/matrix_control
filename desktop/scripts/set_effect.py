import random
import requests
import config


def set_effect(matrix_ip, effect_id: str):
    print('Responded message:', requests.get(f'http://{matrix_ip}/api?function=effect&effect={effect_id}', timeout=1000).text)


if __name__ == '__main__':
    set_effect(config.MATRIX_IP, random.choice(config.EFFECTS_IDS))
