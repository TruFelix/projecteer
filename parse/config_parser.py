"""This file contains EVERYTHING to enable parsing of the config"""

from typing import Any, Dict, List
from replacer import replace

from parse import *


class ConfigParser:
    def __init__(self):
        """A dictionary holding all values parsed from the config"""
        self.variables: Dict[str, Any] = {}
        self.loaded = False

    def parse(self, lines: List[str]):
        # need lineNum for SyntaxError traces
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
                self.parseLine(line)
            except ValueError as ve:
                raise SyntaxError(f"Syntax error in line {lineNum}:\n  {line}\n  {str(ve)}")

        # convert all bools to python bools
        for k, _v in self.variables.items():
            if isinstance(self.variables[k], bool):
                self.variables[k] = fromPyBool(str(self.variables[k]))

        self.loaded = True
        
        # filter magical entries out of the dictionary
        self.variables = {k: v for k, v in self.variables.items() if not k.startswith("__")}
        return self.variables

    def parseLine(self, line: str, replace: bool = False):
        [key, value] = line.replace("\n", "").split("=")
        self.tryAsNumber(key, value)
        self.tryAsString(key, value)
        self.tryAsExpression(key, value)
        if replace:
            self.variables[key] = self.replace(str(self.variables[key]))

    def replace(self, text: str):
        return replace(text, self.variables)

    def tryAsNumber(self, key: str, value: str):
        """Tries to parse as a Number, otherwise does nothing"""

        i = 0
        char = value[i]
        while i in range(len(value)-1) and char.isnumeric():
            char = value[i]
            nextChar = value[i+1]

            if char.isnumeric() and not nextChar.isnumeric():
                parsed = float(value[0:i+1])
                self.variables[key] = parsed
                return parsed

            i += 1

    def tryAsString(self, key: str, value: str):
        """Tries to parse as a String, otherwise does nothing"""

        escapedString = escaped(value)
        if QUOTE in escapedString:
            firstIndex = value.find(QUOTE)
            lastIndex = value.rfind(QUOTE)
            if firstIndex == -1 or lastIndex == -1:
                raise Exception(f"Closing quote({QUOTE}) not found")
            parsed = value[firstIndex:lastIndex+1]
            self.variables[key] = parsed
            return parsed

    def tryAsExpression(self, key: str, value: str):
        """Tries to parse as an Expression, otherwise does nothing"""

        value = toPyBool(value)
        try:
            self.variables[key] = eval(value, self.variables)
        except SyntaxError as se:
            quotedValue = f'\"{value}\"'
            self.variables[key] = eval(quotedValue, self.variables)        
