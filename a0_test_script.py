from maya import cmds

# create a cube
cube = cmds.polyCube()
cubeShape = cube[0]

# create a nurbs circle
circle = cmds.circle()
circleShape = circle[0]

print(cube, circle)
print(type(circle))
print(type(circle[0]))
print(type(None))

# parent the cube to the circle
cmds.parent(cubeShape, circleShape)

# lock the cube's translation so it can only be moved by moving the parent
cmds.setAttr(cubeShape + ".translate", lock=True)
# cmds.setAttr("pCube1.tx", lock = True)

# list test
myList = ["jorge", 98, True]
# print("Output: " + myList[0] + myList[1] + myList[2] + str(32))
print(type(myList))
myList.append("one more string")
print("appended list: " + str(myList))

# dictionary test
applicantDictionary = {"Name": "Jorge Luque", "Position": "Unreal TD", "Phone": 3018217292}
print(applicantDictionary)
print(applicantDictionary["Name"])

# tuple
dir(tuple())
help(tuple)

