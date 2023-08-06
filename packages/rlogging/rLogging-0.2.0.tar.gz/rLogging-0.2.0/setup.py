# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_rlogging', 'rlogging', 'rlogging.service']

package_data = \
{'': ['*']}

install_requires = \
['celery>=5.1.2,<6.0.0',
 'cleo>=0.8.1,<0.9.0',
 'daemons==1.3.2',
 'pyzmq==22.0.3',
 'redis>=3.5.3,<4.0.0',
 'zmq==0.0.0']

setup_kwargs = {
    'name': 'rlogging',
    'version': '0.2.0',
    'description': 'Модуль гибкого логирования python приложений',
    'long_description': '# rlogging\n\nМодуль для логирования приложений python',
    'author': 'rocshers',
    'author_email': 'prog.rocshers@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
