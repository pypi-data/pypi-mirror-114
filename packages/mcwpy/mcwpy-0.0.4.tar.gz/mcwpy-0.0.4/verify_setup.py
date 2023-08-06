# -*- coding: utf-8 -*-
from datetime import date
from _version import __version__
import requests


class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def version_to_tuple(version:str) -> tuple:
    return tuple(map(int, version.split('.')))


try:
    data = requests.get('https://pypi.org/pypi/mcwpy/json').json()

    # Verify that the version is the latest
    assert version_to_tuple(data['info']['version']) < version_to_tuple(__version__)
except:
    print(f'{bcolors.FAIL}Unable to resolve latest release version.{bcolors.ENDC}')
    quit()
else:
    print(f'{bcolors.OKGREEN}Latest release version: {data["info"]["version"]}, new version: {__version__}.{bcolors.ENDC}')
del requests

# Verify that the CHANGELOG is up to date
try:
    with open('CHANGELOG.md') as f:
        assert f"# {__version__} ({str(date.today()).replace('-', '/')})" in f.read()
except:
    print(f'{bcolors.FAIL}Unable to read CHANGELOG.md.{bcolors.ENDC}')
    quit()
else:
    print(f'{bcolors.OKGREEN}CHANGELOG.md is up to date.{bcolors.ENDC}')
del date

print(f'{bcolors.OKGREEN}Setup check passed.{bcolors.ENDC}')
