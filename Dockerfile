FROM ubuntu

ARG CACHEBUST=1 
ENTRYPOINT ["bash", "start.sh"]
ARG GAME_VER=1.16.1
ARG CORES=4
ARG RAM=2048
ARG PORT=25565
ARG SERVICE=minecraft
ARG HOME=/config
ARG TZ=America/New_York
# DONT TOUCH THIS ONE\/
# ENV AM_I_IN_A_DOCKER_CONTAINER Yes
# ENV GAME_VER=${GAME_VER}
# ENV CORES=${CORES}
# ENV RAM=${RAM}
# ENV PORT=${PORT}
# ENV SERVICE=${SERVICE}
# ENV HOME=${HOME}
# ENV TZ=${TZ}

WORKDIR /config/
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update 
RUN apt install git openjdk-8-jre-headless python3 python3-pip gcc -y
COPY init-server.py /config/init-server.py
RUN git clone https://github.com/Tiiffi/mcrcon 
WORKDIR /config/mcrcon
RUN make
RUN cp mcrcon /usr/bin/mcrcon
RUN chmod +x /usr/bin/mcrcon
RUN /usr/bin/mcrcon -v
WORKDIR /config/
RUN pip3 install click requests
RUN python3 init-server.py -v ${GAME_VER} -c ${CORES} -r ${RAM} -p ${PORT} -s ${SERVICE}
RUN touch /config/start.sh
RUN echo java -server -XX:ParallelGCThreads=${CORES} -Xms256M -Xmx${RAM}M -jar /config/spigot-${GAME_VER}.jar nogui > /config/start.sh
RUN chmod +x /config/start.sh
RUN java -jar BuildTools.jar --rev ${GAME_VER}

EXPOSE ${PORT}