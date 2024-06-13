import time
import sys
import get_matrix
import config


def stream_matrix(matrix_ip=config.MATRIX_IP, width=config.WIDTH, height=config.HEIGHT, aspectx=config.ASPECT[0], aspecty=config.ASPECT[1], max_fps=30, numbers=False, dots=False):
    position = 0
    try:
        while True:
            position = 0
            get_matrix.show_matrix(matrix_ip, width=width, height=height, aspectx=aspectx, aspecty=aspecty, numbers=numbers, dots=dots)
            position = 1
            time.sleep(1/max_fps)
            sys.stdout.write(f'\x1b[{height*aspectx+2}A' if numbers else f'\x1b[{height*aspectx}A')
            position = 0
    except KeyboardInterrupt:
        if position == 1:
            print(f'\x1b[{height*aspectx+2}A' if numbers else f'\x1b[{height*aspectx}A')
        print((' '*(width*aspecty+6)+'\n')*(height*aspectx+2) if numbers else (' '*(width*aspecty)+'\n')*(height*aspectx))
        print(f'\x1b[{height*aspectx+4}A' if numbers else f'\x1b[{height*aspectx+2}A')
        print('Stream ended')


if __name__ == '__main__':
    stream_matrix(config.MATRIX_IP)
