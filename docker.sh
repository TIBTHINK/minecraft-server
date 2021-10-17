docker rmi minecraft-test
docker buildx build --build-arg CACHEBUST=$(date +%s) --progress plain -t  minecraft-server .
# docker run -td --name minecraft-test minecraft-server 

docker run -d \
  --name=minecraft-server \
  -e V=1.16.1 \
  -e CORES=4 \
  -e RAM=2048 \
  -e SERVICE=minecraft \
  -e TZ=America/New_York\
  -p 25565:25565 \
  -v /path/to/appdata/config:/config \
  --restart unless-stopped \
  docker.io/library/minecraft-server
# docker exec -id minecraft-server bash
# docker stop minecraft-server
# docker rm minecraft-server