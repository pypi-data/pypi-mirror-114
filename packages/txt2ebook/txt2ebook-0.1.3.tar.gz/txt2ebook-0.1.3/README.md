# txt2ebook

Console tool to convert txt file to different ebook format.

## Installation

From PyPI:

```
pip install txt2ebook
```

## Usage

Showing help message:

```bash
$ txt2ebook
Usage: txt2ebook [OPTIONS] FILENAME

  Console tool to convert txt file to different ebook format.

Options:
  -t, --title TEXT     Set the title of the ebook.
  -l, --language TEXT  Set the language of the ebook.  [default: en]
  -a, --author TEXT    Set the author of the ebook.
  -d, --debug          Enable debugging log.
  --version            Show the version and exit.
  --help               Show this message and exit.
```

Convert a txt file into epub:

```bash
txt2book ebook.txt
```

## Copyright and License

Copyright (C) 2021 Kian-Meng, Ang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
