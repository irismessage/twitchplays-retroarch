# twitchplays-retroarch
Twitch Plays application for RetroArch/FBNeo, with input queue and chat control toggle shortcut.

Commissioned by twitch.tv/LastTimeLord.

Made with [twitchio](https://github.com/TwitchIO/TwitchIO) and [PyAutoGUI](https://github.com/asweigart/pyautogui) ([PyDirectInput](https://github.com/learncodebygaming/pydirectinput) when on Windows).

Informed by [controlmypc](https://gitlab.com/controlmypc/TwitchPlays) and DougDoug's Twitch Plays projects.

## Features:
- Input queue - commands are processed with a queue system and always executed in the order they're sent.
- Hotkeys - add global hotkeys (will work when not focused on the program window) for pausing chat control. Powered by [keyboard](https://github.com/boppreh/keyboard).
- Scalable - can use a thread pool to execute multiple inputs simultaneously.
- Customisable - change settings and commands in `config.toml`.
- Bot commands - try `!help`

## Installation and Usage:
### Download as an exe
If you want the easiest way to use this on Windows without knowing about or installing Python, you can go to the [releases page](https://github.com/JMcB17/twitchplays-retroarch/releases) on GitHub, select the latest one, and download the `twitchplays-retroarch.exe` file from the Assets section.

You can then run it from where ever you downloaded it.

### Install with pip from PyPI
This project is on PyPI: https://pypi.org/project/twitchplays-retroarch/

Just use `pip install twitchplays-retroarch`.

After it's installed you can run it `python -m twitchplays_retroarch` or just `twitchplays-retroarch`.    
You can also access its classes and functions with `import twitchplays_retroarch.`

### Clone from GitHub
The usual:
- `git clone https://github.com/JMcB17/twitchplays-retroarch`
- `cd twitchplays-retroarch`
- `pip install -r requirements.txt`
Then you can use `python -m twitchplays_retroarch` (from within this folder only).

## General Usage

Run the program for the first time, and it will prompt you to allow it to automatically create a new template `config.toml` file.

Open the file in a text editor. It's annotated with what each setting means.

The most important settings are at the start of the file under the `[twitch]` header. You'll need to set them in order to run the bot successfully.

After that, you can read and edit the other settings if you want more customisation.

You can also run the program with the `-h` command line flag for info.
