import fnmatch
import os
from sys import argv

from termcolor import colored, cprint

from parse.config_parser import ConfigParser

SRC_FOLDERS_VARNAME="SRC_FOLDERS"

def stats(projectConfig: ConfigParser):
	"""prints some stats about the project"""
	totalFiles = []

	srcFolders = projectConfig.variables[SRC_FOLDERS_VARNAME] if SRC_FOLDERS_VARNAME in projectConfig.variables.keys() else ['.']
	for arg in argv[2:]:
		srcFolders.append(arg)
		
	excludes = [".*", ".projecteer"]

	for srcFolder in srcFolders:
		if srcFolder.startswith("!"):
			excludes.append(srcFolder[1:].replace("\\", "/"))
			srcFolders.remove(srcFolder)
	
	cprint("Using the following for calculation:", "blue")
	cprint(f"  srcFolders: " + ", ".join(srcFolders), 'blue')
	cprint(f"  excludes: " + ", ".join(excludes), 'blue')

	for srcFolder in srcFolders:
		for file in getFiles(srcFolder, excludes):

			totalFiles.append(file)
	
	for file in list(totalFiles):
		if '.configured' in file and file.replace('.configured', "") in totalFiles:
			totalFiles.remove(file.replace('.configured', ""))

	totalFilesStr = colored(str(len(totalFiles)), "green", attrs=["bold"])
	print(f"TotalFiles: {totalFilesStr}")

	count = 0
	for file in totalFiles:
		count += countLines(file)
	countStr = colored(str(count), "green", attrs=["bold"])
	print(f"{countStr} Lines of code")

def getFiles(dir: str, excludes):
	allFiles = []
	for root, dirs, files in os.walk(dir, topdown=True):
		for d in list(dirs):
			joined = root.replace("\\", "/") + "/" + d.replace("\\", "/")
			for exlcude in excludes:
				if(fnmatch.fnmatch(d, exlcude)):
					try:
						dirs.remove(d)
					except:
						pass

			if joined in excludes:
				try:
					dirs.remove(d)
				except:
					pass

		for file in files:
			# matches = False
			# for exlcude in excludes:
			# 	if fnmatch.fnmatch(file, exlcude):
			# 		matches=True
			# 		break

			# if matches:
			# 	continue

			allFiles.append(root.replace("\\", "/") + "/" + file)
	return allFiles

def countLines(file):
	lines = []
	try:
		with open(file, 'r') as f:
			lines = f.readlines()
	except UnicodeDecodeError:
		pass
	return len(lines)