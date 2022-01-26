import os
import json
import requests
pwd = str(os.getcwd())
from os import system as cmd
import platform
import sys

def compute():
    plugins.jenkins_download("https://ci.opencollab.dev/job/GeyserMC/job/Floodgate/job/master/lastSuccessfulBuild/artifact/spigot/target/floodgate-spigot.jar", "floodgate-spigot.jar")
    plugins.jenkins_download("https://ci.opencollab.dev//job/GeyserMC/job/Geyser/job/master/lastSuccessfulBuild/artifact/bootstrap/spigot/target/Geyser-Spigot.jar", "Geyser_Spigot.jar")
    plugins.github_downloader_sr("https://api.github.com/repos/TIBTHINK/payRespect/releases", "PayRespect.jar")
    plugins.github_downloader("https://api.github.com/repos/EssentialsX/Essentials/releases", "EssentialsX.jar", 8 )
    plugins.github_downloader("https://api.github.com/repos/PryPurity/WorldBorder/releases", "WorldBorder.jar")
    plugins.github_downloader("https://api.github.com/repos/webbukkit/dynmap/releases", "Dynmap.jar")
    yield 

class plugins():
    # This is for repos with more than one release version
    def github_downloader(url, name, sub=1):
        folder_check = os.path.exists(pwd + "/plugins") 
        if not folder_check:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)
        response = requests.get(url)
        data = response.json()
        spigot_number = len(data[1]['assets'])
        download_link = data[1]['assets'][spigot_number - sub]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)
    # This is for repo's that have a single release
    def github_downloader_sr(url, name):
        folder_check = os.path.exists(pwd + "/plugins") 
        if not folder_check:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)         
        response = requests.get(url)
        data = response.json()
        download_link = data[0]['assets'][0]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)
    def jenkins_download(url, name):
        folder_check = os.path.exists(pwd + "/plugins") 
        if not folder_check:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)         
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(url).content)
from alive_progress import alive_bar

with alive_bar(6) as bar:
    for i in compute():
        bar()