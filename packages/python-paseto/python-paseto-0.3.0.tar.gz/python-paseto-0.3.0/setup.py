# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paseto', 'paseto.crypto', 'paseto.protocol']

package_data = \
{'': ['*']}

install_requires = \
['cython>=0.29.24,<0.30.0', 'pynacl>=1.4.0,<2.0.0', 'pysodium>=0.7.9,<0.8.0']

setup_kwargs = {
    'name': 'python-paseto',
    'version': '0.3.0',
    'description': 'Platform-Agnostic Security Tokens for Python',
    'long_description': '# python-paseto\nPlatform-Agnostic Security Tokens for Python\n\n[![Build Status](https://travis-ci.com/purificant/python-paseto.svg?branch=main)](https://travis-ci.com/purificant/python-paseto)\n[![test-workflow](https://github.com/purificant/python-paseto/actions/workflows/test.yaml/badge.svg)](https://github.com/purificant/python-paseto/actions/workflows/test.yaml)\n[![PyPI version](https://badge.fury.io/py/python-paseto.svg)](https://badge.fury.io/py/python-paseto)\n[![Coverage Status](https://coveralls.io/repos/github/purificant/python-paseto/badge.svg?branch=main)](https://coveralls.io/github/purificant/python-paseto?branch=main)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/purificant/python-paseto.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/purificant/python-paseto/context:python)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n# Installation\n\n```bash\npip install python-paseto\n```\n\n# Low level API\nImplements PASETO V2 encrypt / decrypt functions.\nLow level API is focuses on solid, high quality, production ready primitives\nas specified directly in the [PASETO](https://tools.ietf.org/html/draft-paragon-paseto-rfc-00) \nprotocol.\n\n# Example use\n```python\nfrom paseto.protocol.version2 import Version2\n\nmessage = b"foo" # your data\nkey = b"0" * 32  # encryption key\n\ntoken = Version2.encrypt(message, key)\nplain_text = Version2.decrypt(token, key)\n\nassert plain_text == message\nprint(f"token={token}")\nprint(f"plain_text={plain_text}")\nprint(f"message={message}")\n```\n### With optional footer\n```python\nfrom paseto.protocol.version2 import Version2\n\nmessage = b"foo" # your data\nkey = b"0" * 32  # encryption key\noptional_footer = b"sample_footer" # authenticated but not encrypted metadata\n\ntoken = Version2.encrypt(message, key, optional_footer)\nplain_text = Version2.decrypt(token, key, optional_footer)\n\nassert plain_text == message\nprint(f"token={token}")\nprint(f"plain_text={plain_text}")\nprint(f"message={message}")\n```\n\n# High level API\nIn the future a high level API will provide developer friendly access to low level API\nand support easy integration into other projects.\n\n# Development\nTypical dev workflow operations are automated in [Makefile](Makefile),\nincluding testing, linting, code quality checks, benchmarks and dev environment setup.\n\n# Contributing\nThis library is under active development and maintenance. For any feedback, questions,\ncomments or if you would like to request a feature, please raise an issue!\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/purificant/python-paseto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
