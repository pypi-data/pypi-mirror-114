# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['attractors', 'attractors.data', 'attractors.utils']

package_data = \
{'': ['*']}

extras_require = \
{':extra == "doc"': ['matplotlib>=3.4.2,<4.0.0',
                     'tqdm>=4.61.2,<5.0.0',
                     'pathos>=0.2.8,<0.3.0',
                     'more-itertools>=8.8.0,<9.0.0']}

entry_points = \
{'console_scripts': ['attractors = attractors.parser:cli']}

setup_kwargs = {
    'name': 'attractors',
    'version': '1.4.1',
    'description': 'Simulation and visualization of strange attractors',
    'long_description': "attractors\n==========\n\n|Build status| |Docs status| |PyPI version| |PyPI license| |CodeCov|\n\nattractors is a package for simulation and visualization of strange\nattractors.\n\nInstallation\n============\n\nThe simplest way to install the module is via PyPi using pip\n\n``pip install attractors``\n\nAlternatively, the package can be installed via github as follows\n\n::\n\n   git clone https://github.com/Vignesh-Desmond/attractors\n   cd attractors\n   python -m pip install .\n\nTo set up the package for development and debugging, it is recommended\nto use `Poetry <https://python-poetry.org/>`__. Just install with\n``poetry install`` and let Poetry manage the environment and\ndependencies.\n\nPrerequisites\n-------------\n\nTo generate video output, the package uses\n`ffmpeg <https://ffmpeg.org/>`__. Download and install from\n`here <https://ffmpeg.org/download.html>`__ according to your os and\ndistribution and set PATH accordingly. Note that this is only required\nfor generating video output.\n\nUsage\n=====\n\nSee\n`documentation <https://attractors.readthedocs.io/en/latest/>`__\non readthedocs.io\n\nChangelog\n=========\n\nSee\n`changelog <https://github.com/Vignesh-Desmond/attractors/blob/main/CHANGELOG.md>`__\nfor previous versions\n\nDevelopment\n===========\n\nThis package is under early stages of development it's open to any constructive suggestions. \nPlease send bug reports and feature requests through issue trackers and pull requests.\n\nLicense\n=======\n\nThis package is licensed under the `MIT\nLicense <https://github.com/Vignesh-Desmond/attractors/blob/main/LICENSE>`__\n\n.. |Build status| image:: https://img.shields.io/github/workflow/status/Vignesh-Desmond/attractors/Build?style=flat-square&logo=GitHub\n   :target: https://github.com/Vignesh-Desmond/attractors/actions/workflows/build.yml\n.. |PyPI version| image:: https://img.shields.io/pypi/v/attractors?color=blue&style=flat-square\n   :target: https://pypi.python.org/pypi/attractors/\n.. |PyPI license| image:: https://img.shields.io/pypi/l/attractors?style=flat-square&color=orange\n   :target: https://lbesson.mit-license.org/\n.. |CodeCov| image:: https://codecov.io/gh/Vignesh-Desmond/attractors/branch/main/graph/badge.svg?token=2VKMZ5EYVS\n   :target: https://codecov.io/gh/Vignesh-Desmond/attractors\n.. |Docs status| image:: https://img.shields.io/readthedocs/attractors?style=flat-square\n   :target: https://attractors.readthedocs.io/en/latest/",
    'author': 'Vignesh Mohan',
    'author_email': 'vignesh.desmond@gmail.com',
    'maintainer': 'Vignesh Mohan',
    'maintainer_email': 'vignesh.desmond@gmail.com',
    'url': 'https://github.com/Vignesh-Desmond/attractors',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
