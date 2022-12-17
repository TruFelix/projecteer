from config_parser import parseProjectConfig

if __name__ == "__main__":
	with open('project.config', 'r') as f:
		configContent = f.readlines()

		projectConfig = parseProjectConfig(configContent)
		print(str(projectConfig))