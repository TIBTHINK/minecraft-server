docker rmi minecraft-test
docker build -t minecraft-test .
docker run -td --name minecraft-server minecraft-test
docker rm minecraft-server