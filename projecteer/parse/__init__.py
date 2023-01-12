# This holds all values all parsers need
"""All parsers for projecteer"""

# CONSTANTS
QUOTE: str = '"'
ESCAPE: str = "\\"
COMMENT: str = "#"
"""The special variable in scripts, that sets the CurrentWorking Directory for all scripts below"""
CWD: str = "CWD"

def escaped(line: str) -> str:
    """
		Returns a str of [line], where all characters after '\\\\'(backslash) have been removed
		
		example:
		```py
			line = "some command with \\"
			escaped(line) # "I didnt doanything
		```
		"""

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
    """
    Converts boolean str-representation to python version (`True`, `False`)

    This means to replace 'true' with 'True' and 'false' with 'False'.  
    To reverse this, use `fromPyBool`
    """
    return value.replace("true", "True").replace("false", "False")

def fromPyBool(value: str) -> str:
    """
    Converts python boolean str-representation to projecteer representaion (`true`, `false`)

    This means to replace 'true' with 'True' and 'false' with 'False'.  
    To reverse this, use `fromPyBool`
    """
    return value.replace("True", "true").replace("False", "false")