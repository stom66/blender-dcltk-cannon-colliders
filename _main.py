import bpy
from math import degrees
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

		# Create a list of all objects with valid rigibodies
		rb_objects = []
		for obj in col.all_objects:
			if obj.type == 'MESH' and obj.rigid_body is not None:

				# Check it's using one of the supported rb shapes
				rb_shape = obj.rigid_body.collision_shape
				if rb_shape == 'BOX' or rb_shape == 'SPHERE' or rb_shape == 'MESH':
					
					# Get the properties and append them to the list
					object_data = GetObjectRBProperties(obj)
					rb_objects.append(object_data)

		# Check we got some RB's to export, otherwise show an error
		if len(rb_objects) > 0:
			# Export the data
			file = bpy.path.ensure_ext(GetExportPath(), ".json")
			ExportDataToJSON(rb_objects, file, cc_settings.minify_json)

			# Show success nmessage in the status bar
			self.report({'INFO'}, str(len(rb_objects)) + ' Rigidbody colliders exported')
			return {'FINISHED'}
		else:
			# Show a warning to the user
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
		"type"       : rb.type, 			# RB type: ACTIVE or PASSIVE
		"shape"      : rb.collision_shape, 	# Shape: Box, Sphere, Capsule, Cylinder, Cone, Convex Hull or Mesh, 
		"friction"   : rb.friction,  		# Friction value of physics material
		"restitution": rb.restitution,  	# Bounciness value of physics material
		"mass"       : rb.mass,  			# Mass of object
	}
	
	# Set the position, flipping Y and Z
	obj_data["position"] = [obj.location.x, obj.location.z, obj.location.y]

	# Handle BOX colliders
	if rb.collision_shape == "BOX":
		obj_data["dimensions"] = [obj.dimensions.x, obj.dimensions.z, obj.dimensions.y]
		obj_data["rotation"]   = [
			-obj.rotation_euler.x,
			obj.rotation_euler.z,
			obj.rotation_euler.y
		]
		pass

	# Handle SPHERE colliders
	if rb.collision_shape == "SPHERE":
		obj_data["radius"] = max(obj.dimensions) / 2
		pass

	# Handle MESH colliders
	if rb.collision_shape == "MESH": 
		obj_data["vertices"] = []
		obj_data["indices"]  = []

		# Get the actual mesh data
		mesh = obj.data
		for vertex in mesh.vertices:

			# Get verts, adjusted for transform
			vert_pos = (obj.matrix_local @ vertex.co) - obj.location

			# Add the coords to the vertices array
			obj_data["vertices"].extend([vert_pos.x, vert_pos.z, vert_pos.y])

		# Add face indices
		for face in mesh.polygons:
			obj_data["indices"].extend(face.vertices)

	
	# Round values, if enabled
	if cc_settings.round_data: 
		obj_data["position"]    = [round(axis, cc_settings.round_data_length) for axis in obj_data["position"]]
		obj_data["friction"]    = round(obj_data["friction"], cc_settings.round_data_length)
		obj_data["mass"]        = round(obj_data["mass"], cc_settings.round_data_length)
		obj_data["restitution"] = round(obj_data["restitution"], cc_settings.round_data_length)
		
		if "radius" in obj_data: 
			obj_data["radius"]     = round(obj_data["radius"], cc_settings.round_data_length)
		
		if "dimensions" in obj_data: 
			obj_data["dimensions"] = [round(axis, cc_settings.round_data_length) for axis in obj_data["dimensions"]]
		
		if "rotation" in obj_data: 
			obj_data["rotation"] = [round(axis, cc_settings.round_data_length) for axis in obj_data["rotation"]]
		
		if "vertices" in obj_data: 
			obj_data["vertices"]   = [round(vert, cc_settings.round_data_length) for vert in obj_data["vertices"]]

	# Done
	return obj_data