from pathlib import Path

import keyboard
import toml
import twitchio.ext.commands


# todo: add logging
# todo: add docstrings


CONFIG_PATH = Path('config.toml')


class TwitchPlaysRetroArchBot(twitchio.ext.commands.bot.Bot):
    def __init__(self, *args, **kwargs):
        # for pausing user control
        self.twitchplays_commands_enabled = True

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

    async def process_twitchplays_commands(self, message: twitchio.Message) -> bool:
        # todo: implement
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
