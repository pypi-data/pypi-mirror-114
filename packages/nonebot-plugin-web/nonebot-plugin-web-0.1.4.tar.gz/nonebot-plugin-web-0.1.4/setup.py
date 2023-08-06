# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_web']

package_data = \
{'': ['*'],
 'nonebot_plugin_web': ['dist/*',
                        'dist/img/icons/*',
                        'dist/static/css/*',
                        'dist/static/fonts/*',
                        'dist/static/js/*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0-alpha.13,<3.0.0',
 'nonebot2>=2.0.0-alpha.13,<3.0.0',
 'python-socketio>=4.6.1,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-web',
    'version': '0.1.4',
    'description': 'A web monitor for nonebot2',
    'long_description': None,
    'author': 'abrahumlink',
    'author_email': '307887491@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
