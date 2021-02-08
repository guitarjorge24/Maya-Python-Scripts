from maya import cmds


class GearGenerator(object):  # Inherit from object since Maya uses Python 2.7. This is not necessary in Python 3
	"""
	This class has 2 methods: generate_gear (to create gear meshes) and change_teeth (to edit them).
	To use these functions you must first create an instance of the class such as:
		import a2_gear_mesh_generator as gmg
		gear1 = gmg.GearGenerator()
		gear1.generate_gear(8, 0.05)  # resembles a wheel
		gear1.change_teeth(5, 0.2)    # resembles a bolt
		gear1.change_teeth(10, 0.3)   # resembles a gear
		gear1.change_teeth(30, 1.2)   # resembles a CPu heatsink or fan
	"""
	def __init__(self):
		self.transform = None
		self.extrude = None
		self.poly_pipe_constructor = None
		print("New GearGenerator instance has been created. You can now call generate_gear() on this instance.")

	def generate_gear(self, teeth=10, length=0.3):
		"""
		Generates a gear mesh
		Args:
			teeth: How many teeth the gear will have
			length: How long each teeth will be
		"""
		subdivisions_axis = teeth * 2

		# Assigns pPipe to transform and polyPipe input node to poly_pipe_constructor
		self.transform, self.poly_pipe_constructor = cmds.polyPipe(subdivisionsAxis=subdivisions_axis)

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
			cmds.select("%s.f[%s]" % (self.transform, face), add=True)

		# extrudes the selected faces and returns the polyExtrudeFace node that is fed into the pPipeShape node
		self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
		print("extrude: " + str(self.extrude))
		# Lists the attributes of the extrude node.
		# The attribute that contains the faces which were extruded is the inputComponents attribute
		print("listAttr: " + str(cmds.listAttr(self.extrude)))
		print("getAttr of extrude.inputComponents: " + str(cmds.getAttr(self.extrude + ".inputComponents")))

	def change_teeth(self, teeth=10, length=0.3):
		"""
		Allows you to change the number of teeth and length of an existing gear mesh
		Args:
			teeth: How many teeth the gear will have
			length: How long each teeth will be
		"""
		subdivisions_axis = teeth * 2
		cmds.polyPipe(self.poly_pipe_constructor, edit=True, subdivisionsAxis=subdivisions_axis)
		side_faces = range(subdivisions_axis * 2, subdivisions_axis * 3, 2)
		face_names = []

		for face in side_faces:
			face_name = "f[%s]" % face
			face_names.append(face_name)

		print("face_names: " + str(face_names))
		# setAttr has different parameters depending on the type of data we're trying to set https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/CommandsPython/setAttr.html
		# In this case we want to set a list of face components on the extrude node's inputComponents attribute
		# The asterisk unpacks the list and passes the elements as individual arguments
		cmds.setAttr("%s.inputComponents" % self.extrude, len(face_names), *face_names, type="componentList")
		cmds.polyExtrudeFacet(self.extrude, edit=True, localTranslateZ=length)
