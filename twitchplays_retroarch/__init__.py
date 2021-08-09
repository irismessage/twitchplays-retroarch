import queue
import concurrent.futures
import time
from pathlib import Path

import pyautogui
import keyboard
import toml
import twitchio.ext.commands


# todo: add logging
# todo: add docstrings
# todo: customisable command set
# todo: sync command set with RetroArch config files


CONFIG_PATH = Path('config.toml')


class TwitchPlaysRetroArchBot(twitchio.ext.commands.bot.Bot):
    test_keys_fbneo = {
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
        'button1': 'z',
        'button2': 'x',
        'start': 'enter',
        'COIN': 'shiftright',
    }

    def __init__(
            self,
            case_sensitive: bool = False,
            keypress_delay: float = 0.1, keypress_duration: float = 0.1,
            input_threads: int = 1,
            *args, **kwargs
    ):
        self.case_sensitive = case_sensitive
        self.keypress_delay = keypress_delay
        self.keypress_duration = keypress_duration
        # for pausing user control
        self.twitchplays_commands_enabled = True

        self.input_queue = queue.Queue()
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=input_threads, initializer=self.input_handle_loop
        )

        super().__init__(*args, **kwargs)

    async def event_ready(self):
        print('Connected.')

    def twitchplays_commands_toggle(self):
        self.twitchplays_commands_enabled = not self.twitchplays_commands_enabled

        if self.twitchplays_commands_enabled:
            status = 'enabled'
        else:
            status = 'disabled'
        print(f'Twitch Plays commands {status}.')

    def input_handle_loop(self):
        while True:
            if not self.input_queue.empty():
                key_to_press = self.input_queue.get()
                pyautogui.press(key_to_press, interval=self.keypress_duration)
                time.sleep(self.keypress_delay)

    async def process_twitchplays_commands(self, message: twitchio.Message) -> bool:
        commandset = self.test_keys_fbneo

        command = message.content
        if not self.case_sensitive:
            command = command.casefold()

        if command in commandset:
            key_to_press = commandset[command]
            self.input_queue.put(key_to_press)
            return True

        return False

    async def event_message(self, message: twitchio.Message):
        # ignore messages from the bot
        if message.echo:
            return

        if self.twitchplays_commands_enabled:
            await self.process_twitchplays_commands(message)

        # handle commands, like in the base event_message
        await self.handle_commands(message)


def main():
    with open(CONFIG_PATH) as config_file:
        config = toml.load(config_file)

    bot = TwitchPlaysRetroArchBot(
        token=config['twitch']['token'],
        # todo: put in config?
        prefix='!',
        initial_channels=[config['twitch']['channel_to_join']]
    )

    keyboard.add_hotkey(
        config['hotkeys']['toggle_allow_twitchplays_commands'],
        bot.twitchplays_commands_toggle,
        suppress=True
    )

    bot.run()
