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

import yaml

from parse import *
from parse.config_parser import ConfigParser
from replacer import replace

from termcolor import COLORS, colored, cprint


def startScript(scriptAndArgs: str, projectConfig: ConfigParser):
	"""
	Starts the script with given name and potential arguments
	Has to be in the form "SCRIPT_NAME [ARG1] [ARG2] [ARG3]..."
	"""
	splits = scriptAndArgs.split(" ")
	name = splits[0]
	script = findScript(name, projectConfig)
	
	if not CWD in projectConfig.variables.keys():
		projectConfig.variables[CWD] = os.path.abspath(".")

	cprint(f"Executing script '{name}' in {projectConfig.variables[CWD]}", "green")
	os.chdir(projectConfig.variables[CWD])
	
	args = " ".join(splits[1:])
	cmd = f"{script} {args}"
	
	print("\t" + cmd)
	os.system(cmd)

def findScript(name: str, projectConfig: ConfigParser):
	"""Tries to find a script with 'name' and returns the replaced script-content"""
	with open('project.scripts', 'r') as scriptsFile:
		for line in scriptsFile:
			if "=" in line:
				if CWD in line:
					projectConfig.parseLine(line, replace=True)
					cprint(f"  Setting CWD: {projectConfig.variables[CWD]}", "yellow")
				continue
			
			if COMMENT in line or line == "" or line.isspace():
				continue

			[scriptName, script] = line.split(":")
			if scriptName == name:
				# print(f"replacing: {script}, {projectConfig.variables}")
				return replace(script, projectConfig.variables)