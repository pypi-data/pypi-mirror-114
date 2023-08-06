# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clashgap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'clashgap',
    'version': '1.0.0',
    'description': 'A per-character diff/compression algorithm in python',
    'long_description': '# Clashgap\n\n[![Version](https://img.shields.io/pypi/v/clashgap?label=version)](https://pypi.org/project/clashgap)\n[![Downloads](https://static.pepy.tech/personalized-badge/clashgap?period=month&units=abbreviation&left_color=grey&right_color=blue&left_text=downloads/month)](https://pepy.tech/project/clashgap)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](http://makeapullrequest.com)\n[![Code Quality](https://img.shields.io/lgtm/grade/python/g/NioGreek/Clashgap.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/NioGreek/Clashgap/context:python)\n[![Tests Status](https://github.com/NioGreek/Clashgap/actions/workflows/test.yml/badge.svg)](https://github.com/NioGreek/Clashgap/actions)\n[![Build Status](https://github.com/NioGreek/Clashgap/actions/workflows/build.yml/badge.svg)](https://github.com/NioGreek/Clashgap/actions)\n[![Docs Status](https://readthedocs.org/projects/clashgap/badge/?version=latest)](https://clashgap.readthedocs.io/en/latest/)\n\nA per-character diff/compression algorithm implementation in python\n\n## How it works\n\nIn case if you have two strings:\n> "This is a sentence..." and "This is a word..."\n\nyou could "clash" both of them together and find their gap, to get an array loking something like:\n> \\["This is a", \\["sentence", "word"\\], "..."\\]\n\nAs you can the clashgap algorithm looks for collisions in the two strings to find the gap. The clashgaped string maybe used for compression or as the diff of the input strings\n',
    'author': 'NioGreek',
    'author_email': 'GreekNio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/clashgap/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
