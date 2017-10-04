# Magen-Core

[![Build Status](https://travis-ci.org/magengit/magen-core.svg?branch=master)](https://travis-ci.org/magengit/magen-core)
[![codecov](https://codecov.io/gh/magengit/magen-core/branch/master/graph/badge.svg)](https://codecov.io/gh/magengit/magen-core)
[![Code Health](https://landscape.io/github/magengit/magen-core/master/landscape.svg?style=flat)](https://landscape.io/github/magengit/magen-core/master)


This repo containes infrastructure Magen Packages.

Current List of Packages under **Magen-Core**:

| Package Name          | Python Wheel                                    |
| ---------------------:|:------------------------------------------------|
| magen_logaru          | magen_logger-1.0a1-py3-none-any.whl             |
| magen_utils           | magen_utils-1.0a1-py3-none-any.whl              |
| magen_test_utils      | magen_test_utils-1.0a1-py3-none-any.whl         |
| magen_datastore       | magen_datastore-1.0a1-py3-none-any.whl          |
| magen_rest            | magen_rest_service-1.2a1-py3-none-any.whl       |
| magen_stats           | magen_statistics_service-1.0a1-py3-none-any.whl |
| magen_mongo           | magen_mongo-1.0a1-py3-none-any.whl              |
| magen_id_client       | magen_id_client-1.1a1-py3-none-any.whl          |
 
 
For This Service there are available ```make``` commands. Makefile is located in a ```root``` directory. You can execute ```make``` targets only in a directory where Makefile is located.

Make Default Target: ```make default```. Here is the list of targets available for policy

```make
default:
        @echo 'Makefile for Magen Core'
        @echo
        @echo 'Usage:'
        @echo '	make clean    			       :Remove packages from system and pyc files'
        @echo '	make test     			       :Run the test suite'
        @echo '	make package  			       :Create Python wheel package'
        @echo '	make install  			       :Install Python wheel package'
        @echo '	make all      			       :clean->package->install'
        @echo '	make list     			       :List of All Magen Dependencies'
        @echo '	make build_base_docker 	:Build Base Docker Image and Current Image (Run if base image is outdated or gone)'
        @echo '	make clean_docker 		    :Stop and Remove Docker containers and unused images'
        @echo
```
Before running target ```make build_base_docker``` and ```make clean_docker``` make sure to have Docker Machine running

