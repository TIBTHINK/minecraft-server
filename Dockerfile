FROM ubuntu

ENV VERISON=1.17.1
ENV CORES=4
ENV RAM=2048
ENV PORT=25565
ENV SERVICE=minecraft
ENV HOME=/config
ENV TZ=America/New_York
# DONT TOUCH THIS ONE\/
ENV AM_I_IN_A_DOCKER_CONTAINER Yes

WORKDIR /config

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update 
RUN apt install git openjdk-11-jre-headless python3 python3-pip -y
RUN git clone https://github.com/tibthink/minecraft-server 
WORKDIR /config/minecraft-server
RUN pip3 install click requests
# RUN python3 init-server.py -v ${VERISON} -c ${CORES} -r ${RAM} -p ${PORT} -s ${SERVICE}
# CMD java -server -XX:ParallelGCThreads=${CORES} -Xms256M -Xmx${RAM}M -jar /config/minecraft-server/spigot-${VERISON}.jar nogui 

# RUN bash start.sh

EXPOSE ${PORT}