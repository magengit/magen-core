# coding=utf-8
"""
Magen Core magen-utils package setup
"""
from setuptools import setup, find_packages
import sys
import os
import pip

with open(os.path.join(os.path.dirname(__file__), '__init__.py')) as version_file:
    exec(version_file.read())

if sys.version_info < (3, 5, 2):
    sys.exit("Sorry, you need Python 3.5.2+")

pip_version = int(pip.__version__.replace(".", ""))
if pip_version < 901:
        sys.exit("Sorry, you need pip 9.0.1+")

setup(
    name='magen_utils',
    version=__version__,
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'aniso8601>=1.2.1',
        'coverage>=4.4.1',
        'flake8>=3.3.0',
        'Flask>=0.12.2',
        'Flask-Cors>=3.0.3',
        'ipaddress>=1.0.18',
        'netifaces>=0.10.6',
        'pytest>=3.1.3',
        'Sphinx>=1.6.3',
        'wheel>=0.30.0a0',
        'datadog>=0.16.0',
        'python-dateutil>=2.6'
      ],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst']
    },
    test_suite='tests',
    url='http://www.cisco.com',
    license='Apache',
    author='Reinaldo Penno',
    author_email='repenno@cisco.com',
    description='Magen Utils API Package',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Legal Industry',
        'Topic :: Security',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],
)
