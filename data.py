import random
from typing import List
from APIResponse import APIResponse, Door, Position, SimplePosition, Wall, Window
from config import CONFIG
from generateCorners import generateCorners

def between(a,x,b):
    return a <= x and x <= b

def betweenPosition(pos,item):
    return between(item.fromPosition,pos,item.toPosition)

def checkIntersecting(arr:List[SimplePosition],fr:int,to:int):
    for item in arr:
        currentInItem = betweenPosition(fr,item) or \
                        betweenPosition(to,item)
        
        itemInCurrent = between(item.fromPosition,fr,item.toPosition) or \
                        between(item.fromPosition,to,item.toPosition)
        if currentInItem or itemInCurrent:
            return True
    return False

def getData():
    response = APIResponse(success=False,junctions=[],walls=[])

    rooms = generateCorners()

    # rooms = [[{'x': 100, 'y': 100, 'generated': True}, {'x': 574, 'y': 100, 'generated': True}, {'x': 1044, 'y': 100, 'generated': True}], [{'x': 100, 'y': 325, 'generated': True}, {'x': 100, 'y': 325, 'generated': False}, {'x': 373, 'y': 325, 'generated': True}, {'x': 574, 'y': 325, 'generated': False}, {'x': 612, 'y': 325, 'generated': True}, {'x': 970, 'y': 325, 'generated': True}, {'x': 1044, 'y': 325, 'generated': False}], [{'x': 100, 'y': 795, 'generated': True}, {'x': 100, 'y': 795, 'generated': False}, {'x': 373, 'y': 795, 'generated': False}, {'x': 558, 'y': 795, 'generated': True}, {'x': 612, 'y': 795, 'generated': False}, {'x': 948, 'y': 795, 'generated': True}, {'x': 970, 'y': 795, 'generated': False}, {'x': 1210, 'y': 795, 'generated': True}, {'x': 1496, 'y': 795, 'generated': True}], [{'x': 100, 'y': 995, 'generated': False}, {'x': 558, 'y': 995, 'generated': False}, {'x': 948, 'y': 995, 'generated': False}, {'x': 1210, 'y': 995, 'generated': False}, {'x': 1496, 'y': 995, 'generated': False}]]
    rooms = [[{'x': 100, 'y': 100, 'generated': True}, {'x': 413, 'y': 100, 'generated': True}, {'x': 650, 'y': 100, 'generated': True}, {'x': 1028, 'y': 100, 'generated': True}], [{'x': 100, 'y': 441, 'generated': True}, {'x': 100, 'y': 441, 'generated': False}, {'x': 413, 'y': 441, 'generated': False}, {'x': 441, 'y': 441, 'generated': True}, {'x': 650, 'y': 441, 'generated': False}, {'x': 905, 'y': 441, 'generated': True}, {'x': 1028, 'y': 441, 'generated': False}, {'x': 1152, 'y': 441, 'generated': True}], [{'x': 100, 'y': 724, 'generated': True}, {'x': 100, 'y': 724, 'generated': False}, {'x': 353, 'y': 724, 'generated': True}, {'x': 441, 'y': 724, 'generated': False}, {'x': 737, 'y': 724, 'generated': True}, {'x': 905, 'y': 724, 'generated': False}, {'x': 1013, 'y': 724, 'generated': True}, {'x': 1152, 'y': 724, 'generated': False}], [{'x': 100, 'y': 1088, 'generated': True}, {'x': 100, 'y': 1088, 'generated': False}, {'x': 353, 'y': 1088, 'generated': False}, {'x': 534, 'y': 1088, 'generated': True}, {'x': 737, 'y': 1088, 'generated': False}, {'x': 810, 'y': 1088, 'generated': True}, {'x': 1013, 'y': 1088, 'generated': False}, {'x': 1302, 'y': 1088, 'generated': True}], [{'x': 100, 'y': 1303, 'generated': True}, {'x': 100, 'y': 1303, 'generated': False}, {'x': 413, 'y': 1303, 'generated': True}, {'x': 534, 'y': 1303, 'generated': False}, {'x': 656, 'y': 1303, 'generated': True}, {'x': 810, 'y': 1303, 'generated': False}, {'x': 1302, 'y': 1303, 'generated': False}], [{'x': 100, 'y': 1503, 'generated': False}, {'x': 413, 'y': 1503, 'generated': False}, {'x': 656, 'y': 1503, 'generated': False}]]
    print(rooms)

    wall_width = CONFIG.getWALL_WIDTH()
    wall_width_half = wall_width/2

    # for idx,room in enumerate(rooms):
    #     for idx1,room1 in enumerate(room):
    #         room1["x"] = room1["x"] - (room1["x"] % 20)
    #         room1["y"] = room1["y"] - (room1["y"] % 20)

    for idx,room in enumerate(rooms):
        for idx1,room1 in enumerate(room):
            for idx2,room2 in enumerate(room):
                if idx1!=idx2 and room1["x"]==room2["x"] and room1["y"]==room2["y"]:
                    del room[idx2]
    

    joints = []
    for idx,y in enumerate(rooms):
        for x in y:
            joints.append({
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
    
    for idx,room in enumerate(joints):
        for idx1,room1 in enumerate(joints):
            # if idx!=idx1:
                if room["left"] > room1["left"] and room["top"]==room1["top"] and (room["corner"]["left"]==None or room["left"] > joints[room["corner"]["left"]]["left"]):
                    room["corner"]["left"]=idx1

                if room["left"] < room1["left"] and room["top"]==room1["top"] and (room["corner"]["right"]==None or room["left"] > joints[room["corner"]["right"]]["left"]):
                    room["corner"]["right"]=idx1

                if room["top"] > room1["top"] and room["left"]==room1["left"] and (room["corner"]["top"]==None or room["top"] > joints[room["corner"]["top"]]["top"]):
                    room["corner"]["top"]=idx1

                if room["top"] < room1["top"] and room["left"]==room1["left"] and (room["corner"]["bottom"]==None or room["top"] > joints[room["corner"]["bottom"]]["top"]):
                    room["corner"]["bottom"]=idx1


    def traverse(idx,move):
        if idx == None:
            return
        joints[idx]["outerwall"] = True
        current = joints[idx]
        corner = current["corner"]
        if move=="right":
            if corner["right"]!=None and joints[corner["right"]]["outerwall"] == False:
                # print("right")
                traverse(corner["right"],"right")
            elif corner["bottom"]!=None and joints[corner["bottom"]]["outerwall"] == False:
                # print("bottom")
                traverse(corner["bottom"],"bottom")
            elif corner["top"]!=None and joints[corner["top"]]["outerwall"] == False:
                # print("top")
                traverse(corner["top"],"top")
            elif corner["left"]!=None and joints[corner["left"]]["outerwall"] == False:
                # print("left")
                traverse(corner["left"],"left")

        if move=="bottom":
            if corner["bottom"]!=None and joints[corner["bottom"]]["outerwall"] == False:
                # print("bottom")
                traverse(corner["bottom"],"bottom")
            elif corner["right"]!=None and joints[corner["right"]]["outerwall"] == False:
                # print("right")
                traverse(corner["right"],"right")
            elif corner["top"]!=None and joints[corner["top"]]["outerwall"] == False:
                # print("top")
                traverse(corner["top"],"top")
            elif corner["left"]!=None and joints[corner["left"]]["outerwall"] == False:
                # print("left")
                traverse(corner["left"],"left")

        if move=="left":
            if corner["bottom"]!=None and joints[corner["bottom"]]["outerwall"] == False:
                # print("bottom")
                traverse(corner["bottom"],"bottom")
            elif corner["left"]!=None and joints[corner["left"]]["outerwall"] == False:
                # print("left")
                traverse(corner["left"],"left")
            elif corner["right"]!=None and joints[corner["right"]]["outerwall"] == False:
                # print("right")
                traverse(corner["right"],"right")
            elif corner["top"]!=None and joints[corner["top"]]["outerwall"] == False:
                # print("top")
                traverse(corner["top"],"top")

        if move=="top":
            if idx!=0:
                # print("top")
                traverse(corner["top"],"top")

    traverse(0,"right")

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

    for idx,x in enumerate(joints):
        # print(x)
        if x["corner"]["right"]:
            wallsobj.append(Wall(
                fromPosition=Position(int(x["left"]+wall_width_half),int(x["top"]-wall_width_half)),
                toPosition=Position(int(joints[x["corner"]["right"]]["left"]-wall_width_half),int(joints[x["corner"]["right"]]["top"]+wall_width_half)),
                isHorizontal=True,
                isOuterWall=x["targetIsOuterwall"]["right"] and x["outerwall"] and (not x["targetIsOuterwall"]["top"] or not x["targetIsOuterwall"]["bottom"]),
                doors=[],
                windows=[]
            ))
            
        if x["corner"]["bottom"]:
            wallsobj.append(Wall(
                fromPosition=Position(int(x["left"]+wall_width_half),int(x["top"]-wall_width_half)),
                toPosition=Position(int(joints[x["corner"]["bottom"]]["left"]-wall_width_half),int(joints[x["corner"]["bottom"]]["top"]+wall_width_half)),
                isHorizontal=False,
                isOuterWall=x["targetIsOuterwall"]["bottom"] and x["outerwall"] and (not x["targetIsOuterwall"]["right"] or not x["targetIsOuterwall"]["left"]),
                doors=[],
                windows=[]
            ))
    


    outerwalls = []
    innerwalls = []
    for idx,wall in enumerate(wallsobj):
        if wall.isOuterWall:
            outerwalls.append({"idx":idx,"wall":wall})
        else:
            innerwalls.append({"idx":idx,"wall":wall})

    # outer walls doors
    for _ in range(10):
        idx = random.randrange(0,len(outerwalls))
        o:Wall = wallsobj[outerwalls[idx]["idx"]]

        doorWidth = int(random.randrange(80,120))

        checkVertical = not o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            toPosition = fromPosition + doorWidth
            hinge = fromPosition if random.random() > 0.5 else toPosition
            intersecting = checkIntersecting(o.doors,fromPosition,toPosition) or \
                            checkIntersecting(o.windows,fromPosition,toPosition)

            if not intersecting:
                o.doors.append(Door(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    hinge = hinge,
                    openLeft = random.random() > 0.5,
                    style = "default"
                ))

    # outer walls windows
    for _ in range(10):
        idx = random.randrange(0,len(outerwalls))
        o:Wall = wallsobj[outerwalls[idx]["idx"]]

        doorWidth = int(random.randrange(80,120))

        checkVertical = not o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.y-o.fromPosition.y > doorWidth*2
        checkHorizontal = o.isHorizontal and len(o.doors)==0 and len(o.windows)==0 and o.toPosition.x-o.fromPosition.x > doorWidth*2

        if checkVertical:
            fromPosition = random.randrange(10,o.toPosition.y-o.fromPosition.y - 20 - doorWidth)

        if checkHorizontal:
            fromPosition = random.randrange(10,o.toPosition.x-o.fromPosition.x - 20 - doorWidth)

        if checkVertical or checkHorizontal:
            toPosition = fromPosition + doorWidth
            intersecting = checkIntersecting(o.doors,fromPosition,toPosition) or \
                            checkIntersecting(o.windows,fromPosition,toPosition)

            if not intersecting:
                o.windows.append(Window(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    style = "default"
                ))

    # inner walls
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
            intersecting = checkIntersecting(o.doors,fromPosition,toPosition) or \
                            checkIntersecting(o.windows,fromPosition,toPosition)

            if not intersecting:
                o.doors.append(Door(
                    fromPosition = fromPosition,
                    toPosition = toPosition,
                    hinge = hinge,
                    openLeft = random.random() > 0.5,
                    style = "default"
                ))


    response.walls = wallsobj

    return wallsobj,joints
