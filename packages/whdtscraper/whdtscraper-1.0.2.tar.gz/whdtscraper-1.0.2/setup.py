# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whdtscraper']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'whdtscraper',
    'version': '1.0.2',
    'description': 'Wikimedia history dump tsv scraper, a module that scrapes the site and returns to you the available content.',
    'long_description': '# wikimedia-history-dump-tsv-screaper\nA project that scrapes the wikimedia history dump site in order to retrieve the available tsv to download\n',
    'author': 'Eugenio Berretta',
    'author_email': 'euberdeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/euberdeveloper/wikimedia-history-dump-tsv#pip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
