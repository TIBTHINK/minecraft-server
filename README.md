# minecraft-server

A few scrips to setup a spigot server in a jif

All you need to run this program is python3 and the java dev kit
Debain based installs
``` bash
sudo apt install git openjdk-17-jre-headless python3
```
Arch based installs
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
Debain based OS supported
Command line configuration \
Plugin pack script generator\
Install of mcron \
backup setup

## Command line configuration
you can easly find out the command line config by typing

``` bash
tibthink@JARVIS:~/minecraft-server$ python3 init-server.py --help
Usage: init-server.py [OPTIONS]

Options:
  -v, --version TEXT   Choose what version of the game(Defult: 1.18.1)
  -c, --cores INTEGER  Set how many cores you want the server to use
  -r, --ram INTEGER    Set how much allocated ram to the server
  -p, --port INTEGER   Set what port you want the server to run on
  -s, --service TEXT   Sets the service name(Optional)
  -R, --rcon TEXT      Downloads and installs mcrcon
  -P, --pluginpack     Generates a script of essential spigot
                       plugins(Optional)
  -y, --yes            Says yes to autostarting the server
  -d, --debug          Enables debug mode
  -b, --backup         Sets up a backup script(McRcon is required for backups)
  --help               Show this message and exit.
```

A example use would be:

``` bash
tibthink@JARVIS:~/minecraft-server$ python3 init-server.py --version 1.17.1 --cores 3 --ram 1024 --port 4444 --service test
```

For installing the plugin pack you would run a command like this:

``` bash
tibthink@JARVIS:~/minecraft-server$ python3 init-server.py --version 1.17.1 --cores 3 --ram 1024 --port 4444 --service test -P
```
To update plugins simply just run pluginpack.py and it will automaticly download the latest versions

For installing mcrcon and setting up backups.

```bash
tibthink@JARVIS:~/minecraft-server$ python3 init-server.py -R password -b
```

## Docker

as of right now docker isnt working, but i am working on it. \
a example docker command would look like:
``` bash
docker run -d \
  --name=minecraft-server \
  -e VERSION= 1.16.1 \
  -e CORES=4 \
  -e RAM=2048 \
  -e SERVICE=minecraft \
  -e TZ=America/New_York \
  -p 25565:25565 \
  -v /path/to/appdata/config:/config \
  --restart unless-stopped \
  docker.io/tibthink/minecraft-server
```

## Going to be added to the script

Detect if requirements are met \
Docker file/image \
Installing correct libray for 1.17+ \
Have plugin pack find the file name automaticly \
Installing plugins from spigot, github and bukkit website.

