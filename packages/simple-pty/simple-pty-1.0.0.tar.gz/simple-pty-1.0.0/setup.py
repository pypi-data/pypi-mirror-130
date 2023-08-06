# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spty']
setup_kwargs = {
    'name': 'simple-pty',
    'version': '1.0.0',
    'description': 'A utils for easily spawning interactive pty, which listening some signal like `signal.SIGWINCH`',
    'long_description': '# simple-pty - Yet another Pseudo terminal utils implement by python.\n\nsimple-pty is utils for easily spawning interactive pty, which listening some signal like `signal.SIGWINCH`\n\nWorks for Python 3.6+, Linux and macOS.\n\n## Usage\n\n### Install\nYou can install from PyPi.\n\n```bash\n❯ pip install simple-pty\n```',
    'author': 'shabbywu',
    'author_email': 'shabbywu@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shabbywu/simple-pty',
    'py_modules': modules,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
