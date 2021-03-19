import argparse
import shutil
import os

files = ['minecraft.service', 'Bukkit', '.vscode', 'apache-maven-3.6.0', 'update-server.sh', 'CraftBukkit', 'makeMainWorld.py', 'Spigot', 'eula.txt', 'work', 'BuildTools.jar', 'BuildTools.log.txt', 'start.sh', 'spigot-1.16.5.jar', 'BuildData', 'README.md']

def listToString(list):
    str1 = " "
    return (str1.join(list))
files = listToString(files)



parser = argparse.ArgumentParser()
parser.add_argument("clean", help="Removes all files exept the init file")
args = parser.parse_args()
if args.clean:
    os.system("rm -rf " + files)

