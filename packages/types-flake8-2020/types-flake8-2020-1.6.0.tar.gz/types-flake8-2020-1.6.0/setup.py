from setuptools import setup

name = "types-flake8-2020"
description = "Typing stubs for flake8-2020"
long_description = '''
## Typing stubs for flake8-2020

This is a PEP 561 type stub package for the `flake8-2020` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `flake8-2020`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/flake8-2020. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `53eae77983f67f9742af6e83f72f2b39343fdacf`.
'''.lstrip()

setup(name=name,
      version="1.6.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['flake8_2020-stubs'],
      package_data={'flake8_2020-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
