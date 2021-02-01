from maya import cmds

cube = cmds.polyCube()
cubeShape = cube[0]

circle = cmds.circle()
circleShape = circle[0]
print(cube, circle)

print type(circle)
print type(circle[0])

cmds.parent(cubeShape, circleShape)

# cmds.setAttr("pCube1.tx", lock = True)
cmds.setAttr(cubeShape + ".translate", lock=True)
print(type(None))
myList = ["jorge", 98, True]
# print("Output: " + myList[0] + myList[1] + myList[2])
# print("Output: " + str(32))
print type(myList)
myList.append("one more string")
print "appended list:", myList

applicantDictionary = {"Name": "Jorge Luque", "Position": "Unreal TD", "Phone": 3018217292}
print applicantDictionary
print applicantDictionary["Name"]

help(tuple)
dir(tuple())
