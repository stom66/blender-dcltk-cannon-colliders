import 	bpy
import 	os
import 	json
from 	collections 			import defaultdict
from 	xml.etree.ElementTree 	import tostring



# ██████╗  █████╗ ████████╗██╗  ██╗
# ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║
# ██████╔╝███████║   ██║   ███████║
# ██╔═══╝ ██╔══██║   ██║   ██╔══██║
# ██║     ██║  ██║   ██║   ██║  ██║
# ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
#                                  


def GetExportPath() -> str:
	"""
	Get the export path for the collection.

	Returns:
	- str: The export path.
	"""
	# Get cannon collider settings
	cc_settings = bpy.context.scene.cc_settings

	# Get the export path based on the current settings value
	path = bpy.path.abspath(cc_settings.output_file)

	# Ensure the output folder exists
	try:
		# Ensure filepath exists, create it if it doesn't
		os.makedirs(os.path.dirname(path))
	except FileExistsError:
		pass  # The directory already exists, no need to create

	# Normalise the output path, ensuring correct os.sep is used
	path = os.path.normpath(path)

	return path



# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗         ██╗███████╗ ██████╗ ███╗   ██╗
# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝         ██║██╔════╝██╔═══██╗████╗  ██║
# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║            ██║███████╗██║   ██║██╔██╗ ██║
# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║       ██   ██║╚════██║██║   ██║██║╚██╗██║
# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║       ╚█████╔╝███████║╚██████╔╝██║ ╚████║
# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
#

def ExportDataToJSON(
	data,
	file,
	minify
):
	"""
	Export the supplied tileset_data to a file at the given output_path
	"""

	if minify:
		json_string = json.dumps(data)
	else:
		json_string = json.dumps(data, indent="\t")

	# Write the data object to an output JSON file
	with open(file, "w") as json_file:
		json_file.write(json_string)
