# Projecteer

This is a tool for all people doing many projects.

This should:

- configuration
- help you with Project setup

## Getting started

To get started create a `project.config` file in the root of your project.

> This will be the last config file I promise

In it write a format like dotenv:
`[VARIABLENAME]=[EXPRESSION]`

But unlike dotenv, the `EXPRESSION` can also be a calculation (any python expression in that regard), thus strings have to be contained in `"` quotes.

## Configuration

Projecteer helps you to configure your _project_ not your _application_.
The difference being that a project can be anything, also multiple applications

## Best practices

Projecteer is designed to update other config formats, not sourcecode, though undoubtedly it will do that.
The reason for not using it to configure sourcecode is that you will end up with many duplicate files in your sourcecode folders.

So it is encouraged to let projecteer configure:
* .env files
* dockerfiles
	* docker-compose
* deployment files
	* k8s files
	* custom scripts
		this is discuraged, if possible, because you should also use config files
* .config
* .eslint
* api-specs
* documentation