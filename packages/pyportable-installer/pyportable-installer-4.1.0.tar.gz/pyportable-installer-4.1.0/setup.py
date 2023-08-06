# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyportable_installer',
 'pyportable_installer.checkup',
 'pyportable_installer.compilers',
 'pyportable_installer.compilers.accessory',
 'pyportable_installer.compilers.accessory.pyportable_crypto_trial_python310.pyportable_crypto',
 'pyportable_installer.compilers.accessory.pyportable_crypto_trial_python38.pyportable_crypto',
 'pyportable_installer.compilers.accessory.pyportable_crypto_trial_python39.pyportable_crypto',
 'pyportable_installer.main_flow',
 'pyportable_installer.main_flow.step1',
 'pyportable_installer.main_flow.step2',
 'pyportable_installer.main_flow.step3',
 'pyportable_installer.main_flow.step3.step3_1',
 'pyportable_installer.main_flow.step3.step3_2',
 'pyportable_installer.main_flow.step3.step3_3',
 'pyportable_installer.main_flow.step3.step3_3.bat_2_exe',
 'pyportable_installer.main_flow.step4']

package_data = \
{'': ['*'], 'pyportable_installer': ['template/*', 'template/depsland/*']}

install_requires = \
['cython',
 'embed-python-manager',
 'fire',
 'lk-logger',
 'lk-utils',
 'pyarmor',
 'pyportable-crypto']

setup_kwargs = {
    'name': 'pyportable-installer',
    'version': '4.1.0',
    'description': 'Build and distribute portable Python application by all-in-one configuration file.',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
