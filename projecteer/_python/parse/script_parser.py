"""
This file contains EVERYTHING to enable parsing of the scripts

Scripts are located in the project.scripts file
a script is a shell-command (depending on the os)

To specify a custom working directory for all commands below
specify:
`CWD=./some/directory`
it can also be an absolute path:
`CWD=C:/some/directory`
`CWD=/home/some/directory`
"""

import os
from typing import Any, Dict, List

from termcolor import COLORS, colored, cprint

from parse import *
from parse.config_parser import ConfigParser
from manager import PROJECT_SCRIPT_FILE
from replacer import replace


def startScript(scriptAndArgs: str, projectConfig: ConfigParser):
	"""
	Starts the script with given name and potential arguments
	Has to be in the form "SCRIPT_NAME [ARG1] [ARG2] [ARG3]..."
	"""
	splits = scriptAndArgs.split(" ")
	name = splits[0]
	script = findScript(name, projectConfig)

	if script is None:
		cprint(f"Couldn't find script with name '{name}'", "yellow", attrs=["bold"])
		return
	
	if not CWD in projectConfig.variables.keys():
		projectConfig.variables[CWD] = os.path.abspath(".")

	cprint(f"Executing script '{name}' in {projectConfig.variables[CWD]}", "green")
	os.chdir(projectConfig.configRoot + os.sep + projectConfig.variables[CWD])
	
	args = " ".join(splits[1:])
	cmd = f"{script} {args}"
	
	print("\t" + cmd)
	os.system(cmd)

def findScript(name: str, projectConfig: ConfigParser):
	"""Tries to find a script with 'name' and returns the replaced script-content"""
	with open(projectConfig.configRoot + os.sep + PROJECT_SCRIPT_FILE, 'r') as scriptsFile:
		for line in scriptsFile:
			if "=" in line:
				if CWD in line:
					projectConfig.parseLine(line, replace=True)
					cprint(f"  Setting CWD: {projectConfig.variables[CWD]}", "yellow")
				continue
			
			if COMMENT in line or line == "" or line.isspace():
				continue

			split = line.split(":")
			scriptName = split[0]
			script = ":".join(split[1:])
			if scriptName == name:
				# print(f"replacing: {script}, {projectConfig.variables}")
				return replace(script, projectConfig.variables)