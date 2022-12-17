import glob
import os
import re
from pathlib import Path
from sys import argv
from typing import Any, Dict, List

from config_parser import parseProjectConfig

PREFIX = "|"
POSTFIX = "|"
PROJECTEER_FOLDER = ".projecteer"


def findFilesToBeConfigured() -> List[str]:
    paths = []
    # configured sandwiched
    paths += glob.glob('*.configured.*', recursive=True)  # current dir
    paths += glob.glob('**/*.configured.*', recursive=True)  # any sub dir

    # configured in the beginning
    paths += glob.glob('.configured.*', recursive=True)
    paths += glob.glob('**/.configured.*', recursive=True)

    # configured in the end
    paths += glob.glob('*.configured', recursive=True)
    paths += glob.glob('**/*.configured', recursive=True)
    return paths


def replace(content: str, config: Dict[str, Any]):
    replaced = content
    for key, value in config.items():
        matcher = f"{PREFIX}{key}{POSTFIX}"
        replaced = replaced.replace(matcher, str(value))

    # \|(.*?)\|
    regex = re.compile(rf"{re.escape(PREFIX)}(.*?){re.escape(POSTFIX)}")
    matches = re.findall(regex, replaced)
    for match in matches:
        if match != "":
            print(f"NO VARIABLE FOUND FOR: {match}")

    return replaced

##################################################################
### MAIN #########################################################
##################################################################


if __name__ == "__main__":
    if '--cleanup'in argv:
        try:
            with open(f"{PROJECTEER_FOLDER}/generatedFiles", 'r') as f:
                print("cleaning up...")
                for file in f:
                    filePath = file.removesuffix("\n")
                    try:
                        os.remove("./"+ filePath)
                        print(f"  removing {filePath}")
                    except FileNotFoundError as fnfe:
                        print(f"  failed, because {filePath} does not exist")
                        
            os.remove(f"{PROJECTEER_FOLDER}/generatedFiles")
            if not os.listdir(PROJECTEER_FOLDER):
                os.rmdir(PROJECTEER_FOLDER)
        except FileNotFoundError as fnfe:
            print("No generated Files...")
        exit(0)
        

    allReplacedFilePaths = []

    print("loading project configuration ...")
    with open('project.config', 'r') as f:
        configContent = f.readlines()

        projectConfig = None
        try:
            projectConfig = parseProjectConfig(configContent)
        except Exception as e:
            print(e)
            exit(-1)
        # print(str(projectConfig))

    print("looking for files to be configured...")
    filePaths = findFilesToBeConfigured()

    print("Creating/updating files...")
    for filePath in filePaths:
        with open(filePath, 'r') as f:
            content = "".join(f.readlines())
            replaced = replace(content, projectConfig)

            fileName = os.path.basename(filePath)
            replacedFilePath = filePath.replace(".configured", "")
            replacedFileName = os.path.basename(replacedFilePath)
            #  replacedFilePath

            doing = "updating" if os.path.exists(
                replacedFilePath) else "creating"
            print(f"  {doing} {replacedFilePath}")
            with open(replacedFilePath, 'w') as w:
                w.write(replaced)
                allReplacedFilePaths.append(replacedFilePath)
                # if input(f"write to {filename}?") == 'Y':
                #     w.write(replaced)
                # else:
                #     print("done nothing")

    os.makedirs(PROJECTEER_FOLDER, exist_ok=True)
    with open(PROJECTEER_FOLDER+"/generatedFiles", 'a') as f:
        pass
    tmp=None
    with open(PROJECTEER_FOLDER+"/generatedFiles", "r") as f:
        alreadyGenerated = f.read().splitlines()
        alreadyGenerated.extend(allReplacedFilePaths)
        
        tmp = list(set(alreadyGenerated))

    with open(PROJECTEER_FOLDER+"/generatedFiles", 'w') as f:
        f.writelines("\n".join(tmp))
