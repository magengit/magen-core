wheel_version := $(shell python3 -c 'import __init__ as version; print(version.__version__)')
PACKAGE_NAME = magen_rest_service
WHEEL := $(PACKAGE_NAME)-$(wheel_version)-py3-none-any.whl
SPHINX_DIR = docs

DOC_PACKAGES = magen_rest_apis tests

include ../common.mk