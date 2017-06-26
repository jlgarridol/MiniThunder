#!/usr/bin/python3

import os
import json

from sys import argv as _
from shutil import copyfile
from jsmin import jsmin
from rcssmin import cssmin

VERSION="0.1.0.0"
FORMATS={}
with open('../data/supported.json') as data:
    FORMATS = json.load(data)

def copyStructure(originalPath, finalPath):
    if not os.path.isdir(originalPath):
        raise Exception("The origin directory " + originalPath + " not exists")

    if not os.path.exists(finalPath):
        os.makedirs(finalPath)
    elif not os.path.isdir(finalPath):
        raise Exception("The path " + finalPath + " exists but isn't a directory")
    elif not os.listdir(finalPath) == []:
        raise Exception("The folder " + finalPath + " is not empty")
    startCopy(originalPath, finalPath)


def startCopy(origin, final):
    originList = os.listdir(origin)
    for i in originList:
        part = i.split('.')
        if os.path.isdir(origin+"/"+i):
            os.makedirs(final+"/"+i)
            startCopy(origin+"/"+i, final+"/"+i)
        elif not part[len(part)-1] in FORMATS["supported"]:
            copyfile(origin+"/"+i, final+"/"+i)
        else:
            minimizeFile(origin+"/"+i,final+"/"+i,part[len(part)-1])

def minimizeFile(source, production, format):
    input = open(source, "r")
    output = open(production, "w")
    if format == "js":
        output.write(jsmin(input.read()))
    if format == "css":
        output.write(cssmin(input.read(), keep_bang_comments=False))
    input.close()
    output.close()

def main():
    if len(_) == 1 or _[1] == "-h":
        help()
    elif _[1] == "-v":
        version()
    elif _[1] == "-m" and len(_) == 4:
        copyStructure(_[2], _[3])
    else:
        help()

def help():
    print("Usage of minithunder:")
    print("---------------------")
    print("-h:                                          show help")
    print("-v:                                          show version")
    print("-m <Source path> <Production path>:          Minimize project to production")

def version():
    print("MiniThunder - Prepare your software to production")
    print("Version: "+VERSION)

if __name__ == "__main__":
    main()
