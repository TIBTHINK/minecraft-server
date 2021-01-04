#!/bin/python3

import os
from time import sleep
from os import system as cmd
from subprocess import run
import platform

pwd = os.getcwd()
user = os.getlogin()

def make_main_world():
    open("./makeMainWorld.py", "w+").write("""from os import system as cmd
    import os
    from os import system as cmd
            
    if os.geteuid() != 0:
        exit("please run me as root")
    else:

    cmd("cp minecraft.service /etc/systemd/system/minecraft.service")
    cmd("systemctl daemon-reload")
    cmd("systemctl start minecraft.service")
    cmd("systemctl enable minecraft.service")
        """)


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
    system = platform.system()
    if system == "Windows":
        exit("This script was Built for Linux, Windows support will be added in the future")



    version = input("What version of minecraft do you want? (defult is the lastest version): ") or "1.16.4"
    ram = input("how much ram would you like the server to use(defult is 2GB): ") or "2"
    cpu_cores = input("how many cores does your cpu have(defult is 4): ") or "4"

    print("Downloading required files")
    cmd("wget https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar")

    open("./eula.txt", "w+").write("eula=true")
    open("./start.sh", "w+").write("java -server -XX:+UseConcMarkSweepGC -XX:ParallelGCThreads=" + cpu_cores + " -XX:+AggressiveOpts -Xms256M -Xmx" + ram + "G -jar spigot-" + version + ".jar nogui ")
    service_file()
    make_main_world()
    
    cmd("java -jar BuildTools.jar --rev " + version)

    start_server = input("Would you like to start the server after the build is done?[y/n]: ") or "n"
    if start_server == "y":
        cmd("bash start.sh")
    else:

    


    print("\nCongrats, you have just installed Spigot. I recommend turning on mcrcon for easy terminal access.")
except KeyboardInterrupt:
    print("\n\nbye")
