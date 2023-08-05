from setuptools import setup

name = "types-humanfriendly"
description = "Typing stubs for humanfriendly"
long_description = '''
## Typing stubs for humanfriendly

This is a PEP 561 type stub package for the `humanfriendly` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `humanfriendly`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/humanfriendly. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `955a3e5d9d5a35382ad6d0c24985dcd27df8f7f6`.
'''.lstrip()

setup(name=name,
      version="9.2.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['humanfriendly-stubs'],
      package_data={'humanfriendly-stubs': ['decorators.pyi', 'deprecation.pyi', 'sphinx.pyi', 'testing.pyi', 'tables.pyi', 'prompts.pyi', 'cli.pyi', 'case.pyi', 'usage.pyi', 'compat.pyi', 'text.pyi', '__init__.pyi', 'terminal/html.pyi', 'terminal/spinners.pyi', 'terminal/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
