import readchar
import string
import shutil
import sys
import signal

def get_terminal_size():
    return shutil.get_terminal_size((80, 20)).columns

def resize_handler(signum, frame):
    global terminal_width
    new_terminal_width = get_terminal_size()
    if new_terminal_width != terminal_width:
        terminal_width = new_terminal_width
        redraw()

def redraw():
    global line, cursor_position, terminal_width

    # Calculate the number of lines needed to display the current text
    lines = [line[i:i+terminal_width] for i in range(0, len(line), terminal_width)]

    # Move up as many lines as we need to clear the input
    num_lines = len(lines)
    sys.stdout.write(f'\033[{num_lines}A')  # Move up `num_lines` lines

    # Clear the input lines
    for _ in range(num_lines):
        sys.stdout.write('\033[K\n')
    sys.stdout.write('\033[K')  # Clear the last line

    # Print all the lines
    sys.stdout.write(f'\033[{num_lines}A')  # Move back up to the starting line
    for line_part in lines:
        sys.stdout.write(line_part + '\n')
    
    # Move cursor back up to the correct position
    sys.stdout.write(f'\033[{num_lines}A')

    # Calculate the new cursor position within the text
    cursor_row = cursor_position // terminal_width
    cursor_col = cursor_position % terminal_width

    # Move the cursor to the correct position within the text
    sys.stdout.write(f'\033[{cursor_row}B\033[{cursor_col}C')
    
    # Restore cursor position
    sys.stdout.write('\0338')
    sys.stdout.flush()

def main():
    global line, cursor_position, terminal_width

    line = ''
    cursor_position = 0
    terminal_width = get_terminal_size()

    signal.signal(signal.SIGWINCH, resize_handler)

    print("Type your text below (Press 'Ctrl+C' to exit):\n")

    try:
        while True:
            ch = readchar.readchar()

            if ch == '\x03':  # Ctrl+C
                break
            elif ch in {'\x08', '\x7f'}:  # Backspace/Delete
                if cursor_position > 0:
                    cursor_position -= 1
                    line = line[:cursor_position] + line[cursor_position+1:]

                    # Move cursor back one space
                    sys.stdout.write('\b \b')

                    # Redraw the remaining part of the line after the cursor
                    sys.stdout.write(line[cursor_position:] + ' ')
                    sys.stdout.write('\b' * (len(line) - cursor_position + 1))
                    sys.stdout.flush()
            elif ch in string.printable or ch > '\x7f':  # Printable characters and unicode
                line = line[:cursor_position] + ch + line[cursor_position:]
                cursor_position += 1
                sys.stdout.write(ch)
                sys.stdout.flush()

                if cursor_position % terminal_width == 0:
                    print()

    except KeyboardInterrupt:
        pass

    print("\n\nFinal text:")
    print(line)

if __name__ == "__main__":
    main()
