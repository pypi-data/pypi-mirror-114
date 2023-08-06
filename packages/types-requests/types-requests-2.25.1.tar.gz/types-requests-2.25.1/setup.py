from setuptools import setup

name = "types-requests"
description = "Typing stubs for requests"
long_description = '''
## Typing stubs for requests

This is a PEP 561 type stub package for the `requests` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `requests`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/requests. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `1e39a5899aa7311b71623e6283612d56e60a53b2`.
'''.lstrip()

setup(name=name,
      version="2.25.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['requests-stubs'],
      package_data={'requests-stubs': ['adapters.pyi', 'structures.pyi', '__init__.pyi', 'exceptions.pyi', 'auth.pyi', 'models.pyi', 'compat.pyi', 'utils.pyi', 'hooks.pyi', 'cookies.pyi', 'sessions.pyi', 'status_codes.pyi', 'api.pyi', 'packages/__init__.pyi', 'packages/urllib3/filepost.pyi', 'packages/urllib3/response.pyi', 'packages/urllib3/_collections.pyi', 'packages/urllib3/__init__.pyi', 'packages/urllib3/exceptions.pyi', 'packages/urllib3/connectionpool.pyi', 'packages/urllib3/poolmanager.pyi', 'packages/urllib3/connection.pyi', 'packages/urllib3/request.pyi', 'packages/urllib3/fields.pyi', 'packages/urllib3/packages/__init__.pyi', 'packages/urllib3/packages/ssl_match_hostname/_implementation.pyi', 'packages/urllib3/packages/ssl_match_hostname/__init__.pyi', 'packages/urllib3/util/timeout.pyi', 'packages/urllib3/util/response.pyi', 'packages/urllib3/util/retry.pyi', 'packages/urllib3/util/ssl_.pyi', 'packages/urllib3/util/__init__.pyi', 'packages/urllib3/util/url.pyi', 'packages/urllib3/util/connection.pyi', 'packages/urllib3/util/request.pyi', 'packages/urllib3/contrib/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
