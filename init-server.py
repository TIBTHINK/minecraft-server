#!/usr/bin/python3
import os
from time import sleep
from os import system as cmd
import subprocess
import platform
import requests
import json
import multiprocessing
import argparse 

core_count = str(multiprocessing.cpu_count())
punctuation = '''"'''
pwd = os.getcwd()
user = os.getlogin()
response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
output = response.json()
data = json.dumps(output['latest']['release'])
remove_punct = ""
for character in data:
    if character not in punctuation:
        remove_punct = remove_punct + character
latest_release = remove_punct
core_count = str(multiprocessing.cpu_count())
system = platform.system()
if system == "Windows":
    type_of_os = "bat"
else:
    type_of_os = "sh"

def update_server():
    open("./update-server." + type_of_os + "", "w+").write("""
    java -jar BuildTools.jar --rev latest
""")

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
    version = input("What version of minecraft do you want? (Defult is the lastest version): ") or latest_release
    ram = input("how much ram would you like the server to use (Defult is 2048MB): ") or "2048"
    cpu_cores = input("how many cores do you want to give to the server (Defult is how many cores you have): ") or core_count
    build_env = "java -jar BuildTools.jar --rev " + version 
    print("Checking if BuildTools in installed")
    if not os.path.isfile("BuildTools.jar"):
        print("Downloading required files")
        open(pwd + "/BuildTools.jar", 'wb').write(requests.get("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar").content)

    open("./eula.txt", "w+").write("eula=true")
    open("./start."+ type_of_os + "", "w+").write("java -server -XX:+UseConcMarkSweepGC -XX:ParallelGCThreads=" + cpu_cores + " -XX:+AggressiveOpts -Xms256M -Xmx" + ram + "M -jar spigot-" + version + ".jar nogui ")
    if type_of_os == "sh":
        service_file()
        make_main_world()
        update_server()
    else:
        update_server()
    cmd(build_env)      
    start_server = input("Would you like to start the server?[y/N]: ") or "n"
    if start_server == "y":
        if type_of_os == "sh":
            cmd("bash start.sh")
        else:
            cmd("start.bat")
    else:
        print("\nCongrats, you have just installed Spigot. I recommend turning on mcrcon for easy terminal access.")
except KeyboardInterrupt:
    print("\n\nbye") 
