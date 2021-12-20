import os
import json
import requests

pwd = str(os.getcwd())
class plugins():
    def github_downloader(url, name, sub=1):
        folder_check = os.path.exists(pwd + "/plugins") 
        if folder_check:
            print("Folder already exist")
        else:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)
        dynmap_response = requests.get(url)
        data = dynmap_response.json()
        spigot_number = len(data[1]['assets'])
        download_link = data[1]['assets'][spigot_number - sub]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)
    def github_downloader_sr(url, name,):
        folder_check = os.path.exists(pwd + "/plugins") 
        if folder_check:
            print("Folder already exist")
        else:
            path = os.path.join(pwd, "plugins")
            os.mkdir(path)
        dynmap_response = requests.get(url)
        data = dynmap_response.json()
        download_link = data[0]['assets'][0]['browser_download_url']
        open(pwd + "/plugins/" + name, 'wb').write(requests.get(download_link).content)

if __name__ == '__main__':
    plugins.github_downloader("https://api.github.com/repos/webbukkit/dynmap/releases", "Dynmap.jar")
    plugins.github_downloader("https://api.github.com/repos/PryPurity/WorldBorder/releases", "WorldBorder.jar")
    plugins.github_downloader("https://api.github.com/repos/EssentialsX/Essentials/releases", "EssentialsX.jar", 8 )
    plugins.github_downloader_sr("https://api.github.com/repos/TIBTHINK/payRespect/releases", "PayRespect.jar")
                