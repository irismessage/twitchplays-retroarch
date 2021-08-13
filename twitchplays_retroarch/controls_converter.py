import configparser
import re
from pathlib import Path

import toml

# mapping of RetroArch code (left) to PyAutoGUI code (right)
# https://gist.github.com/Monroe88/0f7aa02156af6ae2a0e728852dcbfc90 and experimentation for libretro codes
# https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L114 for PyAutoGUI codes
MAPPING = {
    'rshift': 'shiftright',
    'kp_enter': 'separator',
    'add': '+',
    'subtract': '-',
    'kp_plus': 'add',
    'kp_minus': 'subtract',
    'period': '.',
    'print_screen': 'printscreen',
    'scroll_lock': 'scrolllock',
    'tilde': '~',
    'backquote': '`',
    'quote': "'",
    'comma': ',',
    'minus': '-',
    'slash': '/',
    'semicolon': ';',
    'equals': '=',
    'leftbracket': '[',
    'rightbracket': ']',
    'backslash': '\\',
    'kp_period': 'decimal',
    'kp_equals': '',
    'rctrl': 'controlright',
    'ralt': 'altright',
    'num0': '0',
    'num1': '1',
    'num2': '2',
    'num3': '3',
    'num4': '4',
    'num5': '5',
    'num6': '6',
    'num7': '7',
    'num8': '8',
    'num9': '9',
    'keypad0': 'num0',
    'keypad1': 'num1',
    'keypad2': 'num2',
    'keypad3': 'num3',
    'keypad4': 'num4',
    'keypad5': 'num5',
    'keypad6': 'num6',
    'keypad7': 'num7',
    'keypad8': 'num8',
    'keypad9': 'num9',
}
CFG_KEY_PATTERN = re.compile(r'input_(player[0-9]{1,2})_([a-z0-9_]+)')
CONFIG_DUMMY_HEADER = 'config'


def libretro_cfg_to_pyautogui_toml(in_path: Path, out_path: Path, mapping: dict = None):
    """Convert libretro control schemes to this program's control scheme.

    Args:
        in_path -- Path to the libretro .cfg file
        out_path -- Path to create the .toml file with PyAutoGUI key codes
        mapping -- mapping of libretro to PyAutoGUI key names as a dict. Default controls_converter.MAPPING
    """
    if mapping is None:
        mapping = MAPPING

    config_parser = configparser.ConfigParser()
    # need to do this because configparser needs headers and libretro cfg doesn't have them
    in_string = in_path.read_text(encoding='utf-8')
    in_string = f'[{CONFIG_DUMMY_HEADER}]\n' + in_string
    config_parser.read_string(in_string, source=str(in_path))

    libretro_config = config_parser[CONFIG_DUMMY_HEADER]
    toml_config = {}

    # actual conversion here
    for key, value in libretro_config.items():
        key_match = re.match(CFG_KEY_PATTERN, key)
        if key_match:
            # libretro cfg uses quotes around values, configparser doesn't
            libretro_keycode = value.strip('"')
            player_id = key_match[1]
            key_name = key_match[2]

            # try to get PyAutoGUI equivalent keycode from mapping. If it's not in the mapping it should be the same
            pyautogui_keycode = mapping.get(libretro_keycode, default=libretro_keycode)

            toml_config[player_id][key_name] = pyautogui_keycode

    with open(out_path, 'w', encoding='utf-8') as toml_file:
        toml.dump(toml_config, toml_file)
