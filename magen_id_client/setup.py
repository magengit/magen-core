from setuptools import setup, find_packages

setup(
    name='magen_id_client',
    version='1.1a1',
    packages=find_packages(exclude=['tests*']),
    # packages=['container_test', 'ingestion_apis',
    #          'ingestion_server'],
    install_requires=[
        'flake8>=3.2.1',
        'pytest>=3.0.2',
        'requests>=2.13.0',
        'responses>=0.5.1',
        'Sphinx>=1.5.1',
        'wheel>=0.30.0a0',
        'magen_rest_service>=1.2a1',
    ],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst']
    },
    test_suite='tests',
    url='',
    license='',
    author='Mizanul Chowdhury',
    author_email='michowdh@cisco.com',
    description='Magen ID Client Package',
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
        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],
)
