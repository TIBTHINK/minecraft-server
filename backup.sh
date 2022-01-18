#!/bin/bash

function rcon {
mcrcon -H 127.0.0.1 -P 25575 -p 2240 "$1"
}

rcon "save-off"
rcon "save-all"
tar -cvpzf /config/workspace/minecraft-server/backups/server-$(date +%F-%H-%M).tar.gz /config/workspace/minecraft-server
rcon "save-on"

## Delete older backups
find /config/workspace/minecraft-server/backups/ -type f -mtime +7 -name '*.gz' -delete
                
                
                
                