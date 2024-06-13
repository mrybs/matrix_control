from libshell import shell, set_color, ERROR_COLOR

import config
import fill
import get_info
import get_matrix
import get_effect_settings
import stream_matrix
import make_image
import pixel
import send_image


def command_stream():
    stream_matrix.stream_matrix()


def command_show():
    get_matrix.show_matrix()

def command_settings():
    get_effect_settings.print_effect_settings(get_effect_settings.get_effect_settings())


def command_not_found():
    set_color(ERROR_COLOR)
    print('Command not found\n')


if __name__ == '__main__':
    shell(
        {
            'stream': command_stream,
            'show': command_show,
            'settings': command_settings
        },
        (
            'show',
            'settings'
        ),
        command_not_found,
        ("\033[0m>>> ", 4)
    )
