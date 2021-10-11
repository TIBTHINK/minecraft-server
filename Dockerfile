FROM Ubuntu

MAINTAINER Tibthink version: 1.0

RUN  apt update \
 apt install git openjdk-8-jre-headless python3 python3-pip sudo\
 adduser minecraft -d /home/minecraft -m -p password \
 usermod -a -G 
 su minecraft \


