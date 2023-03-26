from typing import List

import jsonpickle

class Position:
    def __init__(self,x:int,y:int) -> None:
        self.x = x
        self.y = y
        pass
    def toTuple(self):
        return (self.x,self.y)
    def __str__(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)

class SimplePosition:
    def __init__(self,fromPosition:int,toPosition:int) -> None:
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        pass
    def __str__(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)

class Door(SimplePosition):
    def __init__(self,fromPosition:int,toPosition:int,hinge:int,openLeft:bool,style:str) -> None:
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        self.hinge = hinge
        self.openLeft = openLeft
        self.style = style
        pass
    def __str__(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)

class Window(SimplePosition):
    def __init__(self,fromPosition:int,toPosition:int,style:str) -> None:
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        self.style = style
        pass
    def __str__(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)

class Wall(SimplePosition):
    def __init__(self,fromPosition:Position,toPosition:Position,isHorizontal:bool,isOuterWall:bool,doors:List[Door],windows:List[Window]) -> None:
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        self.isHorizontal = isHorizontal
        self.isOuterWall = isOuterWall
        self.doors = doors
        self.windows = windows
        pass
    def __str__(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)

class Junction:
    def __init__(self,success:bool,walls:None) -> None:
        self.success = success
        pass
    def __str__(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)

class APIResponse:
    def __init__(self,success:bool,walls:List[Wall],junctions:List[Junction]) -> None:
        self.success = success
        self.walls = walls
        self.junctions = junctions
        pass
    def __str__(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)