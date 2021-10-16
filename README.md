# minecraft-server

A few scrips to setup a spigot server in a jif

All you need to run this program is python3 and the java dev kit
Ubuntu Based installs
``` bash
sudo apt install git openjdk-8-jre-headless python3
```
Arch Based installs
```bash
sudo pacman -Sy git jre8-openjdk-headless python3 gcc
```

## what does this script do?

Auto configures a service file for you to deploy and have minecraft run in the background. \
Makes a run script for you to use. \
Sets the ram to what you want to give them. \
Auto accepts the EULA before boot. \
Auto detect how many cores are in the system. \
Windows supported. [Beta] \
Arch based OS supported. \
Command line configuration 

## Command line configuration
you can easly find out the command line config by typing

``` bash
tibthink@JARVIS:~/minecraft-server$ python3 init-server.py --help
Usage: init-server.py [OPTIONS]

Options:
  -v, --version TEXT  Choose what version of the game
  -c, --cores TEXT    Set how many cores you want the server to use
  -r, --ram INTEGER   set how much allocated ram to the server
  -p, --port INTEGER  set what port you want the server to run on
  -s, --service TEXT  Sets the service name
  --help              Show this message and exit.
```

A example use would be:

``` bash
python3 init-server.py --version 1.17.1 --cores 3 --ram 1024 --port 4444 --service test
```
## Docker

as of right now docker isnt working, but i am working on it. \
a example docker command would look like:
``` bash
docker run -d \
  --name=minecraft-server \
  -e VERSION= 1.16.1
  -e CORES=4
  -e RAM=2048
  -e SERVICE=minecraft
  -e TZ=America/New_York
  -p 25565:25565 \
  -v /path/to/appdata/config:/config \
  --restart unless-stopped \
  docker.io/tibthink/minecraft-server
```

## Going to be added to the script

Install of mcron \
Detect if requirements are met \
docker file/image
