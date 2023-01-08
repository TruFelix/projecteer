from typing import List

from cursor import CursorHandler, cursorCurrentPosition, cursorSetPosition


class ActionHandler:
    """
    eg:
    ```
    loading XY...
    some content
    more content
    ```

    ```
    loading XY...
    some content
    more content
    ERROR
    ```

    ```
    loading XY...failed
    some content
    more content
    ERROR
    ```
    """

    def __init__(self, cursorHandler: CursorHandler = None):
        """Stack for the headers"""
        self.cHandler = CursorHandler() if cursorHandler is None else cursorHandler
        self.headers: List[Head] = []

    def printHead(self, head: str):
        header = Head(head)
        self.headers.append(header)
        header.print(printer=self.cHandler.print)
        header.position=self.cHandler.relativePosition

    def result(self, result: str):
        head = self.headers.pop()
        oldPosition = cursorCurrentPosition()
        cursorSetPosition(x=head.position[0], y=head.position[1])
        self.cHandler.print(result)
        cursorSetPosition(x=oldPosition[0], y=oldPosition[1])
    
    def dump(self):
      print(f"ActionHandler")
      print(f"  cHandler")
      print(f"    startPoint: {self.cHandler.startPoint}")


class Head:
    def __init__(self, head: str) -> None:
        self.head = head
        self.position = None

    def print(self, printer=print):
        print(self.head)
        self.position = cursorCurrentPosition()


if __name__ == "__main__":
    import time
    cH = CursorHandler()
    cH.print("Testing runningAction from cli_tools")

    handler = ActionHandler()
    time.sleep(5)
    handler.cHandler.setPosition(0,0)
    handler.printHead("Loading something...")
    cH.print("  some results from the loading")
    handler.result("success")
