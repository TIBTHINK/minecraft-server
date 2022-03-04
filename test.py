import shutil
import os
from os import walk
filenames = next(walk("./"), (None, None, []))[2]
dont_remove_these_files = ['docker-build-test.sh', 'docker.sh', 'Dockerfile', '.gitignore', 'init-server.py', 'READEME.md', 'requirements.txt', 'test.py']

for i in dont_remove_these_files:
    filenames.remove(i)


print(filenames)
directory = next(os.walk('./'))[1]
directory.remove(".git")
clean = True

if clean:
    try:
        for i in directory:
            shutil.rmtree(i)
        for i in filenames[:]:
            os.remove(i)
    except OSError as e:
        print("Error: %s : %s" % (directory, e.strerror))
    