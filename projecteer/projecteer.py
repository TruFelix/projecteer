"""This is the actual CLI"""

import os
from sys import argv
from typing import Dict

from termcolor import COLORS, colored, cprint

from cli_tools.cursor import *
from cmds.cleanup import cleanup
from cmds.stats import stats
from manager import (PROJECT_CONFIG_FILE, findFilesToBeConfigured,
                     generateSpecialVariables)
from parse.config_parser import ConfigParser
from parse.script_parser import startScript
from replacer import replace

projectConfig = ConfigParser()

print("projectConfig: " + str(projectConfig))

linesAfter=0

def configureFile(filePath: str, silent: bool = False):
    global linesAfter
    with open(filePath, 'r') as f:
        fileContent = "".join(f.readlines())

    replacedFileContent = replace(fileContent, projectConfig.variables)

    fileName = os.path.basename(filePath)
    generatedFilePath = filePath.replace(".configured", "")
    generateadFileName = os.path.basename(generatedFilePath)

    didSomething = True
    if not silent:
        doing = None
        if fileContent == replacedFileContent:
            doing = colored("nothing", "yellow", attrs=["bold"]) + " This file is marked as being generated, but nothing was replaced, please check:"
        elif os.path.exists(generatedFilePath):
            with open(generatedFilePath, 'r') as f:
                alreadyGeneratedFileContent = "".join(f.readlines())
            if alreadyGeneratedFileContent == replacedFileContent:
                doing = colored("checked", "grey")
                didSomething = False
            else: 
                doing = colored("updating", "yellow")
        else:
            doing = colored("creating", "green")
        print(f"  {doing} {generatedFilePath}")
        linesAfter += 1

    # actually write
    if didSomething:
        with open(generatedFilePath, 'w') as w:
            w.write(replacedFileContent)
    
    return didSomething


def configureProject(silent: bool = False):
    global linesAfter
    cprint("Creating/updating files...", "yellow", attrs=["bold"])
    if not silent: cprint("looking for files to be configured...")
    filePaths = findFilesToBeConfigured()

    updateGeneratedFilePaths = generateSpecialVariables(projectConfig.variables)

    didSomething= False
    linesAfter = 0
    for filePath in filePaths:
        if configureFile(filePath, silent):
            didSomething = True

    if not didSomething:
        # cursorLineUpStart(linesAfter)
        cprint("EVERYTHING UP TO DATE", "green", attrs=["bold"])

    updateGeneratedFilePaths()


def loadProjectConfig():
    global linesAfter
    """Load the whole projectConfig as by using `parseProjectConfig`"""
    if projectConfig.loaded:
        return projectConfig.variables
    
    heading = "loading project configuration..."
    cprint(heading, "yellow")
    linesAfter = 0

    CWD = os.getcwd()
    dirs = CWD.split(os.sep)
    cDirs = list(dirs)
    def cDir(): return os.sep.join(cDirs) + os.sep + PROJECT_CONFIG_FILE
    while not os.path.exists(cDir()) and len(cDirs) > 1:
        tmpRoot = cDir()[:-len(PROJECT_CONFIG_FILE) - 1]
        print(f"  Searched in {tmpRoot}")
        linesAfter += 1
        cDirs.pop()
    
    foundConfigFile = cDir()
    foundRoot = os.sep.join(foundConfigFile.split(os.sep)[:-1])
    if not os.path.exists(foundConfigFile):
        cursorLineUpStart(linesAfter + 1)
        cursorSetHorizontal(len(heading)+1)
        cprint("failed", "red", attrs=["bold"])
        cursorLineDownStart(linesAfter)
        cprint(
            f"'{PROJECT_CONFIG_FILE}' does not exist...are you executing in the correct directory?", "red")
        exit(-1)
    
    cursorLineUpStart(linesAfter)
    cursorSetHorizontal(len(heading) + 1)
    cprint('found','green')
    cprint(f"  config at {foundConfigFile}", "cyan")
    # cprint(f"  root: {foundRoot}", "cyan")
    with open(foundConfigFile, 'r') as f:
        configContent = f.readlines()

    try:
        projectConfig.parse(configContent)
        projectConfig.configRoot = foundRoot
        return projectConfig.variables
    except Exception as e:
        print(e)
        exit(-1)


"""
A dictionary, where the key is a filter function.
If true, it should be executed.
It should be possible to execute only one cmd at a time, the first found should be executed.

Before executing any function contained in this, execute `loadProjectConfig`, if "loadProjectConfig" is True
if `single` is True, don't execute any other script below
"""
cmds = {
    lambda argv: 'cleanup' in argv: 
        {"name": "clean", "func": cleanup, "loadProjectConfig": False, "single": True},
    lambda argv: 'stats' in argv:
        {"name": "stats", "func": lambda: stats(projectConfig), "loadProjectConfig": True, "single": True},
    lambda argv: True: 
        {"name": "configureProject", "func": lambda: configureProject(silent=len(argv)>1), "loadProjectConfig": True, "single": False},
    lambda argv: len(argv) > 1: 
        {"name": "startScript", "func": lambda: startScript(" ".join(argv[1:]), projectConfig), "loadProjectConfig": True, "single": False},
}


def executeCmd(cmdAndArgs):
    """This handles the execution of cmdName, including loading the projectconfig"""

    for checker, cmd in cmds.items():
        if checker(cmdAndArgs):
            if (cmd["loadProjectConfig"]):
                loadProjectConfig()

            cmd["func"]()
            if cmd["single"]:
                return


def main():
    executeCmd(argv)

if __name__ == "__main__":
    main()