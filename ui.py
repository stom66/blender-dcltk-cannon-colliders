import bpy

from . _main import EXPORT_OT_CannonColliders_Export


#  ██████╗ █████╗ ███╗   ██╗███╗   ██╗ ██████╗ ███╗   ██╗     ██████╗ ██████╗ ██╗     ██╗     ██╗██████╗ ███████╗██████╗ ███████╗
# ██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔═══██╗████╗  ██║    ██╔════╝██╔═══██╗██║     ██║     ██║██╔══██╗██╔════╝██╔══██╗██╔════╝
# ██║     ███████║██╔██╗ ██║██╔██╗ ██║██║   ██║██╔██╗ ██║    ██║     ██║   ██║██║     ██║     ██║██║  ██║█████╗  ██████╔╝███████╗
# ██║     ██╔══██║██║╚██╗██║██║╚██╗██║██║   ██║██║╚██╗██║    ██║     ██║   ██║██║     ██║     ██║██║  ██║██╔══╝  ██╔══██╗╚════██║
# ╚██████╗██║  ██║██║ ╚████║██║ ╚████║╚██████╔╝██║ ╚████║    ╚██████╗╚██████╔╝███████╗███████╗██║██████╔╝███████╗██║  ██║███████║
#  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝
#

# UI button to refresh collection dropdown
class SCENE_OT_CannonColliders_UI_RefreshCollections(bpy.types.Operator):
	bl_idname  = "cc.btn_refresh_collections"
	bl_label   = "Refresh Collections"
	bl_options = {'REGISTER'}

	def execute(self, context):
		# Trigger the update_collection_items method
		context.scene.ss_settings.refresh_collections(context)
		return {'FINISHED'}
		
	
# Main panel
class VIEW3D_PT_CannonColliders_UI_Main(bpy.types.Panel):
	bl_label       = 'Cannon Colliders: Export'
	bl_category    = 'DCL Toolkit'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_options     = { 'DEFAULT_CLOSED' }

	def draw(self, context):
		layout = self.layout

		# Collection dropdown
		row = layout.row()
		row.label(text="Export collection")
		col = row.column(align=True)
		col.prop(context.scene.cc_settings, "export_collection", text="")

		col = row.column(align=True)
		col.operator("cc.btn_refresh_collections", text="", icon='FILE_REFRESH')

		# Output path
		row = layout.row()
		row.label(text="Output path:")
		row.prop(context.scene.cc_settings, "output_file", text="")

		# Minify JSON
		row = layout.row()
		col = row.column(align=False)
		col.label(text="JSON: minify output")
		col = row.column(align=True)
		col.prop(context.scene.cc_settings, "minify_json", text="")

		# Minify Data (round)
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Round data")
		col = row.column(align=True)
		col.prop(context.scene.cc_settings, "round_data_length", text="")
		
		col = row.column(align=True)
		col.prop(context.scene.cc_settings, "round_data", text="")

		# Btn: Export
		row = layout.row()
		row.operator(EXPORT_OT_CannonColliders_Export.bl_idname, text="Export", icon="FILE_VOLUME")
