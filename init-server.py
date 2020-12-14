import os
from time import sleep
from os import system as cmd
import requests
from subprocess import run

try:
    version = input("What version of minecraft do you want? (defult is the lastest version): ") or "latest"

    print("Downloading required files")
    url = 'https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar'
    buildtools_file= requests.get(url)
    open('./BuildTools.jar', 'wb').write(buildtools_file.content)
    cmd("wget https://raw.githubusercontent.com/TIBTHINK/minecraft-server/main/makeMainWorld.py")
    cmd("wget https://raw.githubusercontent.com/TIBTHINK/minecraft-server/main/restart-world.sh")
    cmd("wget https://raw.githubusercontent.com/TIBTHINK/minecraft-server/main/start.sh")
    cmd("wget https://raw.githubusercontent.com/TIBTHINK/minecraft-server/main/minecraft.service")

    open("./eula.txt", "w+").write("eula=true")

    cmd("java -jar BuildTools.jar --rev " + version)
    cmd("bash start.sh")


    print("Congrats, you have just installed Spigot. I recommend turning on mcrcon for easy terminal access.\n I want to add a sort of plugin package manager but that is not in the works yet.")
except KeyboardInterrupt:
    print("\n\nbye")