from maya import cmds


def rename_objects():
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
		print("")

		# the parents of the object are added in front and separated by a "|" so we split the string
		# by "|" and get the last element, which is the current object's name without its parents/full path
		short_name = obj.split("|")[-1]
		print "shortName:", short_name
		print("obj (full name): " + obj)

		# returns the type such as mesh, transform, nurbsCurve, camera, etc
		# However, when you select a pCube mesh in the outliner, you are actually selecting it's transform node
		# so if we want to return the object type as "mesh" and not "transform", we have to get the child of
		# the transform which is the "pCubeShape" which has a type of "mesh"
		print("Outliner objType: " + cmds.objectType(obj))

		# if there are no children, assign an empty list to "children" instead of assigning "None"
		children = cmds.listRelatives(obj, children=True, fullPath=True) or []
		print "Children:", children

		if len(children) == 1:
			child = children[0]
			obj_type = cmds.objectType(child)
		else:
			obj_type = cmds.objectType(obj)

		print("Actual objType: " + obj_type)

		# Set the suffix based on object type
		if obj_type == "mesh":
			suffix = "geo"  # geometry
		elif obj_type == "joint":
			suffix = "jnt"
		elif obj_type == "camera":
			print("skipping camera\n" + "________________________")
			continue
		else:
			suffix = "grp"

		# if the suffix has already been added to the object, don't add it again
		if obj.endswith(suffix):
			print ("skipped " + short_name + " because it already has a suffix\n" + "________________________")
			continue

		new_name = short_name + "_" + suffix
		print ("new name: " + new_name)
		print "________________________"
		cmds.rename(obj, new_name)
