MAKE=make
export BASE_IMAGE=base_docker_image
export DOCKER_SRC_TAG=magen_base:17.02
export DOCKER_IMAGE=magen-core
DOCKER_DIR=base_docker_image

PACKAGES = magen_id_client magen_logaru magen_utils magen_rest magen_stats magen_datastore magen_mongo magen_gmail_client

MAGEN_HELPER=lib/magen_helper

include $(MAGEN_HELPER)/make_common/package_common.mk
include $(MAGEN_HELPER)/make_common/docker_common.mk

define mongo_test

    mongo --eval "db.stats()" || (echo "mongodb not running $$?"; exit 1)

endef

default:
	@echo 'Makefile for Magen Core'
	@echo
	@echo 'Usage:'
	@echo '	make clean    			:Remove packages from system and pyc files'
	@echo '	make test     			:Run the test suite'
	@echo '	make package  			:Create Python wheel package'
	@echo '	make install  			:Install Python wheel package'
	@echo '	make all      			:clean->package->install'
	@echo '	make list     			:List of All Magen Dependencies'
	@echo '	make build_base_docker 	:Build Base Docker Image and Current Image (Run if base image is outdated or gone)'
	@echo '	make clean_docker 		:Stop and Remove Docker containers and unused images'
	@echo

update: common_update

mongo_running:
	$(call mongo_test)

stop_docker: common_stop_docker

clean_docker: common_clean_docker

rm_docker: common_rm_docker

doc:
	$(MAKE) -C magen_rest doc
	$(MAKE) -C magen_datastore doc
	$(MAKE) -C magen_mongo doc
	$(MAKE) -C magen_stats doc
	$(MAKE) -C magen_utils doc
	$(MAKE) -C magen_test_utils doc
	$(MAKE) -C magen_id_client doc
	$(MAKE) -C magen_gmail_client doc

test: start_mongo
	$(MAKE) mongo_running
	$(MAKE) -C magen_rest test
	$(MAKE) -C magen_mongo test
	$(MAKE) -C magen_stats test
	$(MAKE) -C magen_utils test
	$(MAKE) -C magen_id_client test
	$(MAKE) -C magen_gmail_client test

upload:
	$(foreach module, $(PACKAGES), $(MAKE) -C $(module) upload;)

install:
	$(foreach module, $(PACKAGES), $(MAKE) -C $(module) install;)
	$(MAKE) list

uninstall:
	$(foreach module, $(PACKAGES), $(MAKE) -C $(module) uninstall;)

package:
	$(foreach module, $(PACKAGES), $(MAKE) -C $(module) package;)

clean:
	$(foreach module, $(PACKAGES), $(MAKE) -C $(module) clean;)
	$(MAKE) list

check:
	$(foreach module, $(PACKAGES), $(MAKE) -C $(module) check;)

all:
	$(MAKE) clean
	$(MAKE) uninstall
	$(MAKE) package
	$(MAKE) install

list: common_list

build_base_docker: clean_docker
	$(MAKE) kill_mongo
	$(MAKE) clean
	$(MAKE) package
	$(MAKE) -C $(BASE_IMAGE) build_docker
	@$(CLEAN_DOCKER)
	@rm -f base_docker_image/*.whl
	@rm -f base_docker_image/pip.conf
