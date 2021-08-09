from pathlib import Path

import toml
import twitchio.ext.commands


CONFIG_PATH = Path('config.toml')


class TwitchPlaysRetroArchBot(twitchio.ext.commands.bot.Bot):
    def __init__(self, *args, **kwargs):
        # for pausing user control
        self.twitchplays_commands_enabled = True

        super().__init__(*args, **kwargs)

    def twitchplays_commands_toggle(self):
        self.twitchplays_commands_enabled = not self.twitchplays_commands_enabled

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
    bot.start()
