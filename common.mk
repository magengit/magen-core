MAKE=make
PYTEST=pytest
COVERAGE=coverage run -m
OS := $(shell uname)
PYTHON=python3
PIP :=pip3

MAGEN_HELPER=../lib/magen_helper


include $(MAGEN_HELPER)/make_common/package_common.mk
include $(MAGEN_HELPER)/make_common/docker_common.mk
include $(MAGEN_HELPER)/make_common/doc_common.mk

default: common_default

clean: common_clean

test: common_test

package: common_package

install: common_install

all: common_all

list: common_list

uninstall: common_uninstall

stop_docker: common_stop_docker

clean_docker: common_clean_docker

rm_docker: common_rm_docker

upload: common_upload

doc: common_doc_api common_doc

test_travis: common_test_travis

check: common_check
