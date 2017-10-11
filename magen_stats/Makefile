wheel_version := $(shell python3 -c 'import __init__ as version; print(version.__version__)')
WHEEL := magen_statistics_service-$(wheel_version)-py3-none-any.whl
PACKAGE_NAME = magen_statistics_service
SPHINX_DIR = docs

DOC_PACKAGES = magen_statistics_api magen_statistics_server tests

include ../common.mk
