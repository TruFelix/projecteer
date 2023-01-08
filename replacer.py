import re
from typing import Any, Dict

PREFIX = "|"
POSTFIX = "|"

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
