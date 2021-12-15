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

pwd = os.getcwd()
class plugins():
    def github_downloader(url, name, sub=1):
        dynmap_response = requests.get(url)
        data = dynmap_response.json()
        spigot_number = len(data[1]['assets'])
        print(data[1]['assets'][spigot_number - sub]['browser_download_url'])
        # open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)
    def github_downloader_single_release(url, name, sub=1):
        dynmap_response = requests.get(url)
        data = dynmap_response.json()
        # spigot_number = len(data[0]['assets'])
        print(data[0]['assets'][0]['browser_download_url'])



plugins.github_downloader("https://api.github.com/repos/webbukkit/dynmap/releases", "Dynmap.jar")
plugins.github_downloader("https://api.github.com/repos/PryPurity/WorldBorder/releases", "WorldBorder.jar")
plugins.github_downloader("https://api.github.com/repos/EssentialsX/Essentials/releases", "EssentialsX.jar", 8 )
plugins.github_downloader_temp("https://api.github.com/repos/TIBTHINK/payRespect/releases", "PayRespect.jar")