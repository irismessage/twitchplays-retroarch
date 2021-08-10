py -m pip install -U pip wheel

py -m pip install -U setuptools twine
py setup.py sdist bdist_wheel

py -m pip install -U pyinstaller
pyinstaller --noconfirm --log-level WARN ^
    --onefile ^
    --paths .venv\Lib\site-packages ^
    --add-data config.example.toml;. ^
    --name twitchplays-retroarch ^
    twitchplays_retroarch\__main__.py
