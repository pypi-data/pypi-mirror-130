# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mesi']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata<4.3',
 'polyleven>=0.7,<0.8',
 'tabulate>=0.8.9,<0.9.0',
 'textdistance[extras]>=4.2.1,<5.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['mesi = mesi.main:mesi_cli']}

setup_kwargs = {
    'name': 'mesi',
    'version': '1.1.0',
    'description': 'Measure similarity in a many-to-many fashion',
    'long_description': "# Mesi\n\n[![Lint and Test](https://github.com/Michionlion/mesi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Michionlion/mesi/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/Michionlion/mesi/branch/main/graph/badge.svg?token=RdzwvXDrxp)](https://codecov.io/gh/Michionlion/mesi)\n[![PyPI](https://img.shields.io/pypi/v/mesi)](https://pypi.org/project/mesi)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/mesi)](https://pypi.org/project/mesi/#files)\n[![License](https://img.shields.io/github/license/Michionlion/mesi.svg)](https://github.com/Michionlion/mesi/blob/master/LICENSE)\n\n---\n\nMesi is a tool to measure the similarity in a many-to-many fashion of long-form\ndocuments like Python source code or technical writing. The output can be useful\nin determining which of a collection of files are the most similar to each\nother.\n\n## Installation\n\nPython 3.9+ and [pipx](https://pypa.github.io/pipx/) are recommended, although\nPython 3.6+ and/or [pip](https://pip.pypa.io/en/stable/) will also work.\n\n```bash\npipx install mesi\n```\n\nIf you'd like to test out Mesi before installing it, use the remote execution\nfeature of `pipx`, which will temporarily download Mesi and run it in an\nisolated virtual environment.\n\n```bash\npipx run mesi --help\n```\n\n## Usage\n\nFor a directory structure that looks like:\n\n```text\nprojects\n├── project-one\n│   ├── pyproject.toml\n│   ├── deliverables\n│   │   └── python_program.py\n│   └── README.md\n├── project-two\n│   ├── pyproject.toml\n│   ├── deliverables\n│   │   └── python_program.py\n│   └── README.md\n│\n```\n\nwhere similarity should be measured between each project's\n`deliverables/python_program.py` file, run the command:\n\n```bash\nmesi projects/*/deliverables/python_program.py\n```\n\nA lower distance in the produced table equates to a higher degree of similarity.\n\nSee the help menu (`mesi --help`) for additional options and configuration.\n\n### Algorithms\n\nThere are many algorithms to choose from when comparing string similarity! Mesi\nimplements all the\n[algorithms](https://github.com/life4/textdistance#algorithms) provided by\n[TextDistance](https://github.com/life4/textdistance). In general `levenshtein`\nis never a bad choice, which is why it is the default.\n\n### Table Formats\n\nMesi uses [tabulate](https://github.com/astanin/python-tabulate) for table\nformatting. The table format can be configured with the `--table-format` option\nto one of the formats\n[listed](https://github.com/astanin/python-tabulate#table-format) in tabulate's\ndocumentation.\n\n### Dependencies\n\nMesi uses two primary dependencies for text similarity calculation:\n[polyleven](https://github.com/fujimotos/polyleven), and\n[TextDistance](https://github.com/life4/textdistance). Polyleven is the default,\nas its singular implementation of [Levenshtein\ndistance](https://en.wikipedia.org/wiki/Levenshtein_distance) can be faster in\nmost situations. However, if a different edit distance algorithm is requested,\nTextDistance's implementations will be used.\n\n## Bugs/Requests\n\nPlease use the [GitHub issue\ntracker](https://github.com/Michionlion/mesi/issues) to submit bugs or request\nnew features, options, or algorithms.\n\n## License\n\nDistributed under the terms of the [GPL v3](LICENSE) license, mesi is free and\nopen source software.\n",
    'author': 'Saejin Mahlau-Heinert',
    'author_email': 'saejinmh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Michionlion/mesi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
