import bpy

from . export import ExportDataToJSON, GetExportPath

class EXPORT_OT_CannonColliders(bpy.types.Operator):
	bl_idname  = "cc.export"
	bl_label   = "Export Cannon Colliders"
	bl_options = {'REGISTER', 'UNDO'}

	filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # type: ignore

	def execute(self, context):
		# Your export logic goes here
		# Use self.filepath to get the export path

		# Call the Main function
		result = CC_Main()

		# Report the result
		if result:
			self.report({'INFO'}, 'Cannon colliders exported successfully')
			return {'FINISHED'}
		else:
			self.report({'ERROR'}, 'Failed to export cannon colliders')
			return {'CANCELLED'}

	#def invoke(self, context, event):
	#	# Open the file dialog
	#	context.window_manager.fileselect_add(self)
	#	return {'RUNNING_MODAL'}


def CC_Main():
	# Ensure nothing is selected
	bpy.ops.object.select_all(action='DESELECT')
	
	# Get collider exporter settings
	cc_settings = bpy.context.scene.cc_settings

	# Get the chosen collection in the panel
	col = bpy.data.collections.get(cc_settings.export_collection)

	# Blank dict for storing RB objects and their properties
	rb_objects = {}

	# Loop through all collection objects, and gt the RB properties
	for obj in col.all_objects:
		if obj.type == 'MESH' and obj.rigid_body is not None:
			rb_objects[obj.name] = GetObjectRBProperties(obj)

	# Export the data
	file = GetExportPath(cc_settings.output_file)
	ExportDataToJSON(rb_objects, file, cc_settings.minify_json)

	return True

			
def GetObjectRBProperties(obj: bpy.types.Object):

	obj_data = {
		"vertices"   : [], # Contains tuples of vert positions
		"indices"    : [], # Contains mesh indices
		"type"       : "", # RB type: ACTIVE or PASSIVE
		"shape"      : "", # Shape: Box, Sphere, Capsule, Cylinder, Cone, Convex Hull or Mesh, 
		"friction"   : 0,  # Friction value of physics material
		"restitution": 0,  # Bounciness value of physics material
		"mass"       : 0,  # Mass of object
	}

	mesh = obj.data
	for vertex in mesh.vertices:
		obj_data["vertices"].append(tuple(vertex.co))

	for face in mesh.polygons:
		obj_data["indices"].extend(face.vertices)

	# Physics properties
	obj_data["shape"]       = obj.rigid_body.collision_shape
	obj_data["friction"]    = obj.rigid_body.friction
	obj_data["restitution"] = obj.rigid_body.restitution
	obj_data["mass"]        = obj.rigid_body.mass
	obj_data["type"]        = obj.rigid_body.type

	return obj_data