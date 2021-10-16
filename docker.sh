docker rmi minecraft-test
docker buildx build --progress plain -t  minecraft-server .
docker run -t  --name minecraft-test minecraft-server
# docker stop minecraft-server
# docker rm minecraft-server