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


def configureFile(filePath: str, silent: bool = False):
    with open(filePath, 'r') as f:
        fileContent = "".join(f.readlines())

    replacedFileContent = replace(fileContent, projectConfig.variables)

    fileName = os.path.basename(filePath)
    generatedFilePath = filePath.replace(".configured", "")
    generateadFileName = os.path.basename(generatedFilePath)

    if not silent:
        doing = None
        if fileContent == replacedFileContent:
            doing = colored("nothing", "yellow", attrs=["bold"]) + " This file is marked as being generated, but nothing was replaced, please check:"
        elif os.path.exists(generatedFilePath):
            with open(generatedFilePath, 'r') as f:
                alreadyGeneratedFileContent = "".join(f.readlines())
            if alreadyGeneratedFileContent == replacedFileContent:
                doing = colored("checked", "grey")
            else: 
                doing = colored("updating", "yellow")
        else:
            doing = colored("creating", "green")
        print(f"  {doing} {generatedFilePath}")

    # actually write
    with open(generatedFilePath, 'w') as w:
        w.write(replacedFileContent)


def configureProject(silent: bool = False):
    cprint("Creating/updating files...", "yellow", attrs=["bold"])
    if not silent: cprint("looking for files to be configured...")
    filePaths = findFilesToBeConfigured()

    updateGeneratedFilePaths = generateSpecialVariables(projectConfig.variables)

    for filePath in filePaths:
        configureFile(filePath, silent)

    updateGeneratedFilePaths()


def loadProjectConfig():
    """Load the whole projectConfig as by using `parseProjectConfig`"""
    if projectConfig.loaded:
        return projectConfig.variables
    heading = "loading project configuration..."
    cprint(heading, "yellow")

    if not os.path.exists(PROJECT_CONFIG_FILE):
        cursorLineUpStart(1)
        cursorSetHorizontal(len(heading)+1)
        cprint("failed", "red", attrs=["bold"])
        cprint(
            f"'{PROJECT_CONFIG_FILE}' does not exist...are you executing in the correct directory?", "red")
        exit(-1)
    with open('project.config', 'r') as f:
        configContent = f.readlines()

    try:
        return projectConfig.parse(configContent)
    except Exception as e:
        print(e)
        exit(-1)


"""
A dictionary, where the key is a filter function.
If true, it should be executed.
It should be possible to execute only one cmd at a time, the first found should be executed.

Before executing any function contained in this, execute `loadProjectConfig`, if "loadProjectConfig" is True
"""
cmds = {
    lambda argv: '--cleanup' in argv: 
        {"name": "cleanup", "func": cleanup, "loadProjectConfig": False},
    lambda argv: True: 
        {"name": "configureProject", "func": lambda: configureProject(silent=len(argv)>1), "loadProjectConfig": True},
    lambda argv: 'stats' in argv:
        {"name": "stats", "func": lambda: stats(projectConfig), "loadProjectConfig": True},
    lambda argv: len(argv) > 1 and not 'stats' in argv: 
        {"name": "startScript", "func": lambda: startScript(" ".join(argv[1:]), projectConfig), "loadProjectConfig": True},
}


def executeCmd(cmdAndArgs):
    """This handles the execution of cmdName, including loading the projectconfig"""

    cmdName = " ".join(cmdAndArgs[1:])

    i = 0
    for checker, cmd in cmds.items():
        if checker(argv):
            if (cmd["loadProjectConfig"]):
                loadProjectConfig()
            cmdNm = cmd["name"]
            # cprint(f"Executing: {cmdNm} | {cmdName}", "green")
            cmd["func"]()
        i += 1


if __name__ == "__main__":
    executeCmd(argv)
    # if '--cleanup' in argv:
    #     cleanup()

    # if len(argv) > 1:
    #     # handle script
    #     startScript(" ".join(argv[1:]))
    #     exit(0)
