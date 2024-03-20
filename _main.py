import bpy
from math import degrees, radians, pi
from mathutils 	import Vector, Matrix, Euler

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

		# Create a list of all rigidbody data
		rb_errors = 0
		rb_objects = []
		for obj in col.all_objects:
			if obj.type == 'MESH' and obj.rigid_body is not None:

				# Check it's using one of the supported rb shapes
				rb_shape = obj.rigid_body.collision_shape
				if rb_shape == 'BOX' or rb_shape == 'SPHERE' or rb_shape == 'MESH':
					
					# Get the properties and append them to the list
					object_data = GetObjectRBProperties(obj)

					if object_data:
						rb_objects.append(object_data)
					else:
						# there was a problem with getting the data, probably an ngon
						rb_errors += 1
						pass

		# Check we got some RB's to export, otherwise show an error
		if len(rb_objects) > 0:
			# Export the data
			file = bpy.path.ensure_ext(GetExportPath(), ".json")
			ExportDataToJSON(rb_objects, file, cc_settings.minify_json)

			# Show success nmessage in the status bar
			message = str(len(rb_objects)) + ' Rigidbody colliders exported'

			# If any RBs were skipped because of ngons then let the user know
			if rb_errors > 0:
				message += ' - ' + str(rb_errors) + (' rigidbodies' if rb_errors > 1 else ' rigidbody') + ' skipped: ngons not supported'


			self.report({'INFO'}, message)
			return {'FINISHED'}
		else:
			# Show a warning to the user
			message = 'No Rigidbodies were found - nothing to do'

			if rb_errors > 0:
				message = str(rb_errors) + (' rigidbodies' if rb_errors > 1 else ' rigidbody') + ' skipped: ngons not supported'

			self.report({'INFO'}, message)
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
		obj_data["dimensions"] = [obj.dimensions.x, obj.dimensions.y, obj.dimensions.z]

		# Start rotation conversion. This is the tricky part. Pretty sure I've lost some brain cells to this.

		# Current matrix
		m_world   = obj.matrix_world

		# Offset matrix
		rot_tgt   = Euler((pi/2, 0, 0))
		m_rot_tgt = rot_tgt.to_matrix().to_4x4()

		# Flip matrix
		flip_matrix = Matrix.Scale(2, 4, (0, 0, 1))

		# Final matrix
		m_rot_new = (m_rot_tgt @ m_world) @ flip_matrix
		rot_new   = m_rot_new.to_euler()
	
		pos_new   = m_rot_new.translation

		# update new rot with above matrix
		obj_data["position"] = [pos_new.x,
								-pos_new.y,
								pos_new.z]

		obj_data["rotation"] = [-rot_new.x, 
								-rot_new.y, 
								rot_new.z]

		obj_data["rotation_order"] = obj.rotation_euler.order

		pass


	# Handle SPHERE colliders
	if rb.collision_shape == "SPHERE":
		obj_data["radius"] = max(obj.dimensions) / 2
		pass


	# Handle MESH colliders
	if rb.collision_shape == "MESH": 
		obj_data["vertices"] = []
		obj_data["indices"]  = []

		# Get the actual mesh data, set some debug counters
		mesh         = obj.data
		vertex_count = 0
		face_count   = 0

		# First, build a list of the vertex positions. Be sure to swizzle YZ to convert to Y+ up
		for vertex in mesh.vertices:
			vertex_count += 1
			# Get vert positions, taking into account the rotation and scale, but ignoring the location.
			# Maybe instead we ONLY account for scale?
			vert_pos = (obj.matrix_local @ vertex.co) - obj.location

			# Add the coords to the vertices array
			obj_data["vertices"].extend([vert_pos.x, vert_pos.z, vert_pos.y])

		pass

		# Now add tri face indicies - note reversed winding order
		for face in mesh.polygons:
			face_count +=1
			
			# Check if the face is a tri
			if len(face.vertices) == 3:
				obj_data["indices"].extend([face.vertices[0], face.vertices[2], face.vertices[1]])

			# Check for quads
			elif len(face.vertices) == 4:
				obj_data["indices"].extend([face.vertices[0], face.vertices[2], face.vertices[1]])
				obj_data["indices"].extend([face.vertices[0], face.vertices[3], face.vertices[2]])

			# Abort if ngon
			elif len(face.vertices) > 4:
				# If we have ngons, then break out and return false. 
				return False

	
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



def convert_rotation(rotation, rotation_order):
	# Convert Euler angles to radians
	#rotation = [radians(angle) for angle in rotation]
	
	# Convert rotation order
	if rotation_order == 'XYZ':
		# Convert from Blender's XYZ to THREE.js's XYZ
		rotation_order = 'ZYX'
	elif rotation_order == 'XZY':
		# Convert from Blender's XZY to THREE.js's ZYX
		rotation_order = 'ZXY'
	elif rotation_order == 'YXZ':
		# Convert from Blender's YXZ to THREE.js's ZYX
		rotation_order = 'ZXY'
	
	# Create a Quaternion from Euler angles
	quaternion = Euler(rotation, rotation_order).to_quaternion()
	
	# Convert Quaternion to Euler angles in THREE.js's rotation order
	return quaternion.to_euler('ZYX')