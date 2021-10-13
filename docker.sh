docker rmi minecraft-test
docker buildx build --progress plain -t minecraft-server .
docker run -td --name minecraft-server minecraft-test
# docker stop minecraft-server
# docker rm minecraft-server