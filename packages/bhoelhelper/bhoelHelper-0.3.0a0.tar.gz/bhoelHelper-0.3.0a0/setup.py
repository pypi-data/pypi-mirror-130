# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel', 'berhoel.helper', 'berhoel.helper.test']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.3"': ['backports.functools-lru-cache>=1.6.1,<2.0.0'],
 ':python_version < "3.4"': ['pathlib2>=2.3.5,<3.0.0']}

setup_kwargs = {
    'name': 'bhoelhelper',
    'version': '0.3.0a0',
    'description': 'Misc helper functionalities.',
    'long_description': '# Berthold Höllmann\'s bhoelHelper module #\n\nSome helper modules used in my other modules. \n\n## Description ##\n\n  \'check_args.py\' -- \'CheckArgs\' is used to process parameters for\n\tfunctions and class methods. It handels \'*data\' and\n\t\'**keyword\' arguments.\n\n  \'machar.py\' -- \'machar\' is a python implementation of the machar\n\troutine from "Numerical recipes in C". It determines and makes\n\tavaible the machine specific parameters affecting floating\n\tpoint arithmetic.\n\n# Installation #\n\npip install bhoelHelper\n\n## Documentation ##\n=============\n\n  Only avaible documentations are the generated documentation. I used\n  "HappyDoc":http://sourceforge.net/projects/happydoc/ to generate\n  documentation in directory doc.\n\n  Send me a "email", mailto:bhoel@starship.python.net if you like\n  this, or have any comments.\n',
    'author': 'Berthold Höllmann',
    'author_email': 'berthold-gitlab@xn--hllmanns-n4a.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
