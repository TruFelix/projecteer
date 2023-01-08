import fnmatch
from parse.config_parser import ConfigParser
import os

SRC_FOLDERS_VARNAME="SRC_FOLDERS"

def stats(projectConfig: ConfigParser):
	"""prints some stats about the project"""
	totalFiles = []

	srcFolders = projectConfig.variables[SRC_FOLDERS_VARNAME]
	excludes = [".*", ".projecteer"]

	for srcFolder in srcFolders:
		if srcFolder.startswith("!"):
			excludes.append(srcFolder[1:].replace("\\", "/"))
			srcFolders.remove(srcFolder)
	
	print(f"srcFolders: {srcFolders}")
	print(f"excludes: {excludes}")

	for srcFolder in srcFolders:
		for file in getFiles(srcFolder, excludes):

			totalFiles.append(file)
	
	totalFiles = list(filter(lambda x: '.configured' not in x, totalFiles))
	print(totalFiles)
	print(f"TotalFiles: {len(totalFiles)}")

	count = 0
	for file in totalFiles:
		count += countLines(file)
	print(f"{count} Lines of code")

def getFiles(dir: str, excludes):
	allFiles = []
	for root, dirs, files in os.walk(dir, topdown=True):
		for d in list(dirs):
			joined = root.replace("\\", "/") + "/" + d.replace("\\", "/")
			for exlcude in excludes:
				if(fnmatch.fnmatch(d, exlcude)):
					try:
						pass
						dirs.remove(d)
					except:
						pass

			if joined in excludes:
				dirs.remove(d)

		for file in files:
			# matches = False
			# for exlcude in excludes:
			# 	if fnmatch.fnmatch(file, exlcude):
			# 		matches=True
			# 		break

			# if matches:
			# 	continue

			print(file)
			allFiles.append(root.replace("\\", "/") + "/" + file)
	return allFiles

def countLines(file):
	lines = []
	with open(file, 'r') as f:
		lines = f.readlines()
	return len(lines)