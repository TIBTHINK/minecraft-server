FROM ubuntu

ENV VERISON=1.17.1
ENV CORES=4
ENV RAM=2048
ENV PORT=25565
ENV SERVICE=minecraft
ENV HOME=/config
ENV AM_I_IN_A_DOCKER_CONTAINER Yes
MAINTAINER Tibthink version: 1.0

WORKDIR /
RUN  apt update 
RUN apt install git openjdk-8-jre-headless python3 python3-pip sudo -y
RUN useradd -r -m -U -d /opt/minecraft/ -s /bin/bash minecraft
RUN su minecraft 
WORKDIR /opt/minecraft/
RUN git clone https://github.com/tibthink/minecraft-server 
WORKDIR /opt/minecraft/minecraft-server/
RUN pip3 install click requests
RUN python3 init-server.py -v ${VERISON} -c ${CORES} -r ${RAM} -p ${PORT} -s ${SERVICE}
RUN chmod 777 /opt/minecraft/minecraft-server/spigot-$VERISON.jar
CMD java -server -XX:ParallelGCThreads=$CORES -Xms256M -Xmx$RAMM -jar /opt/minecraft/minecraft-server/spigot-$VERISON.jar nogui 

# RUN bash start.sh

EXPOSE ${PORT}