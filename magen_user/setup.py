# coding=utf-8
"""
Magen Core magen_gmail_client package setup
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
    name='magen_user',
    version=__version__,
    install_requires=[
        'aniso8601>=1.2.1',
        'coverage>=4.4.1',
        'flake8>=3.3.0',
        'pytest>=3.1.3',
        'Sphinx>=1.6.3',
        'wheel>=0.30.0a0',
        'httplib2>=0.10',
        'Flask>=0.12.2',
        'Flask-Cors>=3.0',
        'Flask-Login>=0.4.1',
        'Flask-WTF>=0.14.2',
        'itsdangerous>=0.24',
        'WTForms>=2.1',
        'pymongo>=3.4'
      ],
    scripts=['magen_user_api/user_api.py'],
    package_dir={'': '.'},
    packages={'magen_user_api', 'magen_user_api.templates', 'magen_user_api.static', 'magen_user_api.static.css'},
    include_package_data=True,
    package_data={
        # If any package contains *.txt, *.rst or *.html  files, include them:
        '': ['*.txt', '*.rst', '*.html', '*.css']
    },
    test_suite='tests',
    url='http://www.cisco.com',
    license='Apache',
    author='Alena Lifar',
    author_email='alifar@cisco.com',
    description='Magen Gmail Client Package',
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
        'Programming Language :: Python :: 3.6',
    ],
)
