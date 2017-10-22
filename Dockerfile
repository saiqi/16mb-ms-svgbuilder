FROM saiqi/16mb-platform:latest

RUN apt-get install -y python3-lxml ; \
    pip3 install svgwrite marshmallow jsonpath-rw

RUN mkdir /service 

ADD application /service/application
ADD ./cluster.yml /service

WORKDIR /service
