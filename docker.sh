docker rmi minecraft-test
docker buildx build --progress plain -t  minecraft-server .
docker run -td --name minecraft-test minecraft-server 
# docker exec -id minecraft-server bash
# docker stop minecraft-server
# docker rm minecraft-server