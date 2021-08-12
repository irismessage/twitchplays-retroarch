"""Utility functions for command line script."""

import ctypes
import os
import sys
from typing import Union, List


def yn(
    prompt: str = 'Y/n\n',
    empty_response: Union[None, bool] = True,
    affirmative: List[str] = None,
    negative: List[str] = None
) -> bool:
    """Give the user a y/n prompt and return True or False.

    Args:
        prompt -- input prompt
        empty_response -- if None, this function will loop until a valid response is given. If a boolean,
                          an empty response will return that value.
        affirmative -- list of responses that will return True, default 'y' and 'yes'
        negative -- list of responses that will return False, default 'n' and 'no'
    """
    if affirmative is None:
        affirmative = ['y', 'yes']
    if negative is None:
        negative = ['n', 'no']

    while True:
        response = input(prompt).casefold()
        if empty_response is not None and not response:
            return empty_response
        elif response in affirmative:
            return True
        elif response in negative:
            return False


def q(
    status: int = 0,
    prompt: str = 'Press enter to exit.\n'
):
    """Wait for any input with prompt, then call sys.exit with status."""
    input(prompt)
    sys.exit(status)


def running_elevated() -> bool:
    """Return whether the program is running as admin or root."""
    if sys.platform == 'win32':
        return ctypes.windll.shell32.IsUserAnAdmin()
    elif sys.platform.startswith('linux'):
        return os.geteuid() == 0
