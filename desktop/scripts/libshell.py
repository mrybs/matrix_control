import os
import re
import sys
import readchar
from wcwidth import wcswidth
from string import printable


ERROR_COLOR = (225, 48, 48)
HINT_COLOR = (100, 100, 100)
INPUT_COLOR = (200, 200, 200)
COMMAND_COLOR = (255, 255, 255)

def optional(func, *args, **kwargs) -> any:
    _args, _kwargs, k = [], {}, {}
    s = [arg.split(':')[0].strip() for arg in ')'.join('('.join(str(inspect.signature(func)).split('(')[1:]).split(')')[:-1]).split(',')]
    for key in kwargs.keys():
        if key in s:
            k[key] = kwargs[key]
    kwargs = k
    if len(s) < len(args):
        _args = args[:-len(s)]
    elif len(s) < len(args) + len(kwargs):
        _args, _kwargs = args[:-len(s)], {list(kwargs.keys())[i]: kwargs[list(kwargs.keys())[i]] for i in
                                          range(len(kwargs) - len(s) - len(args))}
    else:
        _args, _kwargs = args, kwargs
    return func(*_args, **_kwargs)

def flush():
    sys.stdout.flush()

def write(string):
    sys.stdout.write(string)

def save_cursor():
    write('\033[s')

def restore_cursor():
    write('\033[u')

def set_color(color):
    write(f'\033[38;2;{color[0]};{color[1]};{color[2]}m')

def reset_color():
    write('\033[0m')


def make_hint(text: str, hints: tuple[str], index: int) -> str:
    can_be = []
    for i, hint in enumerate(hints):
        syntax = '^('+'|$)('.join(hint) + '|$)$'
        if re.match(syntax, text) is not None:
            if hint.removeprefix(text) != '':
                can_be.append(i)
    return hints[can_be[index%len(can_be)]].removeprefix(text) if len(can_be) != 0 else ''


def unicode_split(text: str):
    def merge(l: list[str], joiners: list[str]):
        buffer = ''
        for i, e in enumerate(l):
            buffer += e
            if e not in joiners and i != len(l)-1 and l[i+1] not in joiners:
                yield buffer
                buffer = ''
        if buffer != '':
            yield buffer

    return list(merge(list(text), ('\u200d', )))


def shell(commands: dict, hints: tuple[str], command_not_found, PS1: str):
    #full_buffer = ''
    buffer: str = ''
    non_printable_buffer: str = ''
    cursor = PS1[1]
    #terminal_size = os.get_terminal_size()
    index = 0
    hint: str = ''
    write(PS1[0])
    #full_buffer += PS1[0]
    flush()
    while ch := readchar.readchar():
        #if terminal_size != os.get_terminal_size():
        #    save_cursor()
        #    write('\x1b[0;0H')
        #    import math
        #    print(math.ceil(len(full_buffer.replace('\n', ''))/os.get_terminal_size().columns))
        #    restore_cursor()
        #    
        #    write(f'\033[{math.ceil(len(full_buffer.replace('\n', ''))/os.get_terminal_size().columns)}A\033[999D')
        #    for c in full_buffer:
        #        if (len(full_buffer) - 1) % (os.get_terminal_size().columns - 1) == 0:
        #            if len(full_buffer) > 0:
        #                write('\r\n')
        #        write(c)
        #    terminal_size = os.get_terminal_size()
        buffer += ch
        if ch == '\t':
            buffer = buffer[:-1]
        elif ch == '\177':
            buffer = buffer[:-1]
            chars = unicode_split(buffer)
            if len(chars) > 0:
                width = wcswidth(chars[-1])
                write(f'\x1b[{width if width > 0 else 0}D\033[0K')
                buffer = buffer.removesuffix(chars[-1])
                #full_buffer = full_buffer.removesuffix(chars[-1])
                if cursor % os.get_terminal_size().columns == 0:
                    write(f'\033[{os.get_terminal_size().columns}C\033[1A')
                    cursor -= os.get_terminal_size().columns
                save_cursor()
                set_color(HINT_COLOR)
                write(hint)
                reset_color()
                restore_cursor()
                cursor -= 1
            else:
                write('\a')
        if hint == '':
            write('\033[0K')

        if ch == '\n':
            write('\033[0K\n')
            #full_buffer += '\n'
            reset_color()
            (commands[buffer.strip().split()[0]] if
            len(buffer.strip()) > 0 and
            buffer.strip().split()[0] in commands
            else command_not_found)()
            reset_color()
            write(PS1[0])
            cursor = PS1[1]
            buffer = ''
            #full_buffer += PS1[0]
        elif ch == '\t':
            hint = make_hint(buffer, hints, index)
            buffer += hint
            #full_buffer += hint
            cursor += len(hint)
            set_color(INPUT_COLOR)
            write(hint)
        elif ch == '\177':
            pass
        elif ch == '\003':
            sys.exit()
        elif ch == '\x1b':
            buffer = buffer[:-1]
            non_printable_buffer = '\x1b'
        elif len(non_printable_buffer) > 0 and non_printable_buffer[-1] == '\x1b' and ch == '[':
            buffer = buffer[:-1]
            non_printable_buffer = '\x1b['
        elif len(non_printable_buffer) > 1 and non_printable_buffer[-2] == '\x1b' and non_printable_buffer[-1] == '[':
            buffer = buffer[:-1]
            if ch == 'A':
                index += 1
                non_printable_buffer = ''
            elif ch == 'B':
                index -= 1
                non_printable_buffer = ''
            elif ch == 'C':
                hint = make_hint(buffer, hints, index)
                buffer += hint
                #full_buffer += hint
                cursor += len(hint)
                set_color(INPUT_COLOR)
                write(hint)
        elif ch in printable or ch > '\x7f':
            if (len(buffer) + PS1[1] - 1) % (os.get_terminal_size().columns - 1) == 0:
                if len(buffer) - PS1[1] > 0:
                    write('\r\n')
            set_color(INPUT_COLOR)
            write(ch)
            #full_buffer += ch
            cursor += wcswidth(ch)
        save_cursor()
        set_color(HINT_COLOR)
        write('\033[0K')
        hint = make_hint(buffer, hints, index)
        write(hint)
        reset_color()
        restore_cursor()
        flush()
