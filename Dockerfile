# FROM oraclelinux:7-slim as build

# ENV GOPATH=/tmp/go
# ENV GOFILE=go1.14.4.linux-amd64.tar.gz
# ENV ORCHPATH=/usr/local

# RUN yum update -y && yum clean all

# RUN yum install -y \
#   libcurl \
#   rsync \
#   gcc \
#   gcc-c++ \
#   bash \
#   git \
#   wget \
#   which \
#   perl-Digest-SHA \
#   oracle-golang-release-el7 \
#   && yum clean all

# RUN yum install -y \
#   golang \
#   && yum clean all

# RUN mkdir -p $ORCHPATH
# WORKDIR $ORCHPATH

# RUN git clone https://github.com/github/orchestrator.git
# WORKDIR $ORCHPATH/orchestrator
# RUN ./script/build

# FROM oraclelinux:7-slim

# ENV PORT=3000
# ENV RAFT=true

# COPY --from=build /usr/local/orchestrator /usr/local/orchestrator

# WORKDIR /usr/local/orchestrator/bin
# COPY run/ .
# ADD docker/entrypoint.sh /entrypoint.sh
# CMD /entrypoint.sh


FROM debian:stable-slim as build

ENV GOPATH=/tmp/go
ENV GOFILE=go1.14.4.linux-amd64.tar.gz
ENV ORCHPATH=/usr/local

RUN apt-get update && apt-get install -y \
  libcurl4 \
  rsync \
  build-essential \
  bash \
  git \
  wget \
  perl \
  sudo \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p $ORCHPATH
WORKDIR $ORCHPATH

RUN git clone https://github.com/github/orchestrator.git
WORKDIR $ORCHPATH/orchestrator
RUN ./script/build

FROM debian:stable-slim

ENV PORT=3000
ENV RAFT=true

COPY --from=build /usr/local/orchestrator /usr/local/orchestrator

WORKDIR /usr/local/orchestrator/bin
COPY run/ .
ADD docker/entrypoint.sh /entrypoint.sh


RUN useradd -ms /bin/bash user && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/user

USER user 
CMD /entrypoint.sh