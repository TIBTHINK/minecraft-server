#!/bin/python3

import os
from time import sleep
from os import system as cmd
import requests
from subprocess import run

pwd = os.getcwd()
user = os.getlogin()

def service_file():
    open("./minecraft.service", "w+").write("""[Unit]
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
ExecStart=bash start.sh
ExecStop=""" + pwd + """/tools/mcrcon/mcrcon -H 127.0.0.1 -P 25575 -p password stop
ExecReload=""" + pwd + """/tools/mcron/mcron -H 127.0.0.1 -P 25575 -p password restart
[Install]
WantedBy=multi-user.target
    """)


try:
    version = input("What version of minecraft do you want? (defult is the lastest version): ") or "1.16.4"
    ram = input("how much ram would you like the server to use(defult is 2GB): ") or "2"
    cpu_cores = input("how many cores does your cpu have(defult is 4): ") or "4"

    print("Downloading required files")
    url = 'https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar'
    buildtools_file= requests.get(url)
    open('./BuildTools.jar', 'wb').write(buildtools_file.content)
    cmd("wget https://raw.githubusercontent.com/TIBTHINK/minecraft-server/main/makeMainWorld.py")
    cmd("wget https://raw.githubusercontent.com/TIBTHINK/minecraft-server/main/restart-world.sh")

    open("./eula.txt", "w+").write("eula=true")
    open("./start.sh", "w+").write("java -server -XX:+UseConcMarkSweepGC -XX:ParallelGCThreads=" + cpu_cores + " -XX:+AggressiveOpts -Xms256M -Xmx" + ram + "G -jar spigot-" + version + ".jar nogui ")
    service_file()
    
    cmd("java -jar BuildTools.jar --rev " + version)
    cmd("bash start.sh")
    


    print("\nCongrats, you have just installed Spigot. I recommend turning on mcrcon for easy terminal access.")
except KeyboardInterrupt:
    print("\n\nbye")
