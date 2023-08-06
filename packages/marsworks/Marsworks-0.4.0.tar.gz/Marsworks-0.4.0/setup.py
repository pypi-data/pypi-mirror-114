# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marsworks', 'marsworks.origin']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'marsworks',
    'version': '0.4.0',
    'description': "An Async. API Wrapper around NASA's Mars Rover Photos API written in Python.",
    'long_description': '<img src=https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia23378-16.jpg class="center">\n\n<p align="center">\n <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</p>\n\n\n# Welcome!\nMarsworks is a lightweight, Async. API wrapper around\n[Mars Rover Photos API](https://api.nasa.gov/) written in Python.\n\nCurrently this project is under development and possibilities of\nbreaking changes in near future is huge until 1.x release.\n\n# Getting Started\n\n## Installation:\n\n`pip install -U marsworks`\n\n## Usage:\n\n```py\n\n#Lets get images using sols.\nimport asyncio\nfrom marsworks import Client\n\nclient = Client()\nasync def main(rover_name, sol) -> list:\n    images = await client.get_photo_by_sol(rover_name, sol) #You can pass camera too.\n    return images\n\n\nimgs = asyncio.run(main("Curiosity", 956))\nprint(imgs[0].img_src)\nprint(imgs[0].photo_id)\n#and many more!\n```\n\n```py\n\n#Lets get some mission manifest.\nimport asyncio\nfrom marsworks import Client, Manifest\n\nclient = Client()\nasync def main(rover_name) -> Manifest:\n    mfest = await client.get_mission_manifest(rover_name)\n    return mfest\n\nmfst = asyncio.run(main("Spirit"))\nprint(mfst.landing_date)\nprint(mfst.status)\n#and more!\n```\n\n### Docs. can be found [here](https://novaemiya.github.io/Marsworks/)!\n\n### Thanks to [Andy](https://github.com/an-dyy) for his contribution.\n',
    'author': 'NovaEmiya',
    'author_email': 'importz750@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NovaEmiya/Marsworks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
