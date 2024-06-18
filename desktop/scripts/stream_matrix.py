import time
import sys
import get_matrix
import config
from websocket import create_connection


def show_matrix(colors, matrix_ip=config.MATRIX_IP, width=config.WIDTH, height=config.HEIGHT, aspectx=1, aspecty=2, numbers=False, dots=False):
    matrix = []
    i = 0
    for y in range(height):
        for _ in range(aspectx):
            if numbers:
                sys.stdout.write((str(i+1).rjust(aspecty) if _ == aspectx - 1 else ' '*aspecty) + ' ')
            for x in range(width):
                i = y*width+x
                color = colors[i*3:i*3+3]
                sys.stdout.write(f'\033[48;2;{color[0]};{color[1]};{color[2]}m' + (('.' if aspectx >= aspecty else ':') if dots else ' ')*aspecty)
            sys.stdout.write('\033[0m')
            if numbers:
                sys.stdout.write(str(i+1).ljust(aspecty))
            sys.stdout.write('\n')
    if numbers:
        sys.stdout.write('   '+''.join([f'{i:<2}' for i in range(1, len(matrix[0])+1)])+'\n')
    sys.stdout.flush()


def stream_matrix(matrix_ip=config.MATRIX_IP, width=config.WIDTH, height=config.HEIGHT, aspectx=config.ASPECT[0], aspecty=config.ASPECT[1], max_fps=30, numbers=False, dots=False, connection_mode=config.STREAM_CONNECTION_MODE):
    if connection_mode not in {"websocket", "post"}:
        return print(f"Invalid: {connection_mode=}")
    position = 0
    ws = create_connection(f"ws://{config.MATRIX_IP}/ws")
    fps = 0
    i = 0
    try:
        while True:
            begin = time.time()
            position = 0
            ws.send("get_matrix\0")
            if connection_mode == "websocket":
                show_matrix(ws.recv(), matrix_ip=matrix_ip, width=width, height=height, aspectx=aspectx, aspecty=aspecty, numbers=numbers, dots=dots)
            elif connection_mode == "post":
                get_matrix.show_matrix(matrix_ip=matrix_ip, width=width, height=height, aspectx=aspectx, aspecty=aspecty, numbers=numbers, dots=dots)
            position = 1
            time.sleep(1/max_fps)
            sys.stdout.write(f'\x1b[{height*aspectx+2}A' if numbers else f'\x1b[{height*aspectx}A')
            position = 0
            fps += 1/(time.time()-begin)
            i += 1
    except KeyboardInterrupt:
        ws.close()
        if position == 1:
            print(f'\x1b[{height*aspectx+2}A' if numbers else f'\x1b[{height*aspectx}A')
        print((' '*(width*aspecty+6)+'\n')*(height*aspectx+2) if numbers else (' '*(width*aspecty)+'\n')*(height*aspectx))
        print(f'\x1b[{height*aspectx+4}A' if numbers else f'\x1b[{height*aspectx+2}A')
        print(f'Stream ended. Average fps {round(fps/i, 2)}')


if __name__ == '__main__':
    stream_matrix(config.MATRIX_IP)
