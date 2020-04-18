#!/usr/bin/python3
#Muisto: A Nostalgic Modern Static Site Generator
#Developer: Mamoru Itoi(@MamoruItoi)


import sys

import main as muisto


#メイン関数
def main():
    try:
        fileName = sys.argv[1]
        if fileName == ".":
            muisto.main()
        elif fileName == "418":
            print("\033[1;31m[Error!]\033[1;m I'm a tea pot.")
        else:
            print("\033[1;31m[Error!]\033[1;m What's that?")
    except IndexError:
        print("\033[1;31m[Error!]\033[1;m Not found the file.")
