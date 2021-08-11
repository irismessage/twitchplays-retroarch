import sys
from typing import Union, List


def yn(
    prompt: str = 'Y/n\n',
    empty_response: Union[None, bool] = True,
    affirmative: List[str] = None,
    negative: List[str] = None
) -> bool:
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
    input(prompt)
    sys.exit(status)
