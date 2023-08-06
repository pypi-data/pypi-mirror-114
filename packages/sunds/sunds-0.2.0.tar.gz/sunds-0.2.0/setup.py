# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sunds',
 'sunds.core',
 'sunds.core.np_geometry',
 'sunds.core.tf_geometry',
 'sunds.datasets',
 'sunds.datasets.nerf_synthetic',
 'sunds.features',
 'sunds.tasks',
 'sunds.utils']

package_data = \
{'': ['*'],
 'sunds.datasets.nerf_synthetic': ['dummy_data/nerf_synthetic/lego/*',
                                   'dummy_data/nerf_synthetic/lego/test/*',
                                   'dummy_data/nerf_synthetic/lego/train/*',
                                   'dummy_data/nerf_synthetic/lego/val/*']}

install_requires = \
['absl', 'numpy>=1.17', 'tensorflow_datasets>=4.4', 'tqdm', 'typing_extensions']

setup_kwargs = {
    'name': 'sunds',
    'version': '0.2.0',
    'description': 'Datasets for scene understanding',
    'long_description': None,
    'author': 'Sunds team',
    'author_email': 'sunds@google.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/google-research/sunds',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
