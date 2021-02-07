from maya import cmds

def generate_gear(teeth=10, length=0.3):
	subdivisions_axis = teeth * 2

	# Assigns pPipe to transform and polyPipe input node to poly_pipe_constructor
	transform, poly_pipe_constructor = cmds.polyPipe(subdivisionsAxis = subdivisions_axis)

	# in a default 20-subdivision pipe, the numbering of the faces is as follows:
	# inner faces: 0-19,  top: 20-39, outer: 40-59, and bottom: 60-79
	# Thus, the outer faces always start counting at NumberOfSubdivisions * 2 and end at NumberOfSubdivisions * 3 -1
	# since the upper limit of range() is exclusive, we don't have to do the "-1"
	outer_side_faces = range(subdivisions_axis*2, subdivisions_axis*3, 2)
	print("outer_side_faces: " + str(outer_side_faces))

	cmds.select(clear=True)

	# select all the faces to extrude
	for face in outer_side_faces:
		# transform_name.f allows you to access a list containing all the faces of the mesh
		# "add' means the next face we select is added to the selection w/o deselecting previously selected faces
		cmds.select("%s.f[%s]" % (transform, face), add=True)

	extrude = cmds.polyExtrudeFacet(localTranslateZ=length)
	print("extrude: " + extrude)
