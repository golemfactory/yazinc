FROM debian:jessie
RUN apt-get update && apt-get install -y wget
RUN mkdir /golem && mkdir /golem/work
WORKDIR /golem
RUN  wget https://github.com/matter-labs/zinc/releases/download/0.1.5/zinc-0.1.5-linux.tar.gz && tar --get --strip-components=1 -f zinc-0.1.5-linux.tar.gz
COPY prove.sh /golem
VOLUME /golem/input /golem/output