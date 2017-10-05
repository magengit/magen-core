FROM ubuntu:16.04
MAINTAINER Alena Lifar

# to get requirements to load properly
RUN apt-get update && \
    apt-get install -y \
                    apt-utils \
                    wget \
                    xz-utils \
                    build-essential \
                    libsqlite3-dev \
                    libreadline-dev \
                    libssl-dev \
                    libffi-dev \
                    openssl \
                    python3 \
                    python3-dev \
                    net-tools \
                    git \
                    libxml2-dev \
                    libxmlsec1-dev \
                    libxmlsec1-openssl \
                    libxslt-dev \
                    zlib1g-dev

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py && pip install -U setuptools && rm get-pip.py
RUN pip3 install --upgrade pip
RUN pip install --upgrade pip

WORKDIR /tmp

ADD magen_logger-1.0a1-py3-none-any.whl /tmp
RUN pip3 install /tmp/magen_logger-1.0a1-py3-none-any.whl

ADD magen_datastore-1.0a1-py3-none-any.whl /tmp
RUN pip3 install /tmp/magen_datastore-1.0a1-py3-none-any.whl

ADD magen_utils-1.1a2-py3-none-any.whl /tmp
RUN pip3 install /tmp/magen_utils-1.1a2-py3-none-any.whl

ADD magen_mongo-1.0a1-py3-none-any.whl /tmp
RUN pip3 install /tmp/magen_mongo-1.0a1-py3-none-any.whl

ADD magen_rest_service-1.2a2-py3-none-any.whl /tmp
RUN pip3 install /tmp/magen_rest_service-1.2a2-py3-none-any.whl

ADD magen_statistics_service-1.0a1-py3-none-any.whl /tmp
RUN pip3 install /tmp/magen_statistics_service-1.0a1-py3-none-any.whl

ADD magen_id_client-1.1a1-py3-none-any.whl /tmp
RUN pip3 install /tmp/magen_id_client-1.1a1-py3-none-any.whl

# ADD pip.conf /etc
