# Server setup tool

## Please note
this was based on my servers configuration, most likely the minecraft.service file wont work unless you followed this guide.

edit files like start to have the multi-threading correct for your specific system

https://linuxize.com/post/how-to-install-minecraft-server-on-ubuntu-18-04/


## Getting started
you will need python3 for this script.
all you need to start the script is.

```
curl https://raw.githubusercontent.com/TIBTHINK/minecraft-server/main/init-server.py | bash
```
depending if you have the java runtime environment install you wont need sudo.

after that you should be good to go. after installing spigot the server will run for the first time and you should be able to join.
you may need to config your firewall to allow port 25565, with this command
```
sudo ufw allow 25565
sudo ufw enable
```
