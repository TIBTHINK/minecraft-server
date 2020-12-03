#!/bin/sh
echo this will restart a new world you have 5 secs to cancel
sleep 5

rm -rf world world_nether world_the_end plugins/dynmap/
./start.sh
