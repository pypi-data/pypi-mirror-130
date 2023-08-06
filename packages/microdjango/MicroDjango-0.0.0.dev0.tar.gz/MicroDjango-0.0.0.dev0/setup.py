# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['microdjango']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0,<5.0']

setup_kwargs = {
    'name': 'microdjango',
    'version': '0.0.0.dev0',
    'description': 'Django on low-power devices',
    'long_description': '# `MicroDjango`: Django on low-power devices\n',
    'author': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'author_email': 'Edu.AI@STEAMforVietNam.org',
    'maintainer': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'maintainer_email': 'Edu.AI@STEAMforVietNam.org',
    'url': 'https://GitHub.com/Django-AI/MicroDjango',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
