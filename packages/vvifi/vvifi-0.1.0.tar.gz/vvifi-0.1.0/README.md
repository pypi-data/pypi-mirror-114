# vvifi

[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python CLI to quickly check your Wi-Fi network password.

## References

- [Wi-Fi Wikipedia page](https://en.wikipedia.org/wiki/Wi-Fi)
- Siddharth Dushantha's [wifi-password](https://github.com/sdushantha/wifi-password) CLI
- Ankit Jain's [wifiPassword](https://github.com/ankitjain28may/wifiPassword) CLI

## Quickstart

```text
Usage: vvifi [OPTIONS]

  A Python CLI to quickly check your Wi-Fi network password. By default, the
  network you are connected to is considered.

Options:
  --networks          Show the names (SSIDs) of saved Wi-Fi networks and exit.
  -n, --network NAME  The name (SSID) of a Wi-Fi network you have previously
                      connected to.

  --version           Show the version and exit.
  --help              Show this message and exit.
```

## Development

- `poetry install`
- `poetry shell`

## Tech Stack

- [Click](https://click.palletsprojects.com/) (for the interface)
- [python-string-utils](https://github.com/daveoncode/python-string-utils) (to remove multiline string indentation)

### Packaging and Development

- [Poetry](https://python-poetry.org/)
- [Mypy](http://mypy-lang.org/)
- [isort](https://pycqa.github.io/isort/)
- [Black](https://github.com/psf/black)
- [Flake8](https://flake8.pycqa.org/)
  - [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)
  - [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)
  - [pep8-naming](https://github.com/PyCQA/pep8-naming)
  - [flake8-builtins](https://github.com/gforcada/flake8-builtins)
- [Bandit](https://bandit.readthedocs.io/)

This CLI was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`joaopalmeiro/cookiecutter-templates/python-cli`](https://github.com/joaopalmeiro/cookiecutter-templates) project template.

## Notes

- `python.pythonPath` (`settings.json` file) is deprecated. More info [here](https://devblogs.microsoft.com/python/python-in-visual-studio-code-may-2020-release/#coming-next-moving-python-pythonpath-out-of-settings-json), [here](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter), and [here](https://github.com/microsoft/vscode-python/issues/11015). Alternative ([source](https://github.com/microsoft/vscode-python/issues/12313#issuecomment-867932929)): `"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"`.
- [`subprocess` module](https://docs.python.org/3.6/library/subprocess.html) (Python 3.6).
- [`sys.platform` values](https://docs.python.org/3.6/library/sys.html#sys.platform).
- `security find-generic-password -h`.
- `/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -h` (more info [here](https://ss64.com/osx/airport.html)).
- [Regular expression](https://github.com/python/cpython/blob/3.6/Lib/textwrap.py#L411) used by `textwrap.dedent()`.
- Classifiers:
  - `"Operating System :: MacOS"` + `"Operating System :: MacOS :: MacOS X"` ([macOS](https://en.wikipedia.org/wiki/MacOS)).
  - [Mac OS 9](https://en.wikipedia.org/wiki/Mac_OS_9) was succeeded by Mac OS X.
  - In the future, replace with `"Operating System :: OS Independent"`.
- Click:
  - [User Input Prompts](https://click.palletsprojects.com/en/7.x/prompts/): Click supports input and confirmation prompts.
  - [Interactive User Prompts](https://github.com/pallets/click/issues/899) issue.
- [PyInquirer](https://github.com/CITGuru/PyInquirer) and [inquirer](https://github.com/magmax/python-inquirer) packages.
- Find the interface for the Wi-Fi network ([source](https://michaelsoolee.com/switch-wifi-macos-terminal/)): `networksetup -listallhardwareports`.
- List [preferred Wi-Fi networks](https://support.apple.com/en-gb/guide/mac-help/mchlp1201/mac) ([source](https://osxdaily.com/2013/01/03/get-list-preferred-wifi-networks-command-line/)): `networksetup -listpreferredwirelessnetworks en0` (or `networksetup -listpreferredwirelessnetworks en1`). The wireless networks the computer has connected to are listed here.
- [click-help-colors](https://github.com/click-contrib/click-help-colors) package.
- Datadog's [mkdocs-click](https://github.com/DataDog/mkdocs-click) extension.

### [python-string-utils](https://github.com/daveoncode/python-string-utils) implementation to remove indentation from multiline strings

```python
import re
from typing import Pattern

# The second `^` is to match a character not present in the list.
MARGIN_RE: Pattern[str] = re.compile(r"^[^\S\r\n]+")


def strip_margin(input_string: str) -> str:
    # ...
    line_separator = "\n"
    lines = [MARGIN_RE.sub("", line) for line in input_string.split(line_separator)]
    out = line_separator.join(lines)

    return out
```
