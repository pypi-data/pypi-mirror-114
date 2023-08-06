# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jayhawk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jayhawk',
    'version': '1.1.1',
    'description': 'An extensible server for the Spartan protocol.',
    'long_description': "# jayhawk\n\nAn extensible server for the [Spartan](https://portal.mozz.us/spartan/spartan.mozz.us/specification.gmi) protocol.\n\n## What's in a name?\n\nSpartan was named for Mozz's alma mater, Michigan State and their Fighting Spartans sports teams (in the tradition of Gopher, which was named after Minnesota's mascot). The college I'm going to be attending this fall has their sports teams all named Jayhawks, so Jayhawk fits the niche.\n",
    'author': 'Robert "khuxkm" Miles',
    'author_email': 'khuxkm+jayhawk@tilde.team',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MineRobber9000/jayhawk',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
