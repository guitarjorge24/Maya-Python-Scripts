from maya import cmds


def generate_gear(teeth=10, length=0.3):
	"""
	Generates a gear mesh
	Args:
		teeth: How many teeth the gear will have
		length: How long each teeth will be

	Returns:
		A tuple containing the transform, constructor, and extrude node of the gear
	"""
	subdivisions_axis = teeth * 2

	# Assigns pPipe to transform and polyPipe input node to poly_pipe_constructor
	transform, poly_pipe_constructor = cmds.polyPipe(subdivisionsAxis=subdivisions_axis)

	# in a default 20-subdivision pipe, the numbering of the faces is as follows:
	# inner faces: 0-19,  top: 20-39, outer: 40-59, and bottom: 60-79
	# Thus, the outer faces always start counting at NumberOfSubdivisions * 2 and end at NumberOfSubdivisions * 3 -1
	# since the upper limit of range() is exclusive, we don't have to do the "-1"
	outer_side_faces = range(subdivisions_axis * 2, subdivisions_axis * 3, 2)
	print("outer_side_faces: " + str(outer_side_faces))

	cmds.select(clear=True)

	# select all the faces to extrude
	for face in outer_side_faces:
		# transform_name.f allows you to access a list containing all the faces of the mesh
		# "add' means the next face we select is added to the selection w/o deselecting previously selected faces
		cmds.select("%s.f[%s]" % (transform, face), add=True)

	# extrudes the selected faces and returns the polyExtrudeFace node that is fed into the pPipeShape node
	extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
	print("extrude: " + str(extrude))
	# Lists the attributes of the extrude node.
	# The attribute that contains the faces which were extruded is the inputComponents attribute
	print("listAttr: " + str(cmds.listAttr(extrude)))
	print("getAttr of extrude.inputComponents: " + str(cmds.getAttr(extrude + ".inputComponents")))
	return transform, poly_pipe_constructor, extrude


def change_teeth(constructor, extrude, teeth=10, length=0.3):
	print(constructor)
	print(extrude)
	subdivisions_axis = teeth * 2
	cmds.polyPipe(constructor, edit=True, subdivisionsAxis=subdivisions_axis)
	side_faces = range(subdivisions_axis * 2, subdivisions_axis * 3, 2)
	face_names = []

	for face in side_faces:
		face_name = "f[%s]" % face
		face_names.append(face_name)

	print("face_names: " + str(face_names))
	# setAttr has different parameters depending on the type of data we're trying to set https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/CommandsPython/setAttr.html
	# In this case we want to set a list of face components on the extrude node's inputComponents attribute
	# The asterisk unpacks the list and passes the elements as individual arguments
	cmds.setAttr("%s.inputComponents" % extrude, len(face_names), *face_names, type="componentList")
	cmds.polyExtrudeFacet(extrude, edit=True, localTranslateZ=length)
