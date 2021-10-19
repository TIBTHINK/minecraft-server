docker rmi minecraft-test
docker build -t  tibthink/minecraft-server .
# docker run -t --name minecraft-test minecraft-server /bin/bash 

docker run -d -t \
  --name=minecraft-server \
  -e V=1.16.1 \
  -e CORES=4 \
  -e RAM=2048 \
  -e SERVICE=minecraft \
  -e TZ=America/New_York\
  -p 25565:25565 \
  -v /com.docker.devenvironments.code/config:/config \
  minecraft-server \
  
  
# docker exec -id minecraft-server bash
# docker stop minecraft-server
# docker rm minecraft-server