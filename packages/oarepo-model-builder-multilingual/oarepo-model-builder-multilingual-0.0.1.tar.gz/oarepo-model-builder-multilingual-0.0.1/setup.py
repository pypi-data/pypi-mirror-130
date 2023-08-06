# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oarepo_model_builder_multilingual',
 'oarepo_model_builder_multilingual.property_preprocessors',
 'oarepo_model_builder_multilingual.schema']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'click>=7.1',
 'deepmerge>=0.3.0,<0.4.0',
 'isort>=5.10.1,<6.0.0',
 'jsonpointer>=2.2,<3.0',
 'langcodes>=3.3.0',
 'libcst>=0.3.19,<0.4.0',
 'marshmallow>=3.14.1,<4.0.0',
 'oarepo-model-builder>=0.9.2,<0.10.0',
 'tomlkit>=0.7.2,<0.8.0']

extras_require = \
{'json5': ['json5>=0.9.6,<0.10.0'], 'pyyaml': ['PyYAML>=6.0,<7.0']}

setup_kwargs = {
    'name': 'oarepo-model-builder-multilingual',
    'version': '0.0.1',
    'description': '',
    'long_description': '# OARepo model builder multilingual\n\n',
    'author': 'Alzbeta Pokorna',
    'author_email': 'alzbeta.pokorna@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
