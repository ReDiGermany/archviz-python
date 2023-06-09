import random
from typing import List

import jsonpickle

from APIResponse import APIResponse, Door, Feature, FeatureType, Position, Room, SimplePosition, Wall, Window
from config import CONFIG
from generateCorners import generateCorners

def between(a,x,b):
    return a <= x and x <= b

def betweenPosition(pos,item):
    return between(item.fromPosition,pos,item.toPosition)

def checkIntersecting(arr:List[SimplePosition],fr:int,to:int):
    for item in arr:
        currentInItem = between(fr,item.fromPosition,to) or \
                        between(fr,item.toPosition,to)
        
        itemInCurrent = between(item.fromPosition,fr,item.toPosition) or \
                        between(item.fromPosition,to,item.toPosition)

        if currentInItem or itemInCurrent:
            return True

    return False

def getData():

    rooms = generateCorners()

    print(rooms)
    return parseData(rooms)

def parseData(rooms):
    globalHeight = int(random.randrange(250,300))
    response = APIResponse(success=False,junctions=[],walls=[])
    
    wall_width = CONFIG.getWALL_WIDTH()
    wall_width_half = wall_width/2

    # TODO: Fix window/door overlap
    for idx,room in enumerate(rooms):
        for idx1,room1 in enumerate(room):
            room1["x"] = room1["x"] - (room1["x"] % 20)
            room1["y"] = room1["y"] - (room1["y"] % 20)

    # Remove double points
    for idx,room in enumerate(rooms):
        for idx1,room1 in enumerate(room):
            for idx2,room2 in enumerate(room):
                if idx1!=idx2 and room1["x"]==room2["x"] and room1["y"]==room2["y"]:
                    del room[idx2]

    # Generate empty joints from points
    joints = []
    for idx,y in enumerate(rooms):
        for x in y:
            joints.append({
                "yIndex": idx,
                "left": x["x"],
                "top": x["y"],
                "outerwall": False,
                "corner": {
                    "top": None,
                    "left": None,
                    "bottom": None,
                    "right": None
                },
                "targetIsOuterwall": {
                    "top": False,
                    "left": False,
                    "bottom": False,
                    "right": False
                }})
            
    # Connect joints together
    for idx,room in enumerate(joints):
        for idx1,room1 in enumerate(joints):
            if room["left"] > room1["left"] and room["top"]==room1["top"] and (room["corner"]["left"]==None or room["left"] > joints[room["corner"]["left"]]["left"]):
                room["corner"]["left"]=idx1

            if room["left"] < room1["left"] and room["top"]==room1["top"] and (room["corner"]["right"]==None or room["left"] > joints[room["corner"]["right"]]["left"]):
                room["corner"]["right"]=idx1

            if room["top"] > room1["top"] and room["left"]==room1["left"] and (room["corner"]["top"]==None or room["top"] > joints[room["corner"]["top"]]["top"]):
                if room["yIndex"]==room1["yIndex"]-1 or room["yIndex"]==room1["yIndex"]+1:
                    room["corner"]["top"]=idx1

            if room["top"] < room1["top"] and room["left"]==room1["left"] and (room["corner"]["bottom"]==None or room["top"] > joints[room["corner"]["bottom"]]["top"]):
                if room["yIndex"]==room1["yIndex"]-1 or room["yIndex"]==room1["yIndex"]+1:
                    room["corner"]["bottom"]=idx1

    maxLen = -1

    # Function to loop arround the outer wall to detect it as such
    def traverse(idx,move,n):
        if idx == None:
            return
        n = n+1
        joints[idx]["outerwall"] = True
        current = joints[idx]
        corner = current["corner"]
        if maxLen!=-1 and n > maxLen:
            return
        if move=="right":
            if corner["right"]!=None and joints[corner["right"]]["outerwall"] == False:
                if maxLen>0: print(f"right: {idx} -> "+str(corner["right"]))
                traverse(corner["right"],"right",n)
            elif corner["bottom"]!=None and joints[corner["bottom"]]["outerwall"] == False:
                if maxLen>0: print(f"bottom: {idx} -> "+str(corner["bottom"]))
                traverse(corner["bottom"],"bottom",n)
            elif corner["top"]!=None and joints[corner["top"]]["outerwall"] == False:
                if maxLen>0: print(f"top: {idx} -> "+str(corner["top"]))
                traverse(corner["top"],"top",n)
            elif corner["left"]!=None and joints[corner["left"]]["outerwall"] == False:
                if maxLen>0: print(f"left: {idx} -> "+str(corner["left"]))
                traverse(corner["left"],"left",n)

        if move=="bottom":
            if corner["right"]!=None and joints[corner["right"]]["outerwall"] == False:
                if maxLen>0: print(f"right: {idx} -> "+str(corner["right"]))
                traverse(corner["right"],"right",n)
            elif corner["bottom"]!=None and joints[corner["bottom"]]["outerwall"] == False:
                if maxLen>0: print(f"bottom: {idx} -> "+str(corner["bottom"]))
                traverse(corner["bottom"],"bottom",n)
            elif corner["top"]!=None and joints[corner["top"]]["outerwall"] == False:
                if maxLen>0: print(f"top: {idx} -> "+str(corner["top"]))
                traverse(corner["top"],"top",n)
            elif corner["left"]!=None and joints[corner["left"]]["outerwall"] == False:
                if maxLen>0: print(f"left: {idx} -> "+str(corner["left"]))
                traverse(corner["left"],"left",n)

        if move=="left":
            if corner["bottom"]!=None and joints[corner["bottom"]]["outerwall"] == False:
                if maxLen>0: print(f"bottom: {idx} -> "+str(corner["bottom"]))
                traverse(corner["bottom"],"bottom",n)
            elif corner["left"]!=None and joints[corner["left"]]["outerwall"] == False:
                if maxLen>0: print(f"left: {idx} -> "+str(corner["left"]))
                traverse(corner["left"],"left",n)
            elif corner["right"]!=None and joints[corner["right"]]["outerwall"] == False:
                if maxLen>0: print(f"right: {idx} -> "+str(corner["right"]))
                traverse(corner["right"],"right",n)
            elif corner["top"]!=None and joints[corner["top"]]["outerwall"] == False:
                if maxLen>0: print(f"top: {idx} -> "+str(corner["top"]))
                traverse(corner["top"],"top",n)

        if move=="top":
            if idx!=0:
                if maxLen>0: print(f"top: {idx} -> "+str(corner["top"]))
                traverse(corner["top"],"top",n)

    traverse(0,"right",0)

    # Checking if joint target is also outer wall
    for idx,joint in enumerate(joints):
        if joints[idx]["corner"]["top"]!=None:
            joints[idx]["targetIsOuterwall"]["top"] = joints[joints[idx]["corner"]["top"]]["outerwall"]
        if joints[idx]["corner"]["left"]!=None:
            joints[idx]["targetIsOuterwall"]["left"] = joints[joints[idx]["corner"]["left"]]["outerwall"]
        if joints[idx]["corner"]["bottom"]!=None:
            joints[idx]["targetIsOuterwall"]["bottom"] = joints[joints[idx]["corner"]["bottom"]]["outerwall"]
        if joints[idx]["corner"]["right"]!=None:
            joints[idx]["targetIsOuterwall"]["right"] = joints[joints[idx]["corner"]["right"]]["outerwall"]

    # print(json.dumps(joints,indent=2))

    wallsobj:List[Wall] = []

    # Building walls from joint info (only to right and bottom joints to prevent double casting)
    for idx,x in enumerate(joints):
        depth = int(random.randrange(20,21))
        height = globalHeight #int(random.randrange(250,250))
        # print(x)
        if x["corner"]["right"]:
            wallsobj.append(Wall(
                fromPosition=Position(int(x["left"]+wall_width_half),int(x["top"]-wall_width_half)),
                toPosition=Position(int(joints[x["corner"]["right"]]["left"]-wall_width_half),int(joints[x["corner"]["right"]]["top"]+wall_width_half)),
                isHorizontal=True,
                isOuterWall=x["targetIsOuterwall"]["right"] and x["outerwall"] and (not x["targetIsOuterwall"]["top"] or not x["targetIsOuterwall"]["bottom"]),
                features=[],
                depth=depth,
                height=height,
            ))
            
        if x["corner"]["bottom"]:
            wallsobj.append(Wall(
                fromPosition=Position(int(x["left"]+wall_width_half),int(x["top"]-wall_width_half)),
                toPosition=Position(int(joints[x["corner"]["bottom"]]["left"]-wall_width_half),int(joints[x["corner"]["bottom"]]["top"]+wall_width_half)),
                isHorizontal=False,
                isOuterWall=x["targetIsOuterwall"]["bottom"] and x["outerwall"] and (not x["targetIsOuterwall"]["right"] or not x["targetIsOuterwall"]["left"]),
                features=[],
                depth=depth,
                height=height,
            ))

    # Differencing between inner and outer walls
    outerwalls = []
    innerwalls = []
    for idx,wall in enumerate(wallsobj):
        if wall.isOuterWall:
            outerwalls.append({"idx":idx,"wall":wall})
        else:
            innerwalls.append({"idx":idx,"wall":wall})

    # Adding Doors to outer walls (entrance doors)
    number_of_doors = int(random.randrange(2,3))
    for _ in range(number_of_doors):
        idx = random.randrange(0,len(outerwalls))
        o:Wall = wallsobj[outerwalls[idx]["idx"]]

        doorWidth = int(random.randrange(120,140))

        checkVertical = not o.isHorizontal and len(o.features)==0 and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and len(o.features)==0 and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            toPosition = fromPosition + doorWidth
            hinge = fromPosition if random.random() > 0.5 else toPosition
            intersecting = checkIntersecting(o.features,fromPosition,toPosition)

            if not intersecting:
                o.features.append(Feature(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    hinge = hinge,
                    openLeft = random.random() > 0.5,
                    style = "default",
                    height = int(random.randrange(180,220)),
                    z = 0,
                    type = FeatureType.DOOR
                ))

    # Adding Windows to outer walls
    windowHeight = int(random.randrange(80,150))
    maxWinHeight = wallsobj[0].height - windowHeight  - 80
    if maxWinHeight <= 80:
        maxWinHeight = 85
    windowZ = int(random.randrange(80,maxWinHeight))
    for _ in range(100):
        idx = random.randrange(0,len(outerwalls))
        o:Wall = wallsobj[outerwalls[idx]["idx"]]

        doorWidth = int(random.randrange(80,120))

        checkVertical = not o.isHorizontal and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            fromPosition = fromPosition - (fromPosition % 20)
            toPosition = fromPosition + doorWidth
            toPosition = toPosition - (fromPosition % 20)
            intersecting = checkIntersecting(o.features,fromPosition,toPosition)

            if not intersecting:
                o.features.append(Feature(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    style = "default",
                    height = windowHeight,
                    z = windowZ,
                    type = FeatureType.WINDOW,
                    hinge=-1,
                    openLeft=False
                ))

    # Adding Doors to inner walls
    for wall in innerwalls:
        o:Wall = wallsobj[wall["idx"]]

        doorWidth = int(random.randrange(80,120))

        checkVertical = not o.isHorizontal and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            toPosition = fromPosition + doorWidth
            hinge = fromPosition if random.random() > 0.5 else toPosition
            intersecting = checkIntersecting(o.features,fromPosition,toPosition)

            if not intersecting:
                o.features.append(Feature(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    hinge = hinge,
                    openLeft = random.random() > 0.5,
                    style = "default",
                    height = int(random.randrange(180,220)),
                    z = int(random.randrange(0,5)),
                    type = FeatureType.DOOR
                ))

    # Sorting Wall Features
    for wall in innerwalls:
        o:Wall = wallsobj[wall["idx"]]
        o.features = sorted(o.features,key=lambda x: x.fromPosition,reverse=False)

    # Sorting Wall Features
    for wall in outerwalls:
        o:Wall = wallsobj[wall["idx"]]
        o.features = sorted(o.features,key=lambda x: x.fromPosition,reverse=False)

    response.walls = wallsobj

    n = 0

    # TODO: When grid enabled: fix joint jumping
    # TODO: fix room datapoints. (if top T => no room recognized due to check if bottom and right ==> go as far as needed?)
    rooms:List[Room] = []
    for idx,joint in enumerate(joints):
        if joint["corner"]["bottom"]!=None and joint["corner"]["right"]!=None:
            rightJoint = joint["corner"]["right"]
            bottomRightJoint = joints[rightJoint]["corner"]["bottom"]
            while bottomRightJoint==None:
                if rightJoint!=None:
                    rightJoint = joints[rightJoint]["corner"]["right"]
                    if rightJoint!=None:
                        bottomRightJoint = joints[rightJoint]["corner"]["bottom"]
                else:
                    break
            if bottomRightJoint!=None:
                n = n+1
                # print(f"current = {idx}, right = {rightJoint}, bottom = {bottomRightJoint}")
                targetJoint = joints[bottomRightJoint]
                rooms.append(Room(
                    fromPosition = Position(joint["left"],joint["top"]),
                    toPosition = Position(targetJoint["left"],targetJoint["top"]),
                    ceilingStyle = "default",
                    floorStyle="default",
                ))
    # print(jsonpickle.encode(joints))
    # print(n)

    return wallsobj,joints,rooms
