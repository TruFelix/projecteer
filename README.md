# Projecteer
This is a tool for all people doing many projects.

This should:
* configuration
* help you with Project setup

## Getting started
To get started create a `project.config` file in the root of your project.
> This will be the last config file I promise

In it write a format like dotenv:
`[VARIABLENAME]=[EXPRESSION]`

But unlike dotenv, the `EXPRESSION` can also be a calculation (any python expression in that regard), thus strings have to be contained in `"` quotes.


## Configuration
Projecteer helps you to configure your *project* not your *application*.
The difference being that a project can be anything, also multiple applications