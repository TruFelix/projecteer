import os
from sys import argv

from termcolor import colored, cprint

from manager import PROJECTEER_FOLDER


def cleanup():
    try:
        with open(f"{PROJECTEER_FOLDER}/generatedFiles", 'r') as f:
            print("cleaning up...")
            for file in f:
                filePath = file.removesuffix("\n")
                try:
                    printRemovalOfFile(filePath)
                    os.remove("./" + filePath)
                except FileNotFoundError as fnfe:
                    cprint(f"  failed, because {filePath} does not exist", "red")
        
        os.remove(f"{PROJECTEER_FOLDER}/generatedFiles")
        if not os.listdir(PROJECTEER_FOLDER):
            os.rmdir(PROJECTEER_FOLDER)
            
    except FileNotFoundError as fnfe:
        cprint("No generated Files recorded...", 'red')

    foundOne = False
    for root, dir, files in os.walk("./"):
        for file in files:
            if ".configured" in file:
                generatedFileName = (root + '/' + file.replace(".configured", "")).replace("//", '/')
                if os.path.exists(generatedFileName):
                    foundOne = True
                    printRemovalOfFile(generatedFileName)
                    os.remove(generatedFileName)

    if not foundOne:
        cprint("Found no generated Files via search", 'yellow', attrs=["bold"])

def printRemovalOfFile(filePath):
    removing = colored("removing", "red")
    print(f"  {removing} {filePath}")
