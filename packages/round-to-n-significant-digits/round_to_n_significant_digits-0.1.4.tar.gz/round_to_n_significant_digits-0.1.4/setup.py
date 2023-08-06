# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['round_to_n_significant_digits']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'round-to-n-significant-digits',
    'version': '0.1.4',
    'description': 'PYPI package with only 1 function to round float numbers',
    'long_description': '==============================\nround_to_n_significant_digits\n==============================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/round_to_n_significant_digits\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/round_to_n_significant_digits\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/round_to_n_significant_digits\n    :target: https://github.com/stas-prokopiev/round_to_n_significant_digits/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://readthedocs.org/projects/round_to_n_significant_digits/badge/?version=latest\n    :target: https://round_to_n_significant_digits.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://travis-ci.org/stas-prokopiev/round_to_n_significant_digits.svg?branch=master\n    :target: https://travis-ci.org/stas-prokopiev/round_to_n_significant_digits\n\n.. image:: https://img.shields.io/pypi/v/round_to_n_significant_digits\n   :target: https://img.shields.io/pypi/v/round_to_n_significant_digits\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/round_to_n_significant_digits\n   :target: https://img.shields.io/pypi/pyversions/round_to_n_significant_digits\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nOverview.\n=========================\nround_to_n_significant_digits is a one function PYPI package made only with one\ngoal to round float numbers in python to asked number of signifacant digits\n\n\n.. code-block:: python\n\n    import round_to_n_significant_digits\n\n    round_to_n_significant_digits.rtnsd(0.23234, 2)  # 0.23\n    round_to_n_significant_digits.rtnsd(0.235, 2)  # 0.24\n    round_to_n_significant_digits.rtnsd(105.3, 1)  # 105\n    round_to_n_significant_digits.rtnsd(105.3, 1)  # 100\n    round_to_n_significant_digits.rtnsd(125.3, 2)  # 130\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install round_to_n_significant_digits\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/round_to_n_significant_digits/>`_\n    * `readthedocs <https://round_to_n_significant_digits.readthedocs.io/en/latest/>`_\n    * `GitHub <https://github.com/stas-prokopiev/round_to_n_significant_digits>`_\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.\n',
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
