FROM debian:buster
MAINTAINER Timothée Floure <timothee.floure@fnux.ch>

RUN apt-get update
RUN apt-get install -y wget kicad

COPY generate-html-bom.sh /usr/local/bin/
CMD /usr/local/bin/generate-html-bom.sh
