import bpy
from mathutils 	import Vector

from . export import ExportDataToJSON, GetExportPath

class EXPORT_OT_CannonColliders_Export(bpy.types.Operator):
	bl_idname  = "cc.export"
	bl_label   = "Export Cannon Colliders"
	bl_options = {'REGISTER', 'UNDO'}

	filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # type: ignore

	def execute(self, context):

		# Check if we are not already in object mode
		if bpy.context.mode != 'OBJECT':
			# Switch to object mode
			bpy.ops.object.mode_set(mode='OBJECT')

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

		# Check we got some RB's to export, otherwiose show an error
		if len(rb_objects) > 0:
			ExportDataToJSON(rb_objects, file, cc_settings.minify_json)
			self.report({'INFO'}, str(len(rb_objects)) + ' Rigidbody colliders exported')
			return {'FINISHED'}
		else:
			# Add a warning to the user
			self.report({'INFO'}, 'No Rigidbodies were found - nothing to do')
			return {'CANCELLED'}
			

			
def GetObjectRBProperties(obj: bpy.types.Object):
	# Get collider exporter settings
	cc_settings = bpy.context.scene.cc_settings

	# Set short ref to rigidbody
	rb = obj.rigid_body

	# Blank dict to store the results in
	obj_data = {
		"obj_name"   : obj.name,			# Object name
		"position"   : [],					# Object position
		"vertices"   : [], 					# Contains vert positions (not in tuples)
		"indices"    : [], 					# Contains mesh indices
		"type"       : rb.type, 			# RB type: ACTIVE or PASSIVE
		"shape"      : rb.collision_shape, 	# Shape: Box, Sphere, Capsule, Cylinder, Cone, Convex Hull or Mesh, 
		"friction"   : rb.friction,  		# Friction value of physics material
		"restitution": rb.restitution,  	# Bounciness value of physics material
		"mass"       : rb.mass,  			# Mass of object
	}
	
	# Set the position, flipping Y and Z
	obj_data["position"] = [obj.location.x, obj.location.z, obj.location.y]
	
	# Round off position, if enabled
	if cc_settings.round_data:
		obj_data["position"] = [
			round(axis, cc_settings.round_data_length) for axis in [
				obj.location.x, obj.location.z, obj.location.y
			]]

	# Get the actual mesh data
	mesh = obj.data
	for vertex in mesh.vertices:

		# Get verts, adjusted for transform
		vert_pos = (obj.matrix_local @ vertex.co) - obj.location

		# Round off coords, if enabled
		if cc_settings.round_data: 
			vert_pos = Vector((round(value, cc_settings.round_data_length) for value in vert_pos))


		obj_data["vertices"].extend([vert_pos.x, vert_pos.z, vert_pos.y])

	# Add face indices
	for face in mesh.polygons:
		obj_data["indices"].extend(face.vertices)

	return obj_data