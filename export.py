import 	bpy
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

def GetExportPath(path: str) -> str:
	"""
	Get the export path for the collection.

	Args:
	- output_path (str): The output path for the collection.

	Returns:
	- str: The export path.
	"""
	# Set the export file name to match the collection name (minus the MATCH_STRING)
	path = bpy.path.abspath(path)
	
	# Ensure filepath doesn't have a trailing slash, as this causes a permission error
	if path.endswith("/") or path.endswith("\\"):
		path = path[:-1]

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
