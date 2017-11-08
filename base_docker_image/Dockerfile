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

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update && apt-get install -y python3.6 python3.6-dev

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
RUN update-alternatives --set python3 /usr/bin/python3.5

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py && pip install -U setuptools
RUN pip3 install --upgrade pip
RUN pip install --upgrade pip

RUN update-alternatives --set python3 /usr/bin/python3.6

RUN python3 get-pip.py && pip install -U setuptools && rm get-pip.py
RUN pip3 install --upgrade pip
RUN pip install --upgrade pip

WORKDIR /tmp

ADD magen*.whl /tmp/
COPY magen_requirements.txt /tmp
RUN pip3 install -r magen_requirements.txt

RUN update-alternatives --set python3 /usr/bin/python3.5
RUN pip3 install -r magen_requirements.txt

# ADD pip.conf /etc
