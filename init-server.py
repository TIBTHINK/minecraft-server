import os
from time import sleep
from os import system as cmd
import requests
from subprocess import run

version = input("What version of minecraft do you want? (defult is the lastest version): ") or "latest"

print("Installing BuildTools")
url = 'https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar'
buildtools_file= requests.get(url)
open('./BuildTools.jar', 'wb').write(buildtools_file.content)


output = run("java -version", capture_output=True).stdout
if b'java: command not found' in output:
    print("installing java runtime envirement")
    cmd("sudo apt update")
    cmd("sudo apt install openjdk-8-jre-headless")

open("./eula.txt", "w+").write("eula=true")

cmd("java -jar BuildTools.jar --rev " + version)
cmd("bash start.sh")


print("Congrats, you have just installed Spigot. I recommend turning on mcrcon for easy terminal access.\n I want to add a sort of plugin package manager but that is not in the works yet.")