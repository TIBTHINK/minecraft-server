FROM ubuntu

ENTRYPOINT ["/bin/bash", "/config/minecraft-server/start.sh"]
ENV VERISON=1.16.1
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
RUN apt install git openjdk-8-jre-headless openjdk-8-jre-headless python3 python3-pip gcc systemctl wget -y
RUN git clone https://github.com/tibthink/minecraft-server 
RUN git clone https://github.com/Tiiffi/mcrcon 
WORKDIR /config/mcrcon
RUN make
RUN cp mcrcon /usr/bin/mcrcon
RUN chmod +x /usr/bin/mcrcon
RUN /usr/bin/mcrcon -v
WORKDIR /config/minecraft-server
RUN git pull
RUN pip3 install click requests
RUN python3 init-server.py -v ${VERISON} -c ${CORES} -r ${RAM} -p ${PORT} -s ${SERVICE}
RUN java -jar BuildTools.jar --rev ${VERISON}
RUN chmod +x /config/minecraft-server/start.sh
# RUN ufw allow 25565
# RUN ufw enable


EXPOSE ${PORT}