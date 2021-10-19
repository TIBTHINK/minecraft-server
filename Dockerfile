FROM ubuntu

ARG CACHEBUST=1 
ENTRYPOINT ["bash", "/config/start.sh"]
ENV V=1.16.1
ENV CORES=4
ENV RAM=2048
ENV PORT=25565
ENV SERVICE=minecraft
ENV HOME=/config
ENV TZ=America/New_York
# DONT TOUCH THIS ONE\/
ENV AM_I_IN_A_DOCKER_CONTAINER Yes

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
RUN python3 init-server.py -v ${V} -c ${CORES} -r ${RAM} -p ${PORT} -s ${SERVICE}
RUN echo java -server -XX:ParallelGCThreads=${CORES} -Xms256M -Xmx${RAM}M -jar /config/spigot-${V}.jar nogui > /config/start.sh
RUN java -jar BuildTools.jar --rev ${V}
RUN chmod +x /config/start.sh
# RUN iptables -A INPUT -p tcp --dport 25565 -j ACCEPT
# RUN netfilter-persistent save
# RUN netfilter-persistent reload

# RUN ufw allow 25565
# RUN ufw enable


EXPOSE ${PORT}