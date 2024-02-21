#    <Scene Slicer - Blender addon for exporting a scene in a confiruable grid of 3d tiles>
#
#    Copyright (C) <2024> <Tom Steventon>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
	"name"       : "DCL Toolkit: Cannon Colliders",
	"description": "Exporter tool for generating Cannon-compatible colliders from Rigidbodies",
	"author"     : "Tom Steventon - stom66",
	"version"    : (1, 0, 0),
	"blender"    : (3, 6, 0),
	"location"   : "3D Viewport -> Sidebar -> DCL Toolkit",
	"description": "DCL Toolkit: Cannon Colliders",
	"category"   : "Import-Export",
	"doc_url"    : "https://github.com/stom66/blender-dcltk-cannon-colliders"
}

from . _main 		import *
from . _settings 	import *
from . ui 			import *



# ██████╗ ███████╗ ██████╗ ██╗███████╗████████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
# ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
# ██████╔╝█████╗  ██║  ███╗██║███████╗   ██║   ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
# ██╔══██╗██╔══╝  ██║   ██║██║╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
# ██║  ██║███████╗╚██████╔╝██║███████║   ██║   ██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
#
		
def register():
	# Register settings class
	bpy.utils.register_class(CannonColliderSettings)

	bpy.utils.register_class(EXPORT_OT_CannonColliders)
	bpy.utils.register_class(SCENE_OT_CannonColliders_RefreshCollections)
	bpy.utils.register_class(VIEW3D_PT_CannonColliders_Export)
	bpy.utils.register_class(VIEW3D_PT_CannonColliders_Main)

	bpy.types.Scene.cc_settings = bpy.props.PointerProperty(type=CannonColliderSettings)
	

def unregister():
	# Unregister various UI component classes
	bpy.utils.unregister_class(VIEW3D_PT_CannonColliders_Main)
	bpy.utils.unregister_class(VIEW3D_PT_CannonColliders_Export)
	bpy.utils.unregister_class(SCENE_OT_CannonColliders_RefreshCollections)
	bpy.utils.unregister_class(EXPORT_OT_CannonColliders)

	# Unregister settings class
	bpy.utils.unregister_class(CannonColliderSettings)

	del bpy.types.Scene.cc_settings
