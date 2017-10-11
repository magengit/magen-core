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

ADD magen*.whl /tmp/
COPY magen_requirements.txt /tmp
RUN pip3 install -r magen_requirements.txt

# ADD pip.conf /etc
