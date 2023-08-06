from setuptools import setup

name = "types-flake8-plugin-utils"
description = "Typing stubs for flake8-plugin-utils"
long_description = '''
## Typing stubs for flake8-plugin-utils

This is a PEP 561 type stub package for the `flake8-plugin-utils` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `flake8-plugin-utils`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/flake8-plugin-utils. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `88c8a5829e0e9735570cc2f69e39a5a27d0db4bf`.
'''.lstrip()

setup(name=name,
      version="1.3.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['flake8_plugin_utils-stubs'],
      package_data={'flake8_plugin_utils-stubs': ['__init__.pyi', 'plugin.pyi', 'utils/__init__.pyi', 'utils/assertions.pyi', 'utils/constants.pyi', 'utils/equiv_nodes.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
