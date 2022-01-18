import os
from os import system as cmd

pwd = str(os.getcwd())

def backup():
    folder_check = os.path.exists(pwd + "/backups") 
    if not folder_check:
        path = os.path.join(pwd, "backups")
        os.mkdir(path)

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
  open(pwd + "terminal.sh", 'w').write("mcrcon -H 127.0.0.1 -P 25575 -p """ + password + """ -t")



# rcon_install()
backup("test")
