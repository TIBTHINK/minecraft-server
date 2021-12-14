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
def github_downloader(url, name, download_link_config):
    dynmap_response = requests.get(url)
    data = dynmap_response.json()
    spigot_number = len(data[1]['assets'])
    download_link = data[1]['assets'][spigot_number - 1]['browser_download_url']
    open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)

github_downloader("https://api.github.com/repos/webbukkit/dynmap/releases", "dynmap.jar", "[1]['assets'][spigot_number - 1]['browser_download_url']")