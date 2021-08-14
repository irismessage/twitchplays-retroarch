"""Tools for converting RetroArch controls to command sets for Twitch Plays."""

import configparser
import re
import sys
import logging as log
from pathlib import Path
from typing import Union

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
CFG_NAME = 'retroarch.cfg'
CFG_NONE_STRING = 'nul'
CONVERSION_DEST = 'converted-retroarch-controls.toml'
TOML_HEADER = '# This contains control schemes grabbed and converted from your RetroArch settings.\n' \
              '# You can take any one of these sections, and put it in your config file as [keys].\n'


def convert_dicts(libretro_config: dict, mapping: dict) -> dict:
    """Convert a config dict from libretro cfg to one for toml."""
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
            pyautogui_keycode = mapping.get(libretro_keycode, libretro_keycode)

            # ignore nul values and special values, which are just digits
            if pyautogui_keycode != CFG_NONE_STRING and not pyautogui_keycode.isdigit():
                toml_config.setdefault(player_id, {})[key_name] = pyautogui_keycode

    return toml_config


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
    config_dummy_header = 'config'
    in_string = f'[{config_dummy_header}]\n' + in_string
    config_parser.read_string(in_string, source=str(in_path))
    libretro_config = config_parser[config_dummy_header]

    toml_config = convert_dicts(dict(libretro_config), mapping)

    toml_config_string = toml.dumps(toml_config)
    toml_config_string = TOML_HEADER + toml_config_string
    with open(out_path, 'w', encoding='utf-8') as toml_file:
        toml_file.write(toml_config_string)


def locate_libretro_config() -> Union[Path, None]:
    """Try to find libretro.cfg depending on platform.

    Returns None if not found in search locations.
    """
    libretro_cfg_locations_platforms = {
        'win32': [
            Path(r'C:\RetroArch-Win64'),
            Path(r'C:\Program Files\RetroArch'),
            Path(r'C:\Program Files (x86)\RetroArch'),
            Path.home().joinpath(r'AppData\Roaming\RetroArch'),
        ],
        'darwin': [
            Path.home().joinpath('Library/Application Support/Retroarch'),
        ],
        'linux': [
            Path('/etc'),
            Path.home(),
            Path.home().joinpath('.config/retroarch'),
        ]
    }
    libretro_cfg_locations_default = [Path()]

    for platform in libretro_cfg_locations_platforms:
        if sys.platform.startswith(platform):
            cfg_locations = libretro_cfg_locations_platforms[platform]
            break
    else:
        cfg_locations = libretro_cfg_locations_default

    for location in cfg_locations:
        if location.is_dir():
            return location / CFG_NAME

    return None


def auto_conversion(
        cfg_location: Path = None,
        github_link: str = 'GitHub', config_name: str = 'your config file'
):
    """Search for and convert libretro config.

    Uses locate_retroarch_config if not given as argument.
    Returns True if successful.
    """
    log.info('Trying to automatically convert RetroArch controls settings to use..')

    # try to find if not given as an argument
    if cfg_location is None:
        log.info('Searching for RetroArch installation..')
        cfg_location = locate_libretro_config()
    # search failed, quit
    if cfg_location is None:
        log.error(
            'Unable to location RetroArch installation. \n'
            "  If you have RetroArch installed in a normal location but it couldn't be found, please get in touch. \n"
            '  (%s) \n'
            '  If you can find RetroArch/retroarch.cfg yourself, copy it into this folder, or use the -rc argument.',
            github_link
        )
        return False

    log.info('Found RetroArch config at %s.', cfg_location)
    dest = Path(CONVERSION_DEST)
    log.info('Converting RetroArch controls configuration to %s.', dest)
    # todo: better error handling?
    try:
        libretro_cfg_to_pyautogui_toml(cfg_location, dest)
    except Exception as error:
        log.error('Unable to convert libretro config!', exc_info=error)
        return False
    else:
        log.info(
            'Successfully converted RetroArch configuration. Check %s for control scheme templates to put in %s!',
            dest, config_name
        )
        return True
