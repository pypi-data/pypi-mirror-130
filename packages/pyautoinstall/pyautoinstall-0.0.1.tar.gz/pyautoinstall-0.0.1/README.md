<h1 align='center'>PyAutoInstall</h1>
<h3 align='center'>Magically install modules just by importing them!!</h3>
<p align="center">
  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src='https://img.shields.io/badge/MADE%20WITH-Python-red?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src='https://img.shields.io/pypi/pyversions/pyautoinstall?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src='https://img.shields.io/pypi/status/pyautoinstall?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src='https://img.shields.io/pypi/l/pyautoinstall?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/pyautoinstall/"><img src='https://img.shields.io/pypi/v/pyautoinstall?style=for-the-badge'/></a>
</p>

## 📝 Description
This is a **Work-In-Progress** Library which will **change**
your way of installing packages **forever**.

### 🤯 Disclaimer
(This project is still in unstable planning stage)

## 🔥 Getting Started
- ### ⬇️ Installation
  While it would be nice to install `pyautoinstall` just by importing it,
  that just isn't the case.

  - Via pip
    ```
    pip install pyautoinstall
    ```
  
- ### ⚡ Usage
  - Without pyautoinstall
    ```python
    >>> import requests
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ModuleNotFoundError: No module named 'requests'
    ```
  - With it
    ```python
    >>> import pyautoinstall
    >>> import requests
    Should I install requests? (y/n) - y
    Successfully installed requests!!
    >>> requests.get('https://pypi.org/project/pyautoinstall/')
    <Response [200]>
    ```