# Projecteer

This is a tool for all people doing many projects.

This should:

- configuration
- help you with Project setup

## Getting started

The easiest way to install Projecteer is to use pip:  
`pip install projecteer`

To get started create a `project.config` file in the root of your project.  
> This will be the last config file I promise

In it write a format like dotenv:
`[VARIABLENAME]=[EXPRESSION]`

But unlike dotenv, the `EXPRESSION` can also be a calculation (any python expression in that regard), thus strings have to be contained in `"` quotes.

After that you can use the `|VARIABLENAME|` in **ANY** file, just mark it as `.configured` somewhere in the name
> eg:
> `.configured.env`
> `mySite.configured.html`
> `docker-compose.configured.yaml`

When working with git:
add `|PROJECTEER_GENERATED_FILES|` to your `.gitignore`, to not check them into source-control

For your scripts:
add a `project.scripts` file and add your scripts like so:
`SCRIPTNAME: SCRIPT-COMMAND WITH |VARIABLES|`
if you have multiple commands that should be executed from the same working-directory:
`CWD = ./even/here/|VARIABLES|`

For a better understanding, please look at the [example](./example/).

## Configuration

Projecteer helps you to configure your _project_ not your _application_.
The difference being that a project can be anything, also multiple applications.

Learn about the [Best practices](#best-practices) to make the most out of projecteer and not get frustrated.

### Variables
Lets say you have a backend and a frontend, and they should communicate over http.
You set the port to be `8080` for now. Now later in your development, you decide 8080 is garbage, i need `80`
then you would have to set that value in both frontend and backend. That isnt too bad, but once you have your dockerfiles,
deployment scripts/configs, custom scripts, npm start scripts and what not, it can become tedious.

Projecteer allows you to set your **CONFIG** Variables in **ONE** place.

### Scripts
Take that example, your backend is an nodeJs application and you have some npm-scripts, as well as another project written in dart/flutter:

You can create a script to get everything up and running with one command:
`projecteer setup` or `projecteer install`, however you like, this can be achieved by:
`setup: cd |BACKEND_DIR| && npm i && cd ../|FRONTEND_DIR| && flutter pub get`

You can set a working directory inside the scripts file for all commands below:
`CWD=./someWrkdir`
`CWD=./|someVariable|/somethingElse`

## Commands
### Cleanup
You don't need to worry about projecteer not keeping everything tidy, but if you do have issues, there is this command:

`projecteer cleanup`

This will remove all generated files.

### Special commands
Ever wondered, how many lines of code you have written in 534 files?
Well projecteer can help you with that and more:

`projecteer stats`

This command will use the array of source-folders as specified with `SRC_FOLDERS`.
You can use and `!` in front of a folder to exclude it from the calculation
Per default it will use `.` and exclude `.*` and `.projecteer`, which will be always excluded

## Best practices

Projecteer is designed to update other config formats, not sourcecode, though undoubtedly it will do that.
The reason for not using it to configure sourcecode is that you will end up with many duplicate files in your sourcecode folders.

So it is encouraged to let projecteer configure:
* config-files
	* .env files
	* .config
	* .eslint
	* and what not
* dockerfiles
	* docker-compose
* deployment files
	* k8s files
	* custom scripts
		this is discuraged, if possible, because you should also use config files
* api-specs
* documentation