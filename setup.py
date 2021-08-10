import setuptools
import twitchplays_retroarch


with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='twitchplays-retroarch',
    version=twitchplays_retroarch.__version__,
    author='JMcB',
    author_email='joel.mcbride1@live.com',
    license='GPLv3',
    description='witch Plays application for RetroArch/FBNeo, with input queue and chat control toggle shortcut.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JMcB17/twitchplays-retroarch',
    packages=setuptools.find_packages(),
    package_data={
        '': 'config.example.toml',
    },
    entry_points={
        'console_scripts': [
            'twitchplays-retroarch=twitchplays_retroarch:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Natural Language :: English',
        'Topic :: Games/Entertainment',
    ],
    python_requires='>=3',
    install_requires=[
        'twitchio>=2,<3',
        'PyAutoGUI>=0.9,<0.10',
        'toml>=0.10,<0.11',
        'keyboard>=0.13,<0.14',
    ]
)
