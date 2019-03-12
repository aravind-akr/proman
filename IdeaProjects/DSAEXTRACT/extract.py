
# This is untar/unzip a file from given path location. To do this: take a path, check its cwd,
# if it is same with the dir given in path
# If not, change to dir in path. Check if it zip or tar, then unzip or untar respectively.
# It should untar/unzip to the same file name.
# pip install patool, pip install pyunpack

from pyunpack import Archive
import os, sys

# Checking whether path directory and current Directory are same, if not change the dir to path dir.
# Checking whether file exists

def checkDirectoryAndFile(pathdir,currentDir,filename):
    if(pathdir == currentDir):
        print("It is in same directory")
    else:
        os.chdir(pathdir)
        print("It is different directory")

    if os.path.exists(filename):
        print("Exists already")
    else:
        print("Does not Exists")
        os.mkdir(filename)

# Check if it is tar or zip file

def extract(tarfilename):
    with open(tarfilename, 'r') as tarfile:
        base = os.path.basename(tarfile.name)
        filename=base[:-4]
        pathdir=os.path.dirname(tarfile.name)
        currentDir=os.getcwd()
    checkDirectoryAndFile(pathdir, currentDir, filename)

    Archive(base).extractall(filename)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("You can also give filename as a command line argument")
        filename = input("Give your path file name: ")
    else:
        filename = sys.argv[1]
    extract(filename)
