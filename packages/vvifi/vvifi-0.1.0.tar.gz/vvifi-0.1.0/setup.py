# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vvifi']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'python-string-utils>=1.0.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['vvifi = vvifi.cli:main']}

setup_kwargs = {
    'name': 'vvifi',
    'version': '0.1.0',
    'description': 'A Python CLI to quickly check your Wi-Fi network password.',
    'long_description': '# vvifi\n\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA Python CLI to quickly check your Wi-Fi network password.\n\n## References\n\n- [Wi-Fi Wikipedia page](https://en.wikipedia.org/wiki/Wi-Fi)\n- Siddharth Dushantha\'s [wifi-password](https://github.com/sdushantha/wifi-password) CLI\n- Ankit Jain\'s [wifiPassword](https://github.com/ankitjain28may/wifiPassword) CLI\n\n## Quickstart\n\n```text\nUsage: vvifi [OPTIONS]\n\n  A Python CLI to quickly check your Wi-Fi network password. By default, the\n  network you are connected to is considered.\n\nOptions:\n  --networks          Show the names (SSIDs) of saved Wi-Fi networks and exit.\n  -n, --network NAME  The name (SSID) of a Wi-Fi network you have previously\n                      connected to.\n\n  --version           Show the version and exit.\n  --help              Show this message and exit.\n```\n\n## Development\n\n- `poetry install`\n- `poetry shell`\n\n## Tech Stack\n\n- [Click](https://click.palletsprojects.com/) (for the interface)\n- [python-string-utils](https://github.com/daveoncode/python-string-utils) (to remove multiline string indentation)\n\n### Packaging and Development\n\n- [Poetry](https://python-poetry.org/)\n- [Mypy](http://mypy-lang.org/)\n- [isort](https://pycqa.github.io/isort/)\n- [Black](https://github.com/psf/black)\n- [Flake8](https://flake8.pycqa.org/)\n  - [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)\n  - [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)\n  - [pep8-naming](https://github.com/PyCQA/pep8-naming)\n  - [flake8-builtins](https://github.com/gforcada/flake8-builtins)\n- [Bandit](https://bandit.readthedocs.io/)\n\nThis CLI was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`joaopalmeiro/cookiecutter-templates/python-cli`](https://github.com/joaopalmeiro/cookiecutter-templates) project template.\n\n## Notes\n\n- `python.pythonPath` (`settings.json` file) is deprecated. More info [here](https://devblogs.microsoft.com/python/python-in-visual-studio-code-may-2020-release/#coming-next-moving-python-pythonpath-out-of-settings-json), [here](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter), and [here](https://github.com/microsoft/vscode-python/issues/11015). Alternative ([source](https://github.com/microsoft/vscode-python/issues/12313#issuecomment-867932929)): `"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"`.\n- [`subprocess` module](https://docs.python.org/3.6/library/subprocess.html) (Python 3.6).\n- [`sys.platform` values](https://docs.python.org/3.6/library/sys.html#sys.platform).\n- `security find-generic-password -h`.\n- `/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -h` (more info [here](https://ss64.com/osx/airport.html)).\n- [Regular expression](https://github.com/python/cpython/blob/3.6/Lib/textwrap.py#L411) used by `textwrap.dedent()`.\n- Classifiers:\n  - `"Operating System :: MacOS"` + `"Operating System :: MacOS :: MacOS X"` ([macOS](https://en.wikipedia.org/wiki/MacOS)).\n  - [Mac OS 9](https://en.wikipedia.org/wiki/Mac_OS_9) was succeeded by Mac OS X.\n  - In the future, replace with `"Operating System :: OS Independent"`.\n- Click:\n  - [User Input Prompts](https://click.palletsprojects.com/en/7.x/prompts/): Click supports input and confirmation prompts.\n  - [Interactive User Prompts](https://github.com/pallets/click/issues/899) issue.\n- [PyInquirer](https://github.com/CITGuru/PyInquirer) and [inquirer](https://github.com/magmax/python-inquirer) packages.\n- Find the interface for the Wi-Fi network ([source](https://michaelsoolee.com/switch-wifi-macos-terminal/)): `networksetup -listallhardwareports`.\n- List [preferred Wi-Fi networks](https://support.apple.com/en-gb/guide/mac-help/mchlp1201/mac) ([source](https://osxdaily.com/2013/01/03/get-list-preferred-wifi-networks-command-line/)): `networksetup -listpreferredwirelessnetworks en0` (or `networksetup -listpreferredwirelessnetworks en1`). The wireless networks the computer has connected to are listed here.\n- [click-help-colors](https://github.com/click-contrib/click-help-colors) package.\n- Datadog\'s [mkdocs-click](https://github.com/DataDog/mkdocs-click) extension.\n\n### [python-string-utils](https://github.com/daveoncode/python-string-utils) implementation to remove indentation from multiline strings\n\n```python\nimport re\nfrom typing import Pattern\n\n# The second `^` is to match a character not present in the list.\nMARGIN_RE: Pattern[str] = re.compile(r"^[^\\S\\r\\n]+")\n\n\ndef strip_margin(input_string: str) -> str:\n    # ...\n    line_separator = "\\n"\n    lines = [MARGIN_RE.sub("", line) for line in input_string.split(line_separator)]\n    out = line_separator.join(lines)\n\n    return out\n```\n',
    'author': 'João Palmeiro',
    'author_email': 'joaommpalmeiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joaopalmeiro/vvifi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
