FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive

ENV LC_CTYPE C.UTF-8

RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  git \
  automake \
  build-essential \
  curl \
  dpkg-sig \
  wget \
  gcc \
  make \
  python3-pip \
  python3-dev \
  gedit \
  vim \
  nano \
  && rm -rf /var/lib/apt/lists/*
