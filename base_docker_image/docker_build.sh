#!/usr/bin/env bash

echo "============== Building MAGEN BASE Docker Container =============="

path=`pwd`
MAGEN=`cd .. && pwd`

cd ${MAGEN}

requirements_filename=magen_requirements.txt

number_of_packages=8

# names of folders where magen packages are stored
folders=(magen_logaru magen_utils magen_datastore magen_rest magen_stats magen_mongo magen_id_client magen_gmail_client)
# names of magen packages
packages=(magen_logger magen_utils magen_datastore magen_rest_service magen_statistics_service magen_mongo magen_id_client magen_gmail_client)

for ((i=0; i<${number_of_packages}; i++))
do
    echo "Copying [${folders[i]}] to docker folder"
    # cd to package folder and get package version
    cd ${MAGEN}/${folders[i]}
    package_version=`python3 -c 'import __init__ as version; print(version.__version__)'`
    wheel_file=${packages[i]}-${package_version}-py3-none-any.whl
    # Creating requirements file with correct versions
    [ ${i} -eq 0 ] && echo ${wheel_file} > ${path}/${requirements_filename} || echo ${wheel_file} >> ${path}/${requirements_filename}
    # creating a path to wheel file, ex: magen_logaru/dist/magen_logger-1.0a1-py3-none-any.whl
    wheel_path=${folders[i]}/dist/${wheel_file}
    # make sure we're in root of the project
    cd ${MAGEN}
    # copying wheel into docker folder
    cp ${wheel_path} ${path}
done
# cp pip.conf ${path}
cd ${path}
docker build -t magen_base:17.02 .
