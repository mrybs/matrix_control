import sys
import requests
import config


def get_matrix(matrix_ip=config.MATRIX_IP, width=config.WIDTH, height=config.HEIGHT):
    request = f'http://{matrix_ip}/api?function=getMatrix'
    hex_colors = requests.get(request, timeout=1000).text
    matrix = []
    i = 0
    for y in range(height):
        matrix.append([])
        for x in range(width):
            i = y*width+x
            hex_color = hex_colors[i*6:i*6+6]
            matrix[-1].append((
                int(hex_color[:2], base=16), 
                int(hex_color[2:4], base=16), 
                int(hex_color[4:], base=16)
            ))
    return matrix


def print_matrix(matrix, aspectx=1, aspecty=2, numbers=False, dots=False):
    if numbers:
        sys.stdout.write('   '+''.join([f'{i:>2}' for i in range(1, len(matrix[0])+1)])+'\n')
    for i, y in enumerate(matrix):
        for _ in range(aspectx):
            if numbers:
                sys.stdout.write((str(i+1).rjust(aspecty) if _ == aspectx - 1 else ' '*aspecty) + ' ')
            for x in y:
                sys.stdout.write(f'\033[48;2;{x[0]};{x[1]};{x[2]}m' + (('.' if aspectx >= aspecty else ':') if dots else ' ')*aspecty)
            sys.stdout.write('\033[0m')
            if numbers:
                sys.stdout.write(str(i+1).ljust(aspecty))
            sys.stdout.write('\n')
    if numbers:
        sys.stdout.write('   '+''.join([f'{i:<2}' for i in range(1, len(matrix[0])+1)])+'\n')
    sys.stdout.flush()


def show_matrix(matrix_ip=config.MATRIX_IP, width=config.WIDTH, height=config.HEIGHT, aspectx=1, aspecty=2, numbers=False, dots=False):
    request = f'http://{matrix_ip}/api?function=getMatrix'
    hex_colors = requests.get(request, timeout=1000).text
    matrix = []
    i = 0
    for y in range(height):
        for _ in range(aspectx):
            if numbers:
                sys.stdout.write((str(i+1).rjust(aspecty) if _ == aspectx - 1 else ' '*aspecty) + ' ')
            for x in range(width):
                i = y*width+x
                hex_color = hex_colors[i*6:i*6+6]
                sys.stdout.write(f'\033[48;2;{int(hex_color[:2], base=16)};{int(hex_color[2:4], base=16)};{int(hex_color[4:], base=16)}m' + (('.' if aspectx >= aspecty else ':') if dots else ' ')*aspecty)
            sys.stdout.write('\033[0m')
            if numbers:
                sys.stdout.write(str(i+1).ljust(aspecty))
            sys.stdout.write('\n')
    if numbers:
        sys.stdout.write('   '+''.join([f'{i:<2}' for i in range(1, len(matrix[0])+1)])+'\n')
    sys.stdout.flush()

if __name__ == '__main__':
    print_matrix(get_matrix())
