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
import argparse


pwd = os.getcwd()
# Adding parser to program
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clean", help="Removes all files exept the init file",
                    action="store_true")
parser.add_argument("-v", "--version", help="Set the version you want",
                    action="store_true")
parser.add_argument("-C", "--cores", help="Set how many cores you want the server to use",
                    action="store_true")
parser.add_argument("-m", "--memory", help="Set how much ram you want to allocate",
                    action="store_true")
args = parser.parse_args()
if args.clean:
    print("work in proggress")

else:
# The main meat of the script
    response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    output = response.json()
    data = json.dumps(output['latest']['release'])
    core_count = str(multiprocessing.cpu_count())
    pwd = os.getcwd()
    user = os.getlogin()
    
    
    core_count = str(multiprocessing.cpu_count())
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


    def mcron_setup():
        import os
        dir = "tools"
        dir2 = "server"
        parent_dir = "./"
        mode = 0o777
        path = os.path.join(parent_dir, dir)
        path2 = os.path.join(parent_dir, dir2)
        if not os.path.isdir(path + path2):
            os.mkdir(path, mode)
            os.mkdir(path2, mode)
        else:
            return
        cmd("git clone https://github.com/Tiiffi/mcrcon.git tools/mcrcon")
        cmd("cd tools/mcron")
        cmd("gcc -std=gnu11 -pedantic -Wall -Wextra -O2 -s -o mcrcon mcrcon.c")
        cmd("cd " + pwd)

    def update_server():
        open("./update-server." + type_of_os + "", "w+").write("""java -jar BuildTools.jar --rev """ + version )

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
        open("./" + service_file_name + ".service", "w+").write("""[Unit]
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
        version = input("What version of minecraft do you want? (Latest version is: "+ latest_release +"): ") or latest_release
        ram = input("How much ram would you like the server to use (Defult is 2048MB): ") or "2048"
        cpu_cores = input("How many cores do you want to give to the server (Defult is how many cores you have): ") or core_count
        port = input("Which port do you want the server to be on (Defult is 25565): ") or "25565"
        
        if type_of_os == "sh":
            service_file_name = input("Name of the service file to be generated? (Defult is minecraft): ") or "minecraft"
        build_env = "java -jar BuildTools.jar --rev " + version 
        print("Checking if BuildTools in installed")
        if not os.path.isfile("BuildTools.jar"):
            print("###DOWNLOADING REQUIRED FILES###")
            open(pwd + "/BuildTools.jar", 'wb').write(requests.get("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar").content)

        open("./eula.txt", "w+").write("eula=true")
        open("./start."+ type_of_os + "", "w+").write("java -server -XX:ParallelGCThreads=" + cpu_cores + " -Xms256M -Xmx" + ram + "M -jar spigot-" + version + ".jar nogui ")
        open("server.properties", "w+").write("server-port=" + port + "")
        if type_of_os == "sh":
            service_file()
            make_main_world()
            update_server()
            print("seting up mcron")
            mcron_setup()
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
