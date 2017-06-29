#!/usr/bin/python3

import os

from sys import argv as _
from shutil import copyfile
from jsmin import jsmin
from rcssmin import cssmin

VERSION = "0.1.1.0"
verbose = False
FORMATS = {
    "supported": ["js", "css", "htm", "html", "twig"]
}

def copyStructure(originalPath, finalPath):
    """Copy folder structure and start copy and minimize"""
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
    """Copy files which do not support minifer"""
    originList = os.listdir(origin)
    for i in originList:
        part = i.split('.')
        if os.path.isdir(origin+"/"+i):
            if verbose:
                print(final + "/" + i + " has been created")
            os.makedirs(final+"/"+i)
            startCopy(origin+"/"+i, final+"/"+i)
        elif not part[len(part)-1] in FORMATS["supported"]:
            copyfile(origin+"/"+i, final+"/"+i)
            if verbose:
                print(origin + "/" + i + " has been copied")
        else:
            minimizeFile(origin+"/"+i,final+"/"+i,part[len(part)-1])

def minimizeFile(source, production, format):
    """Minify files"""
    input = open(source, "r")
    output = open(production, "w")
    output.write(globals()[format+"min"](input.read()))
    input.close()
    output.close()
    if verbose:
        print(source + " has been minified")

def htmlmin(source):
    """Minify html"""
    ret = ""
    codePre = False #Is inside a code or pre label
    lines = source.split("\n")
    for i in lines:
        if "<!DOCTYPE" in i:
            ret = i+"\n"
        else:
            if "</pre>" in i or "</code>" in i:
                codePre = False
            elif "<pre>" in i or "<code>" in i:
                codePre = True
            if codePre:
                ret += "\n"+i
            else:
                index = 0
                for j in i:
                    if j != " " and j != "\t":
                        break
                    else:
                        index += 1
                i = i[index:]
                ret += i
    return ret

def htmmin(source):
    """Minify htm"""
    return htmlmin(source)

def twigmin(source):
    """Minify twig"""
    return htmlmin(source)

def main():
    """Main activity"""
    if len(_) == 1 or _[1] == "-h":
        help()
    elif _[1] == "-v":
        version()
    elif _[1] == "-m" and len(_) == 4:
        copyStructure(_[2], _[3])
    else:
        help()

def help():
    """Help"""
    print("Usage of minithunder:")
    print("---------------------")
    print("-h:                                          show help")
    print("-v:                                          show version")
    print("-m <Source path> <Production path>:          Minimize project to production")

def version():
    """version"""
    print("MiniThunder - Prepare your software to production")
    print("Version: "+VERSION)

if __name__ == "__main__":
    main()
