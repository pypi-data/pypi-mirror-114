# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['john_toolbox', 'john_toolbox.preprocessing', 'john_toolbox.utils']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=3.8.0,<4.0.0',
 'numpy>=1.19,<2.0',
 'pandas>=1.1,<2.0',
 'tqdm>=4.51,<5.0']

setup_kwargs = {
    'name': 'john-toolbox',
    'version': '0.4.9',
    'description': 'Wrapper for transformers scikit learn pipeline and wrapper for ml model',
    'long_description': '<h1 align="center">\n\nWelcome to john_toolbox 👋\n\n</h1>\n<p>\n<img alt="Version" src="https://img.shields.io/badge/version-0.4.9-blue.svg?cacheSeconds=2592000" />\n<a href="https://nguyenanht.github.io/john-toolbox/" target="_blank"><img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" /></a>\n<a href="https://github.com/nguyenanht/john-toolbox/graphs/commit-activity" target="_blank"><img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>\n<a href="None" target="_blank"><img alt="License:MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>\n\n</p>\n\n> This is my own toolbox for pipeline preprocessing Transformer and Pytorch model with callbacks.\n### 🏠 [Homepage](https://github.com/nguyenanht/john-toolbox)\n\n## Install\n```sh\npip install john-toolbox\n\n```\n\n\n\n## Author\n👤 **Johnathan Nguyen**\n\n\n* GitHub: [@nguyenanht](https://github.com/{github_username})\n\n## How to use ?\n\nIf you want examples. please refer to notebooks directory. It contains tutorials.\n\n\n\n\n## Show your support\nGive a ⭐️ if this project helped you!\n\n\n## Useful link\n\n#### how to publish new version in pypi with poetry ?\nhttps://johnfraney.ca/posts/2019/05/28/create-publish-python-package-poetry/\n\n#### how to create a new release ?\nhttps://www.atlassian.com/fr/git/tutorials/comparing-workflows/gitflow-workflow\n\n#### how to generate docs\nhttps://github.com/JamesALeedham/Sphinx-Autosummary-Recursion\n\n#### how to deploy with github actions\nhttps://blog.flozz.fr/2020/09/21/deployer-automatiquement-sur-github-pages-avec-github-actions/\n\n---\n_This README was created with the [markdown-readme-generator](https://github.com/pedroermarinho/markdown-readme-generator)_',
    'author': 'john',
    'author_email': 'contact@nguyenjohnathan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nguyenanht/john-toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
