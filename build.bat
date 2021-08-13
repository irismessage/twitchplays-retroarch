git archive -o downloads\twitchplays-retroarch.zip HEAD
git archive -o downloads\twitchplays-retroarch.tar.gz HEAD
git bundle create downloads\twitchplays_retroarch.bundle main

.venv\Scripts\python.exe -m pip install -U pip wheel setuptools
.venv\Scripts\python.exe setup.py sdist bdist_wheel

py -3.9 -m pip install -U pip wheel
py -3.9 -m pip install -U pyinstaller
pyinstaller --noconfirm --log-level WARN ^
--onefile ^
--paths .venv\Lib\site-packages ^
--add-data config.example.toml;. ^
--name twitchplays-retroarch ^
--icon assets\tpra-logo1-256.ico ^
--distpath downloads\ ^
twitchplays_retroarch\__main__.py
