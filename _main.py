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
		result = Main()

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


def Main():
	# Ensure nothing is selected
	bpy.ops.object.select_all(action='DESELECT')
	
	# Get collider exporter settings
	cc_settings = bpy.context.scene.cc_settings

	# Get the chosen collection in the panel
	col = bpy.data.collections.get(cc_settings.export_collection)

	# Create a list of all objects with rigibodies

	# Blank dict for storing RB objects and their properties
	rb_objects = []

	# Loop through all collection objects, and gt the RB properties
	for obj in col.all_objects:
		if obj.type == 'MESH' and obj.rigid_body is not None:
			object_data = GetObjectRBProperties(obj)
			rb_objects.append(object_data)

	# Export the data
	file = bpy.path.ensure_ext(GetExportPath(), ".json")
	
	ExportDataToJSON(rb_objects, file, cc_settings.minify_json)

	return True

			
def GetObjectRBProperties(obj: bpy.types.Object):

	# Blank dict to store the results in
	obj_data = {
		"obj_name"   : obj.name,						# Object name
		"position"   : [],					# Object position
		"vertices"   : [], 								# Contains vert positions (not in tuples)
		"indices"    : [], 								# Contains mesh indices
		"type"       : obj.rigid_body.type, 			# RB type: ACTIVE or PASSIVE
		"shape"      : obj.rigid_body.collision_shape, 	# Shape: Box, Sphere, Capsule, Cylinder, Cone, Convex Hull or Mesh, 
		"friction"   : obj.rigid_body.friction,  		# Friction value of physics material
		"restitution": obj.rigid_body.restitution,  	# Bounciness value of physics material
		"mass"       : obj.rigid_body.mass,  			# Mass of object
	}
	# Set the position, flipping Y and Z
	obj_data["position"] = [obj.location.x, obj.location.z, obj.location.y]

	# Get the actual mesh data
	mesh = obj.data
	for vertex in mesh.vertices:
		x, y, z = vertex.co[:]
		obj_data["vertices"].extend([x, z, y])

	for face in mesh.polygons:
		obj_data["indices"].extend(face.vertices)

	return obj_data