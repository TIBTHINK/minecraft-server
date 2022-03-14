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
import subprocess
from datetime import date

today = date.today()
pwd = os.getcwd()

response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
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

try:
  
    @click.command()
    @click.option("-v", "--version", is_flag=False, flag_value=latest_release, default=latest_release, help="Choose what version of the game(Defult: " + latest_release + ")")
    @click.option("-p", "--port", default=25565, is_flag=False, flag_value=25565, help="Set what port you want the server to run on")
    @click.option("-s", "--service", is_flag=False, flag_value="minecraft", default="minecraft", help="Sets the service name(Optional)")
    @click.option("-R", "--rcon", is_flag=False, flag_value="Password", default="change-to-a-better-password", help="Downloads and installs mcrcon")
    @click.option("-P", "--pluginpack", is_flag=True, flag_value=True, help="Generates a script of essential spigot plugins(Optional)")
    @click.option("-y", "--yes", is_flag=True, flag_value=True, help="Says yes to autostarting the server after setup is done")
    @click.option("-d", "--debug", is_flag=True, flag_value=True, help="Enables debug mode")
    @click.option("-b", "--backup", is_flag=True, flag_value=True, help="Sets up a backup script(McRcon is required for backups)")
    @click.option("-C", "--clean", is_flag=True, flag_value=True, help="Reverts back to a clean slate (THIS WILL REMOVE EVERYTHING THAT ISNT ALREADY IN THE REPO")

    def main(version, cores, ram, port, service, pluginpack, yes, debug, rcon, backup, clean):

        
        # Checks if rcon, backup or service is called on a non linux machine
        if type_of_os == "bat":
            if not bool(rcon):
                exit("Rcon isnt supported on your machine")
            elif not bool(service):
                exit("Service file isnt supported on your machine")

        password = rcon
        if SECRET_KEY or debug:
            user = 'minecraft'
        else:
            user = os.getlogin()


        if clean:
            import shutil
            import os
            from os import walk
            filenames = os.listdir("./")
            dont_remove_these_files = ["docker-build-test.sh", "docker.sh", "Dockerfile", ".gitignore", "init-server.py", "README.md", "requirements.txt", "test.py", ".git", "Bukkit", "Spigot", "BuildData", "backups", "CraftBukkit", "mcrcon", "work", "__pycache__", "plugins", "apache-maven-3.6.0"]
            print("###Removing needed files from delete list###")
            for i in dont_remove_these_files:
                if i in filenames:
                    filenames.remove(i)
                else:
                    print("File does not exist")
                # print(filenames)


            print(filenames)
            directory = next(os.walk("./"))[1]
            directory.remove(".git")
            clean = True

            if clean:
                try:
                    for i in directory:
                        print("Removing: " + i)
                        shutil.rmtree(i)
                    for i in filenames:
                        print("Removing: " + i)
                        os.remove(i)
                except OSError as e:
                    print("Error: %s : %s" % (directory, e.strerror))
    
            

        def plugin_pack_script_gen():
            open(pwd + "/pluginpack.py", 'w+').write("""# Yes i know, i could find a way to get the name of the jar file,
# but i am not motivated to give a fuck about it so you guys just
# have to deal with the lazyness 
import os
import json
import requests
pwd = str(os.getcwd())
from os import system as cmd
import platform
import sys


class plugins():
    # This is for repos with more than one release version
    def github_downloader(url, name, sub=1):
        folder_check = os.path.exists(pwd + "/plugins") 
        if not folder_check:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)
        response = requests.get(url)
        data = response.json()
        spigot_number = len(data[1]['assets'])
        download_link = data[1]['assets'][spigot_number - sub]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)
    # This is for repo's that have a single release
    def github_downloader_sr(url, name):
        folder_check = os.path.exists(pwd + "/plugins") 
        if not folder_check:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)         
        response = requests.get(url)
        data = response.json()
        download_link = data[0]['assets'][0]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)
    def jenkins_download(url, name):
        folder_check = os.path.exists(pwd + "/plugins") 
        if not folder_check:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)         
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(url).content)

if __name__ == '__main__':
        print('[Downloading] | >                                     | 0% | 0/6\\r', end='', flush=True)
        plugins.github_downloader("https://api.github.com/repos/webbukkit/dynmap/releases", "Dynmap.jar")
        sys.stdout.flush()
        print('[Downloading] | ======>                               | 16.6% | 1/6\\r', end='', flush=True)
        plugins.github_downloader("https://api.github.com/repos/PryPurity/WorldBorder/releases", "WorldBorder.jar")
        sys.stdout.flush()
        print('[Downloading] | ============>                         | 33.2% | 2/6\\r', end='', flush=True)
        plugins.github_downloader("https://api.github.com/repos/EssentialsX/Essentials/releases", "EssentialsX.jar", 8 )
        sys.stdout.flush()
        print('[Downloading] | ==================>                   | 49.8% | 3/6\\r', end='', flush=True)
        plugins.github_downloader_sr("https://api.github.com/repos/TIBTHINK/payRespect/releases", "PayRespect.jar")
        sys.stdout.flush()
        print('[Downloading] | ========================>             | 66.4% | 4/6\\r', end='', flush=True)
        plugins.jenkins_download("https://ci.opencollab.dev//job/GeyserMC/job/Geyser/job/master/lastSuccessfulBuild/artifact/bootstrap/spigot/target/Geyser-Spigot.jar", "Geyser_Spigot.jar")
        sys.stdout.flush()
        print('[Downloading] | ==============================>       | 83.0% | 5/6\\r', end='', flush=True)
        plugins.jenkins_download("https://ci.opencollab.dev/job/GeyserMC/job/Floodgate/job/master/lastSuccessfulBuild/artifact/spigot/target/floodgate-spigot.jar", "floodgate-spigot.jar")
        sys.stdout.flush()
        print('[Downloading] | ====================================> |  100% | 6/6\\n', end='', flush=True)
            """)
            from pluginpack import plugins
            print("### DOWNLOADING PLUGINS ###")
            print('[Downloading] | >                                     | 0% | 0/6\r', end='', flush=True)
            plugins.github_downloader("https://api.github.com/repos/webbukkit/dynmap/releases", "Dynmap.jar")
            sys.stdout.flush()
            print('[Downloading] | ======>                               | 16.6% | 1/6\r', end='', flush=True)
            plugins.github_downloader("https://api.github.com/repos/PryPurity/WorldBorder/releases", "WorldBorder.jar")
            sys.stdout.flush()
            print('[Downloading] | ============>                         | 33.2% | 2/6\r', end='', flush=True)
            plugins.github_downloader("https://api.github.com/repos/EssentialsX/Essentials/releases", "EssentialsX.jar", 8 )
            sys.stdout.flush()
            print('[Downloading] | ==================>                   | 49.8% | 3/6\r', end='', flush=True)
            plugins.github_downloader_sr("https://api.github.com/repos/TIBTHINK/payRespect/releases", "PayRespect.jar")
            sys.stdout.flush()
            print('[Downloading] | ========================>             | 66.4% | 4/6\r', end='', flush=True)
            plugins.jenkins_download("https://ci.opencollab.dev//job/GeyserMC/job/Geyser/job/master/lastSuccessfulBuild/artifact/bootstrap/spigot/target/Geyser-Spigot.jar", "Geyser_Spigot.jar")
            sys.stdout.flush()
            print('[Downloading] | ==============================>       | 83.0% | 5/6\r', end='', flush=True)
            plugins.jenkins_download("https://ci.opencollab.dev/job/GeyserMC/job/Floodgate/job/master/lastSuccessfulBuild/artifact/spigot/target/floodgate-spigot.jar", "floodgate-spigot.jar")
            sys.stdout.flush()
            print('[Downloading] | ====================================> |  100% | 6/6\n', end='', flush=True)


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
ExecStart= /usr/bin/bash """ + pwd +"""/start.sh
ExecStop=/usr/bin/mcrcon -H 127.0.0.1 -P 25575 -p password stop
ExecReload=/usr/bin/mcrcon -H 127.0.0.1 -P 25575 -p password restart
[Install]
WantedBy=multi-user.target
            """)

        def update_server():
            open("./update-server." + type_of_os, "w+").write("""java -jar BuildTools.jar --rev """ + version)


        def make_main_world():
            open("./makeMainWorld.sh", "w+").write("""if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

systemctl stop minecraft.service
cp minecraft.service /etc/systemd/system/minecraft.service
systemctl daemon-reload
systemctl start minecraft.service
systemctl enable minecraft.service
                """)
        def backups():
            folder_check = os.path.exists(pwd + "/backups") 
            if not folder_check:
                path = os.path.join(pwd, "backups")
                os.mkdir(path)

            if type_of_os == "bat" or debug:
                open(pwd + "\\backup.bat", 'w+').write("""@echo on
                echo ### Backing up ###" 
                powershell Compress-Archive """ + pwd + """\ """+ pwd +"""\\backups\Server-""" + today.strftime("%d/%m/%Y") + """.zip
                
                
                """)

            open(pwd + "/backup.sh", 'w+').write("""#!/bin/bash

function rcon {
mcrcon -H 127.0.0.1 -P 25575 -p """ + password + """ "$1"
}

rcon "save-off"
rcon "save-all"
tar -cvpzf """ + pwd + """/backups/server-$(date +%F-%H-%M).tar.gz """ + pwd + """
rcon "save-on"

## Delete older backups
find """ + pwd + """/backups/ -type f -mtime +7 -name '*.gz' -delete
                
                
                
                """)

        def rcon_install():
        # Downloads and installs mcrcon
            cmd("git clone https://github.com/Tiiffi/mcrcon") 
            os.chdir('./mcrcon')
            cmd("make")
            cmd("cp mcrcon /usr/bin/mcrcon")
            os.chdir('../')
            open(pwd + "/terminal.sh", 'w').write("mcrcon -H 127.0.0.1 -P 25575 -p " + password + " -t")


        # It is indented correctly, dont try to fix it
        print("Checking if BuildTools in installed")
        if not os.path.isfile("BuildTools.jar"):
            print("### DOWNLOADING BUILDTOOLS ###")
            open(pwd + "/BuildTools.jar", 'wb').write(requests.get("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar").content)
        # Auto accpeting eula, making a sick start script and setting custom ports
        open("eula.txt", "w+").write("eula=true")
        open("start." + type_of_os, "w+").write("java -server -XX:ParallelGCThreads=" + str(cores) + " -Xms256M -Xmx" + str(ram) + "M -jar " + pwd +  "/spigot-" + version + ".jar nogui ")
        open("server.properties", "w+").write("server-port=" + str(port) + "")
        if bool(rcon):
            open("server.properties", "w+").write("""\nrcon.port=25575
rcon.password=""" + rcon + """
enable-rcon=true""")



        # checking if this server supports custom scripts
        if type_of_os == "sh":
            service_file()
            make_main_world()
            update_server() 
            if bool(rcon):
                rcon_install()
            if backup:
                backups()    
        else:
            update_server()
               
        cmd("java -jar BuildTools.jar --rev " + version)
        if pluginpack:
            plugin_pack_script_gen()

        # Listen, we dont like no docker containers
        # Checks if script is running in a docker container
        if SECRET_KEY:
            start_server = "n"
        elif yes:
            start_server = "y"
        else:
            start_server = input("Would you like to start the server? [y/N] ") or "n"
        

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

    

except KeyboardInterrupt:
    print("\nbye")