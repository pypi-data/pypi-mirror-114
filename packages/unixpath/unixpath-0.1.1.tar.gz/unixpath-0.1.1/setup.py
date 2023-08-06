# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unixpath']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unixpath',
    'version': '0.1.1',
    'description': 'unix-style path processing functions',
    'long_description': '# unixpath\n\n> unix-style path processing functions\n\n\n## Why?\n\nMy goal was to provide `posixpath` path processing functions in pure Python (e.g. `normpath`, `join`, `split`, etc) *minus* any functions that rely on any kind of "filesystem" concept (`stat`, etc).\n\nBasically, this is a "minimum viable unix path processing framework." Path processing functions are useful for e.g. ML libraries that want to use unix-style paths to refer to model variables.\n\n(Honestly `unixpath` is kind of pointless. Its functions are copy-pasted from `posixpath`, so why not just `import posixpath` and not worry about the extra dependency on `unixpath`? Answer: because I was curious how Python implemented their unix path processing functions, so I made this library as a learning exercise.)\n\n\n## Install\n\n```\npython3 -m pip install -U unixpath\n```\n\n## Usage\n\n```py\nimport unixpath\nunixpath.join(\'a\', \'b\') # \'a/b\'\nunixpath.join(\'a\', \'b\', \'..\', \'c\') # \'a/b/../c\'\nunixpath.normpath(\'a/b/../c\') # \'a/c\'\n```\n\n## License\n\nMIT\n\n## Contact\n\nA library by [Shawn Presser](https://www.shawwn.com). If you found it useful, please consider [joining my patreon](https://www.patreon.com/shawwn)!\n\nMy Twitter DMs are always open; you should [send me one](https://twitter.com/theshawwn)! It\'s the best way to reach me, and I\'m always happy to hear from you.\n\n- Twitter: [@theshawwn](https://twitter.com/theshawwn)\n- Patreon: [https://www.patreon.com/shawwn](https://www.patreon.com/shawwn)\n- HN: [sillysaurusx](https://news.ycombinator.com/threads?id=sillysaurusx)\n- Website: [shawwn.com](https://www.shawwn.com)\n\n',
    'author': 'Shawn Presser',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shawwn/unixpath',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
