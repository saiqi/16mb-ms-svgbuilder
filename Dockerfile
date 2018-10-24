FROM saiqi/16mb-platform:latest

RUN pip3 install jsonpath-rw lxml

RUN mkdir /service 

ADD application /service/application
ADD ./cluster.yml /service

WORKDIR /service
