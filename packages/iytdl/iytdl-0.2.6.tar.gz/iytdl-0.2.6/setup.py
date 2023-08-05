# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iytdl', 'iytdl.types']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'Pyrogram>=1.2.9,<2.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'hachoir>=3.1.2,<4.0.0',
 'html-telegraph-poster>=0.4.0,<0.5.0',
 'mutagen>=1.45.1,<2.0.0',
 'youtube-search-python==1.4.6',
 'youtube_dl>=2021.6.6,<2022.0.0']

setup_kwargs = {
    'name': 'iytdl',
    'version': '0.2.6',
    'description': 'Asynchronous Standalone Inline YouTube-DL Module',
    'long_description': '<p align="center">\n<img src="https://i.imgur.com/Q94CDKC.png" width=250px>\n\n# iYTDL\n\n<a href="https://github.com/iytdl/iytdl/actions"><img alt="Actions Status" src="https://github.com/psf/black/workflows/Primer/badge.svg"></a>\n<a href="https://github.com/iytdl/iytdl/blob/main/LICENSE"><img alt="License: GPLv3" src="https://img.shields.io/badge/License-GPLv3-blue.svg"></a>\n<a href="https://pypi.org/project/iytdl/"><img alt="PyPI" src="https://img.shields.io/pypi/v/iytdl"></a>\n<a href="https://pepy.tech/project/iytdl"><img alt="Downloads" src="https://pepy.tech/badge/iytdl"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n</p>\n\n> Asynchronous Standalone Inline YouTube-DL Module\n\n## ⭐️ Features\n\n- Fully Asynchronous\n- Fast and Memory Efficient (uses Aiosqlite for Caching)\n- Uses search query based sha1 hashes to store results to avoid storing duplicate data\n- Supports Context Manager\n- [Supported Sites](https://ytdl-org.github.io/youtube-dl/supportedsites.html)\n\n## Requirements\n\n- Python >=3.8,<4\n- A Pyrogram Based Bot\n- FFmpeg\n\n## Callbacks\n\n- Back and Next\n\n```python\nr"^yt_(back|next)\\|(?P<key>[\\w-]{5,11})\\|(?P<pg>\\d+)$"\n```\n\n- List View\n\n```python\nr"^yt_listall\\|(?P<key>[\\w-]{5,11})$"\n```\n\n- Extract Info\n\n```python\nr"^yt_extract_info\\|(?P<key>[\\w-]{5,11})$"\n```\n\n- Download\n\n```python\nr"yt_(?P<mode>gen|dl)\\|(?P<key>[\\w-]+)\\|(?P<choice>[\\w-]+)\\|(?P<dl_type>a|v)$"\n```\n\n## Usage\n\n- Detailed usage with example\n\n### [iytdl_example.py](https://github.com/iytdl/iytdl/blob/master/example/iytdl_example.py)\n',
    'author': 'Leorio Paradinight',
    'author_email': '62891774+code-rgb@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iytdl/iytdl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
