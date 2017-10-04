#!/usr/bin/env bash

echo "============== Building MAGEN BASE Docker Container =============="

path=`pwd`
MAGEN=`cd .. && pwd`

cd ${MAGEN}

cp magen_logaru/dist/magen_logger-1.0a1-py3-none-any.whl ${path}
cp magen_utils/dist/magen_utils-1.0a1-py3-none-any.whl ${path}
cp magen_test_utils/dist/magen_test_utils-1.0a1-py3-none-any.whl ${path}
cp magen_datastore/dist/magen_datastore-1.0a1-py3-none-any.whl ${path}
cp magen_rest/dist/magen_rest_service-1.2a1-py3-none-any.whl ${path}
cp magen_stats/dist/magen_statistics_service-1.0a1-py3-none-any.whl ${path}
cp magen_mongo/dist/magen_mongo-1.0a1-py3-none-any.whl ${path}
cp magen_id_client/dist/magen_id_client-1.0a1-py3-none-any.whl ${path}
# cp pip.conf ${path}

cd ${path}

docker build -t magen_base:17.02 .
