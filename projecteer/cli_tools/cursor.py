import re
import sys

if(sys.platform == "win32"):
    import ctypes
    from ctypes import wintypes
else:
    import termios


def _cursorPrint(msg: str):
    print(msg, end="")


def cursorUp(up: int = 1):
    _cursorPrint(f"\033[{up}A")


def cursorDown(down: int = 1):
    _cursorPrint(f"\033[{down}B")


def cursorRight(right: int = 1):
    _cursorPrint(f"\033[{right}C")


def cursorLeft(left: int = 1):
    _cursorPrint(f"\033[{left}D")


def cursorLineDownStart(lines: int = 1):
    _cursorPrint(f"\033[{lines}E")


def cursorLineUpStart(lines: int = 1):
    _cursorPrint(f"\033[{lines}F")


def cursorSetHorizontal(y: int = 1):
    _cursorPrint(f"\033[{y}G")


def cursorSetPosition(x: int = 1, y: int = 1):
    _cursorPrint(f"\033[{y};{x}f")


def cursorMove(x: int = 0, y: int = 0):
    if x != 0:
        if x > 0:
            cursorRight(x)
        else:
            cursorLeft(x)

    if y != 0:
        if y > 0:
            cursorUp(y)
        else:
            cursorDown(y)


def cursorCurrentPosition():
    if(sys.platform == "win32"):
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        OldStdinMode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)

    try:
        _ = ""
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            True
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
    finally:
        # set echo state back
        if(sys.platform == "win32"):
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
        else:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)

    return(int(res.group("x")), int(res.group("y")))


class CursorHandler:
    def __init__(self, startPoint=None):
        self.lines = 0
        self.startPoint = cursorCurrentPosition() if startPoint is None else startPoint

    def absolutePosition(self, relativeFromStart):
        """Returns a tuple position that is absolute, given a relative position from 'startPoint'"""
        [x, y] = self.startPoint
        return (relativeFromStart[0] + x, relativeFromStart[1] + y)

    def relativePosition(self, absolute):
        [x, y] = self.startPoint
        return (absolute[0] - x, absolute[1]-y)

    def setPosition(self, x: int = 0, y: int = 0):
        """Sets the position of the cursor relative to 'startPoint'"""
        relY = self.lines - y
        if relY != 0:
            if relY < 0:
                cursorDown(relY)
            else:
                cursorUp(relY)
        
        relX = 0
        
                
        # pos = self.absolutePosition((x, y))
        # cursorSetPosition(x=pos[0], y=pos[1])

    def print(self, msg="", end='\n'):
        self.lines += 1
        print(msg, end=end)

    def currentPos(self):
        return (cursorCurrentPosition()[0], self.lines)


if __name__ == "__main__":
    print("Testing cursor from cli_tools...")

    cHandler = CursorHandler()

    for y in range(5):
        for x in range(5):
            print(f"{x}", end="")
        cHandler.print()

    # startPos = cHandler.currentPos()
    finish = cHandler.currentPos()

    cHandler.setPosition(x=3, y=1)
    print("X", end="")

    cHandler.setPosition(x=finish[0], y=finish[1])
