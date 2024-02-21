import bpy


# ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
# ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
# ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
# ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
# ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
# ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
#
                                 
class CannonColliderSettings(bpy.types.PropertyGroup):
	
	def refresh_collections(self, context):
		items = [(col.name, col.name, col.name) for col in bpy.context.scene.collection.children if col.name != "Cutters"]
		return items

	# Collection to export dropdown
	export_collection: bpy.props.EnumProperty(
		name        = "Export Collection",
		description = "Choose a collection to convert and export",
		items       = refresh_collections,
		default 	= None,
		#update      = refresh_collections,
		attr        = "export_collection"
	)  # type: ignore

	# Output path
	output_file: bpy.props.StringProperty(
		name        = "Output path",
		description = "Choose a folder to export to",
		default     = "//colliders.json",
		subtype     = 'FILE_PATH'
	) # type: ignore

	# JSON minify
	minify_json: bpy.props.BoolProperty(
		name        = "Minify JSON",
		description = "Minify the exported JSON to reduce filesize",
		default     = True,
	) # type: ignore
	