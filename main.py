import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def color_text(text, color_name):
    global color_mode
    if color_mode:
        colors = {
            "black": "\033[38;2;173;216;230m",
            "red": "\033[38;2;255;81;81m",
            "green": "\033[38;2;152;251;152m",
            "yellow": "\033[33m",
            "blue": "\033[38;2;135;206;250m",
            "magenta": "\033[38;2;221;160;221m",
            "cyan": "\033[38;2;0;255;255m",
            "white": "\033[38;2;245;245;245m"
        }
        reset_color = "\033[0m"
        if color_name in colors:
            return f"{colors[color_name]}{text}{reset_color}"
        else:
            return text
    else:
        return text