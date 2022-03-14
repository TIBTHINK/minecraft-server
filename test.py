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
    