# This file contains EVERYTHING to enable parsing

from typing import Any, Dict, List

QUOTE = '"'
ESCAPE = "\\"
COMMENT = "#"

variables: Dict[str, Any] = {}


def parseProjectConfig(lines: List[str]):
    global variables

    for lineNum in range(len(lines)):
        line = lines[lineNum]

        if line.startswith(COMMENT):
            continue

        if line == "\n":
            continue

        if COMMENT in line:
            index = line.find(COMMENT)
            line = line[0:index]

        try:
            parseLine(line)
        except ValueError as ve:
            raise Exception(f"Syntax error in line {lineNum}:\n  {line}\n  {str(ve)}")

    for k, _v in variables.items():
        if isinstance(variables[k], bool):
            variables[k] = fromPyBool(str(variables[k]))

    return {k: v for k, v in variables.items() if not k.startswith("__")}

def parseLine(line: str):
    global variables
    [key, value] = line.split("=")
    tryAsNumber(key, value)
    tryAsString(key, value)
    tryAsExpression(key, value)


def tryAsNumber(key: str, value: str):
    """Tries to parse as a Number, otherwise does nothing"""
    global variables

    i = 0
    char = value[i]
    while i in range(len(value)-1) and char.isnumeric():
        char = value[i]
        nextChar = value[i+1]

        if char.isnumeric() and not nextChar.isnumeric():
            parsed = float(value[0:i+1])
            variables[key] = parsed
            return parsed

        i += 1


def tryAsString(key: str, value: str):
    """Tries to parse as a String, otherwise does nothing"""
    global variables

    escapedString = escaped(value)
    if QUOTE in escapedString:
        firstIndex = value.find(QUOTE)
        lastIndex = value.rfind(QUOTE)
        if firstIndex == -1 or lastIndex == -1:
            raise Exception(f"Closing quote({QUOTE}) not found")
        parsed = value[firstIndex:lastIndex+1]
        variables[key] = parsed
        return parsed


def tryAsExpression(key: str, value: str):
    """Tries to parse as an Expression, otherwise does nothing"""
    global variables

    value = toPyBool(value)

    variables[key] = eval(value, variables)


def escaped(line: str) -> str:
    """Returns a str of [line], where all characters after '\\' have been removed"""

    tmp = ""  # will hold the escaped string
    lastSlice = -2  # starts at -2 because this should be without 'correction' the index of the last slice

    for i in range(len(line)):
        char = line[i]

        if char is ESCAPE:
            tmp += line[lastSlice+2:i]
            lastSlice = i

    tmp += line[lastSlice+2:-1]

    return tmp

def toPyBool(value: str) -> str:
    return value.replace("true", "True").replace("false", "False")

def fromPyBool(value: str) -> str:
    return value.replace("True", "true").replace("False", "false")
