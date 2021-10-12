FROM Ubuntu

ENV VERISON=1.17.1
ENV CORES=4
ENV RAM=2048
ENV PORT=25565
ENV SERVICE=minecraft
ENV HOME=/config

MAINTAINER Tibthink version: 1.0

RUN  apt update \
 apt install git openjdk-8-jre-headless python3 python3-pip sudo\
 adduser minecraft -d /home/minecraft -m -p password \
 usermod -a -G 
RUN su minecraft \
    git clone https://github.com/tibthink/minecraft-server . \
    pip3 install -r requirements.txt \
    python3 init-server.py -v ${VERISON} -c ${CORES} -r ${RAM} -p ${PORT} -s ${SERVICE} \
    bash start.sh

EXPOSE ${PORT}