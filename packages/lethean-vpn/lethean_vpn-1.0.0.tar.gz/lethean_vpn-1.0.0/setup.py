"""
    Lethean VPN

    Distributed Virtual Private Marketplace  # noqa: E501

    Contact: contact@lethean.io
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "lethean_vpn"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "urllib3 >= 1.25.3",
    "python-dateutil",
    "syslogmp",
    "ed25519",
    "cryptography",
    "psutil",
    "jsonpickle",
    "configargparse",
    "requests",
    "dnspython"
]

setup(
    name=NAME,
    version=VERSION,
    description="Lethean VPN",
    author="Lethean VPN",
    author_email="contact@lethean.io",
    url="https://lt.hn/en/docs/vpn",
    keywords=["vpn"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="GPLv3",
    long_description="""\
    Distributed Virtual Private Marketplace  # noqa: E501
    """
)
