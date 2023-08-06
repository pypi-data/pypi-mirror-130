# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyautoinstall']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyautoinstall',
    'version': '0.0.1',
    'description': 'Magically install modules just by importing them!!',
    'long_description': '<h1 align=\'center\'>PyAutoInstall</h1>\n<h3 align=\'center\'>Magically install modules just by importing them!!</h3>\n<p align="center">\n  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src=\'https://img.shields.io/badge/MADE%20WITH-Python-red?style=for-the-badge\'/></a>\n  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src=\'https://img.shields.io/pypi/pyversions/pyautoinstall?style=for-the-badge\'/></a>\n  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src=\'https://img.shields.io/pypi/status/pyautoinstall?style=for-the-badge\'/></a>\n  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src=\'https://img.shields.io/pypi/l/pyautoinstall?style=for-the-badge\'/></a>\n  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src=\'https://img.shields.io/pypi/v/pyautoinstall?style=for-the-badge\'/></a>\n</p>\n\n## 📝 Description\nThis is a **Work-In-Progress** Library which will **change**\nyour way of installing packages **forever**.\n\n### 🤯 Disclaimer\n(This project is still in unstable planning stage)\n\n## 🔥 Getting Started\n- ### ⬇️ Installation\n  While it would be nice to install `pyautoinstall` just by importing it,\n  that just isn\'t the case.\n\n  - Via pip\n    ```\n    pip install pyautoinstall\n    ```\n  \n- ### ⚡ Usage\n  - Without pyautoinstall\n    ```python\n    >>> import requests\n    Traceback (most recent call last):\n      File "<stdin>", line 1, in <module>\n    ModuleNotFoundError: No module named \'requests\'\n    ```\n  - With it\n    ```python\n    >>> import pyautoinstall\n    >>> import requests\n    Should I install requests? (y/n) - y\n    Successfully installed requests!!\n    >>> requests.get(\'https://pypi.org/project/pyautoinstall/\')\n    <Response [200]>\n    ```',
    'author': 'Ajay Ratnam',
    'author_email': 'ajayratnam.satheesh@gmail.com',
    'maintainer': 'Ajay Ratnam',
    'maintainer_email': 'ajayratnam.satheesh@gmail.com',
    'url': 'https://github.com/ajratnam/pyautoinstall',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
