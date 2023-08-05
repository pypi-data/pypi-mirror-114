#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['loudify']

package_data = \
{'': ['*']}

install_requires = \
['flit_core>=2.2.0', 'coloredlogs', 'setuptools_scm', 'pyzmq']

entry_points = \
{'console_scripts': ['loudify-broker = loudify:main_broker',
                     'loudify-cli = loudify:main_cli',
                     'loudify-client = loudify:main_client',
                     'loudify-worker = loudify:main_worker']}

setup(name='loudify',
      version='0.0.post17',
      description='Initialisation module for loudify broker.',
      author='Martyn van Dijke',
      author_email='martijnvdijke600@gmail.com',
      url='https://github.com/martynvdijke/loudify',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
     )
