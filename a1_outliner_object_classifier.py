# You can call the rename_object in this script to automatically add a suffix to all objects in the outliner that represents their type.
# You set the rename_only_selected option to True to rename only currently selected objects.
from maya import cmds

# region GLOBAL VARIABLES
# Assigns a suffix to each object type
suffixes_dict = {
	"ambientLight": "LGT",  # light
	"mesh": "GEO",  # geometry
	"nurbsCurve": "NC",  # nurbsCurve
	"joint": "JNT",  # joint
	"camera": None,
}
default_suffix = "GRP"  # group
# endregion


def rename_objects(rename_only_selected=False):
	"""
	This function adds a suffix to objects in the Outliner that represent the object't type

	Args:
		rename_only_selected: False by default. Set to true to rename only the currently selected objects.

	Returns: A list of all the objects that were renamed.
	"""
	# "long" returns the full path so we get the object's parents which allows us to sort
	selected_objects = cmds.ls(selection=rename_only_selected, dag=True, long=True)

	# if user wants to rename only selected but they didn't select any objects
	if rename_only_selected and not selected_objects:
		raise RuntimeError(
			"You have chosen to rename only selected objects but have not selected any. "
			"Please select at least 1 object.")

	# Sorting with key=len sorts from shortest to longest. We reverse the sorting to sort from longest to shortest
	# since children have longer names than their parents and we want to get the children.
	selected_objects.sort(key=len, reverse=True)

	print("________________________")
	for obj in selected_objects:
		print("")

		# the parents of the object are added in front and separated by a "|" so we split the string
		# by "|" and get the last element, which is the current object's name without its parents/full path
		short_name = obj.split("|")[-1]
		print("shortName: " + short_name)
		print("obj (full name): " + obj)

		# returns the type such as mesh, transform, nurbsCurve, camera, etc
		# However, when you select a pCube mesh in the outliner, you are actually selecting it's transform node
		# so if we want to return the object type as "mesh" and not "transform", we have to get the child of
		# the transform which is the "pCubeShape" which has a type of "mesh"
		print("Outliner objType: " + cmds.objectType(obj))

		# if there are no children, assign an empty list to "children" instead of assigning "None" so the statement
		# below "len(children)" is always valid
		children = cmds.listRelatives(obj, children=True, fullPath=True) or []
		print("Children: " + str(children))

		# joints don't have any children by default, unlike meshes which have shape nodes as children by default
		if len(children) == 0 or cmds.objectType(obj) == "joint":
			obj_type = cmds.objectType(obj)
		else:
			obj_type = cmds.objectType(children[0])

		print("Actual objType: " + obj_type)

		# if dict doesn't contain key, then it returns default_suffix
		suffix = suffixes_dict.get(obj_type, default_suffix)

		if not suffix:  # true when type is camera
			print("skipping camera\n" + "________________________")
			continue

		# if the suffix has already been added to the object, don't add it again
		if obj.endswith("_" + suffix):
			print("skipped " + short_name + " because it already has a suffix\n" + "________________________")
			continue

		new_name = "%s_%s" % (short_name, suffix)  # string substitution is a little more efficient than string concatenation of 3 strings in Python
		print("new name: " + new_name)
		print("________________________")
		cmds.rename(obj, new_name)

		# return condensed  list of objects that got renamed and their new names
		index = selected_objects.index(obj)
		selected_objects[index] = obj.replace(short_name, new_name)

	print selected_objects
	return selected_objects

