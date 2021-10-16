#!/usr/bin/python3

# IMPORTS BABY
import os
from time import sleep
from os import system as cmd
import subprocess
import platform
import requests
import json
import multiprocessing
import sys
import click

pwd = os.getcwd()

response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
output = response.json()
data = json.dumps(output['latest']['release'])
core_count = str(multiprocessing.cpu_count())
pwd = os.getcwd()
SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if SECRET_KEY:
    user = 'minecraft'
else:
    user = os.getlogin()

system = platform.system()
if system == "Windows":
    type_of_os = "bat"
else:
    type_of_os = "sh"
punctuation = '''"'''
remove_punct = """"""
for character in data:
    if character not in punctuation:
        remove_punct = remove_punct + character

latest_release = remove_punct

try:
  
    @click.command()
    @click.option("-v", "--version", default=latest_release, prompt="What version of minecraft do you want?: ", help="Choose what version of the game")
    @click.option("-c", "--cores", default=core_count, prompt="How many cores do you want to give to the server: ", help="Set how many cores you want the server to use")
    @click.option("-r", "--ram", default=2048, prompt="How much ram would you like the server to use", help="set how much allocated ram to the server")
    @click.option("-p", "--port", default=25565, prompt="Which port do you want the server to be on", help="set what port you want the server to run on")
    @click.option("-s", "--service", default="minecraft", prompt="Name of the service file to be generated?:", help="Sets the service name")
    


    def main(version, cores, ram, port, service):
        version = version
        cores = cores
        ram = ram
        port = port
        service = service
    



        def service_file():
            open("./" + service + ".service", "w+").write("""[Unit]
Description=Minecraft Server
After=network.target
[Service]
User=""" + user + """
Nice=1
KillMode=none
SuccessExitStatus=0 1
ProtectHome=true
ProtectSystem=full
PrivateDevices=true
NoNewPrivileges=true
WorkingDirectory=""" + pwd + """
ExecStart= /usr/bin/bash """ + pwd +"""start.sh
ExecStop=/usr/local/bin/mcrcon -H 127.0.0.1 -P 25575 -p password stop
ExecReload=/usr/local/bin/mcrcon -H 127.0.0.1 -P 25575 -p password restart
[Install]
WantedBy=multi-user.target
            """)
        def mcron_setup():

            cmd("git clone https://github.com/Tiiffi/mcrcon.git minecraft-server/mcrcon")
            cmd("cd minecraft-server/mcron")
            cmd("make")
            cmd("sudo make install")
            cmd("cd " + pwd)


        def update_server():
            open("./update-server." + type_of_os + "",
                "w+").write("""java -jar BuildTools.jar --rev """ + version)


        def make_main_world():
            open("./makeMainWorld.py", "w+").write("""from os import system as cmd
import os
from os import system as cmd
if os.geteuid() != 0:
    exit("please run me as root")
else:
    cmd("systemctl stop minecraft.service")
    cmd("cp minecraft.service /etc/systemd/system/minecraft.service")
    cmd("systemctl daemon-reload")
    cmd("systemctl start minecraft.service")
    cmd("systemctl enable minecraft.service")
                """)

        print("Checking if BuildTools in installed")
        if not os.path.isfile("BuildTools.jar"):
            print("###DOWNLOADING REQUIRED FILES###")
            open(pwd + "/BuildTools.jar", 'wb').write(requests.get("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar").content)

        open("./eula.txt", "w+").write("eula=true")
        open("./start." + type_of_os + "", "w+").write("java -server -XX:ParallelGCThreads=" + cores + " -Xms256M -Xmx" + str(ram) + "M -jar " + pwd +  "spigot-" + version + ".jar nogui ")
        open("server.properties", "w+").write("server-port=" + str(port) + "")

        if type_of_os == "sh":
            service_file()
            make_main_world()
            update_server()         
            cmd("java -jar BuildTools.jar --rev " + version)
            if SECRET_KEY == "False":
                mcron_setup()
            

        else:
            update_server()
            cmd("java -jar BuildTools.jar --rev " + version)


        if SECRET_KEY:
            start_server = "n"
        else:
            start_server = input("Would you like to start the server? [y/N]") or "n"
        
        if start_server == "y":
            if type_of_os == "sh":
                cmd("bash start.sh")
            else:
                cmd("start.bat")
        else:
            print("You can start the server with ./start." + type_of_os)


    if __name__ == '__main__':
        main()
    

except KeyboardInterrupt:
    print("\nbye")