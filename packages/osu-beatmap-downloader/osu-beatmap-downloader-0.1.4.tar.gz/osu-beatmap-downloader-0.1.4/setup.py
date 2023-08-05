# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osu_beatmap_downloader']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0', 'loguru>=0.4.1,<0.5.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['osu-beatmap-downloader = osu_beatmap_downloader:main']}

setup_kwargs = {
    'name': 'osu-beatmap-downloader',
    'version': '0.1.4',
    'description': 'Downloads x most favorized beatmapsets into your osu! song directory',
    'long_description': "# Osu! Beatmapset Downloader\n\nDownloads given number of beatmapsets with the most favorites from [osu.ppy.sh](https://osu.ppy.sh/beatmapsets) into the default osu! directory.\n\n## Installation\n\nYou can install this program via `pip`:\n```\npip install osu-beatmap-downloader\n```\nThis will install the program in the global python package folder inside your python installation directory.\n\nYou can also install it into your python `user` directory with:\n```\npip install --user osu-beatmap-downloader\n```\n\nThese directories might not be in PATH. If you want to use this program from the command line, you may have to add the correct directories to PATH.\n\n## Usage\n\nTo start the downloader use:\n```\nosu-beatmap-downloader\n```\nThe program will ask for your osu! username and password because [osu.ppy.sh](https://osu.ppy.sh/beatmapsets) won't let you download beatmaps without being logged in.\n\nThe program will then ask you if you want to save your credentials so that you don't have to enter them every time you want to start the program. They will be stored in `%USERPROFILE%/.osu-beatmap-downloader/credentials.json` in **plaintext** (yes, that includes your password!). If you want to delete the credential file you can run:\n```\nosu-beatmap-downloader --delete-creds\n```\n\nBy default the program will download the **top 200** beatmaps. You can change the limit with:\n```\nosu-beatmap-downloader --limit 500\n```\nor\n```\nosu-beatmap-downloader -l 500\n```\n\nThe programm will limit its rate to 30 files per minute to prevent unnecessary load on osu!s website.\nDespite this after a specific amount of songs (that I don't know) the website will prevent any further downloads. The program will terminate after 5 failed downloads. In this case **you might have to wait for half an hour or even longer** before you can download again.\n\nEvery step will be printed in your command line window and will also be logged in `%USERPROFILE%/.osu-beatmap-downloader/downloader.log` if you want to look at it later.\n",
    'author': 'Vincent Mathis',
    'author_email': 'vincemathis94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vincentmathis/osu-beatmap-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
