FROM saiqi/16mb-platform:latest

RUN pip3 install svgwrite marshmallow

RUN mkdir /service 

ADD application /service/application
ADD ./cluster.yml /service

WORKDIR /service
