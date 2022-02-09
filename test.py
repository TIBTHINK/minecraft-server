import subprocess
subprocess = subprocess.Popen("java --version", shell=True, stdout=subprocess.PIPE)
subprocess_return = subprocess.stdout.read()
print(subprocess_return)