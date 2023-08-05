"""
    Firefly III API Client

    This is the Python client for Firefly III API

    The version of the OpenAPI document: 1.5.4
    Contact: ms32035@gmail.com
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "Firefly III API Client"
VERSION = "1.5.4"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
  "urllib3 >= 1.25.3",
  "python-dateutil",
]

setup(
    name=NAME,
    version=VERSION,
    description="Firefly III API Client",
    author="Marcin Szymanski",
    author_email="ms32035@gmail.com",
    url="https://github.com/ms32035/firefly-iii-client",
    keywords=["OpenAPI", "OpenAPI-Generator", "Firefly III API Client"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="AGPLv3",
    long_description="""\
    This is the Python client for Firefly III API
    """
)
