def cleanup():
    try:
        with open(f"{PROJECTEER_FOLDER}/generatedFiles", 'r') as f:
            print("cleaning up...")
            for file in f:
                filePath = file.removesuffix("\n")
                try:
                    os.remove("./" + filePath)
                    print(f"  removing {filePath}")
                except FileNotFoundError as fnfe:
                    print(f"  failed, because {filePath} does not exist")

        os.remove(f"{PROJECTEER_FOLDER}/generatedFiles")
        if not os.listdir(PROJECTEER_FOLDER):
            os.rmdir(PROJECTEER_FOLDER)
    except FileNotFoundError as fnfe:
        print("No generated Files...")
    exit(0)
