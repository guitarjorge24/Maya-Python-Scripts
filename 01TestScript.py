from maya import cmds

cube = cmds.polyCube()
cubeShape = cube[0]

circle = cmds.circle()
circleShape = circle[0]
print(cube, circle)

type(circle)
type(circle[0])
print(type(word))

cmds.parent(cubeShape, circleShape)

#cmds.setAttr("pCube1.tx", lock = True)
cmds.setAttr(cubeShape + ".translate", lock = True)
print(type(None))
myList = ["jorge", 98, True]
#print("Output: " + myList[0] + myList[1] + myList[2])
#print("Output: " + str(32))
print type(myList)
myList.append("one more string")
print "appended list:", myList

applicantDictionary = {"Name":"Jorge Luque", "Position":"Unreal TD", "Phone" : 3018217292}
print applicantDictionary
print applicantDictionary["Name"]

help(tuple)
dir(tuple())

# returns a list of the currently selected objects
selection = cmds.ls(selection=True)
if len(selection) == 0:
    # "long" returns the full path so we get the object's parents which allows us to sort
    selection = cmds.ls(dag=True, long=True)

# Sorting with key=len sorts from shortest to longest. We reverse the sorting to sort from longest to shortest
# since children have longer names than their parents and we want to get the children.
selection.sort(key=len, reverse=True)

print "________________________"
for obj in selection:
    print ""
    # the parents of the obejct are added in front and separated by a "|" so we split the string 
    # by "|" and get the last element, which is the current object's name without its parents/full path
    shortName = obj.split("|")[-1]
    print "name:", shortName
    
    # returns the type such as mesh, transform, nurbsCurve, camera, etc
    # However, when you select a pCube mesh in the outliner, you are actually selecting it's transform node
    # so if we want to return the object type as "mesh" and not "transform", we have to get the child of
    # the transform which is the "pCubeShape" which has a type of "mesh"
    print("Outliner objType: " + cmds.objectType(obj))
    
    # if there are no children, assign an empty list to "children" instead of assigning "None"
    children = cmds.listRelatives(obj, children=True, fullPath=True) or []
    print "Children:", children
    print "________________________"
    if(len(children) == 1):
        child = children[0]
        objType = cmds.objectType(child)
    else:
        objType = cmds.objectType(obj)
    print("Actual objType: " + objType)
    #print("actual objType: {}".format(objType))