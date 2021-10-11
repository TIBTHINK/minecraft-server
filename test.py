import click
import os
from time import sleep
from os import system as cmd
import subprocess
import platform
import requests
import json
import multiprocessing

response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
output = response.json()
data = json.dumps(output['latest']['release'])
core_count = int(multiprocessing.cpu_count())
pwd = os.getcwd()
user = 'user'  #os.getlogin()

system = platform.system()
if system == "Windows":
    type_of_os = "bat"
else:
    type_of_os = "sh"
punctuation = '''"'''
remove_punct = """"""
for character in data:
    if character not in punctuation:
        remove_punct = remove_punct + character

latest_release = remove_punct

@click.command()
@click.option("--version", default=latest_release, prompt="What version of minecraft do you want?: ", help="Choose what version of the game")
@click.option("--cores", default=core_count, prompt="How many cores do you want to give to the server: ", help="Set how many cores you want the server to use")
@click.option("--ram", default=2048, prompt="How much ram would you like the server to use", help="set how much allocated ram to the server")
@click.option("--port", default=25565, prompt="Which port do you want the server to be on", help="set what port you want the server to run on")
def hello(cores, version, ram, port):   
    print(cores)
    print(version)
    print(ram)
    print(port)

if __name__ == '__main__':
    hello()