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

response = requests.get(
    "https://launchermeta.mojang.com/mc/game/version_manifest.json")
output = response.json()
data = json.dumps(output['latest']['release'])
core_count = multiprocessing.cpu_count()
SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)


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



@click.command()
@click.option("-v", "--version", is_flag=False, flag_value=latest_release, default=latest_release, help="Choose what version of the game(Defult: " + latest_release + ")")
@click.option("-c", "--cores", default=core_count, prompt="How many cores do you want to give to the server: ", help="Set how many cores you want the server to use")
@click.option("-r", "--ram", default=2048, prompt="How much ram would you like the server to use", help="Set how much allocated ram to the server")
@click.option("-p", "--port", default=25565, prompt="Which port do you want the server to be on", help="Set what port you want the server to run on")
@click.option("-s", "--service", is_flag=False, flag_value="minecraft", default="minecraft", help="Sets the service name(Optional)")
@click.option("-P", "--pluginpack", is_flag=True, flag_value=True, help="Generates a script of essential spigot plugins(Optional)")
@click.option("-d", "--debug", is_flag=True, flag_value=True, help="Allows to run a debug on any machine with defult vaules")
@click.option("-y", "--yes", is_flag=True, flag_value=True, help="You can have the server start on its own ")
def main(version, cores, ram, port, service, pluginpack, debug, yes):

    if SECRET_KEY or debug:
        user = 'minecraft'
    else:
        # user = os.getlogin()
        print("lol")
    if pluginpack:
        open("./pluginpack.py", "w+").write("""import os
import json
import requests

pwd = str(os.getcwd())
class plugins():
    def github_downloader(url, name, sub=1):
        folder_check = os.path.exists(pwd + "/plugins") 
        if folder_check:
            print("Folder already exist")
        else:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)
        dynmap_response = requests.get(url)
        data = dynmap_response.json()
        spigot_number = len(data[1]['assets'])
        download_link = data[1]['assets'][spigot_number - sub]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)
    def github_downloader_sr(url, name,):
        folder_check = os.path.exists(pwd + "/plugins") 
        if folder_check:
            print("Folder already exist")
        else:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)
        dynmap_response = requests.get(url)
        data = dynmap_response.json()
        download_link = data[0]['assets'][0]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)

if __name__ == '__main__':
    plugins.github_downloader("https://api.github.com/repos/webbukkit/dynmap/releases", "Dynmap.jar")
    plugins.github_downloader("https://api.github.com/repos/PryPurity/WorldBorder/releases", "WorldBorder.jar")
    plugins.github_downloader("https://api.github.com/repos/EssentialsX/Essentials/releases", "EssentialsX.jar", 8 )
    plugins.github_downloader_sr("https://api.github.com/repos/TIBTHINK/payRespect/releases", "PayRespect.jar")
                """)
    from pluginpack import plugins
    plugins.github_downloader(
        "https://api.github.com/repos/webbukkit/dynmap/releases", "Dynmap.jar")
    plugins.github_downloader(
        "https://api.github.com/repos/PryPurity/WorldBorder/releases", "WorldBorder.jar")
    plugins.github_downloader(
        "https://api.github.com/repos/EssentialsX/Essentials/releases", "EssentialsX.jar", 8)
    plugins.github_downloader_sr(
        "https://api.github.com/repos/TIBTHINK/payRespect/releases", "PayRespect.jar")

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
ExecStart= /usr/bin/bash """ + pwd + """/start.sh
ExecStop=/usr/bin/mcrcon -H 127.0.0.1 -P 25575 -p password stop
ExecReload=/usr/bin/mcrcon -H 127.0.0.1 -P 25575 -p password restart
[Install]
WantedBy=multi-user.target
            """)

def update_server():
    open("./update-server." + type_of_os + "", "w+").write("""java -jar BuildTools.jar --rev """ + version)

def make_main_world():
    open("./makeMainWorld.py", "w+").write("""from os import system as cmd
import os
if os.geteuid() != 0:
    exit("please run me as root")
else:
    cmd("systemctl stop minecraft.service")
    cmd("cp minecraft.service /etc/systemd/system/minecraft.service")
    cmd("systemctl daemon-reload") 
    cmd("systemctl start minecraft.service")
    cmd("systemctl enable minecraft.service")
                """)
def backend():
    print("Checking if BuildTools in installed")
    if not os.path.isfile("BuildTools.jar"):
        print("###DOWNLOADING REQUIRED FILES###")
        open(pwd + "BuildTools.jar", 'wb+').write(requests.get("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar").content)
    # Auto accpeting eula, making a sick start script and setting custom ports
    open("eula.txt", "w+").write("eula=true")
    open("start." + type_of_os, "w+").write("java -server -XX:ParallelGCThreads=" + str(cores) + " -Xms256M -Xmx" + str(ram) + "M -jar " + pwd + "/spigot-" + version + ".jar nogui ")
    open("server.properties", "w+").write("server-port=" + str(port) + "")
    # checking if this server supports custom scripts
    if type_of_os == "sh":
        service_file()
        make_main_world()
        update_server()
    else:
        update_server()
    # Listen, we dont like no docker containers
    # Checks to understand what to do
    if SECRET_KEY:
        start_server = "y"
        cmd("java -jar BuildTools.jar --rev " + version)
    elif debug:
        start_server = "n"
    else:
        cmd("java -jar BuildTools.jar --rev " + version)
        start_server = input("Would you like to start the server? [y/N]") or "n"
    # Auto start server
    if start_server == "y":
        if type_of_os == "sh":
            cmd("bash start.sh")
        else:
            cmd("start.bat")
    else:
        print("You can start the server with ./start." + type_of_os)

if __name__ == '__main__':
    main()
    backend()

