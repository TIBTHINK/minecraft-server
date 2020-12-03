#!/bin/sh


java -server -XX:+UseConcMarkSweepGC -XX:ParallelGCThreads=24 -XX:+AggressiveOpts -Xms4G -Xmx6G -jar spigot-*.jar nogui 
