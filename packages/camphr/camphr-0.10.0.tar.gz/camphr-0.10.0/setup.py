# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camphr',
 'camphr.ner_labels',
 'camphr.tokenizer',
 'camphr.tokenizer.juman',
 'camphr.tokenizer.mecab',
 'camphr.tokenizer.sentencepiece']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'dataclass-utils>=0.7.12,<0.8.0',
 'dataclasses>=0.6,<0.7',
 'pytextspan>=0.5.0,<1.0',
 'pytokenizations>=0.4.8,<1.0',
 'typing-extensions>=3.7.4']

extras_require = \
{'all': ['sentencepiece>=0.1.96,<0.2.0',
         'mojimoji>=0.0.11,<0.0.12',
         'pyknp>=0.4.2,<0.5',
         'mecab-python3>=1.0,<1.1'],
 'juman': ['mojimoji>=0.0.11,<0.0.12', 'pyknp>=0.4.2,<0.5'],
 'mecab': ['mecab-python3>=1.0,<1.1'],
 'sentencepiece': ['sentencepiece>=0.1.96,<0.2.0']}

entry_points = \
{'console_scripts': ['camphr = camphr.cli.__main__:main']}

setup_kwargs = {
    'name': 'camphr',
    'version': '0.10.0',
    'description': 'spaCy plugin for Transformers, Udify, Elmo, etc.',
    'long_description': '',
    'author': 'tamuhey',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PKSHATechnology-Research/camphr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
