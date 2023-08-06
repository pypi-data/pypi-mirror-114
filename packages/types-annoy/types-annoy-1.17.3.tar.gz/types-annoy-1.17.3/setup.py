from setuptools import setup

name = "types-annoy"
description = "Typing stubs for annoy"
long_description = '''
## Typing stubs for annoy

This is a PEP 561 type stub package for the `annoy` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `annoy`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/annoy. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `7c37d6117d0141c3cabd2880e160410308f4c060`.
'''.lstrip()

setup(name=name,
      version="1.17.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['annoy-stubs'],
      package_data={'annoy-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
