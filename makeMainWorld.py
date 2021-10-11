from os import system as cmd
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
                