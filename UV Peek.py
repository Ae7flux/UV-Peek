
bl_info = {
	"name": "UV Peek",
	"version": (0, 1, 0),
	"blender": (2, 80, 0),
	"author": "Ae7flux",
	"location": "View2D",
	"description": "Show connected UVs",
	"category": "Utility",}

import bpy 
from bpy.types import WorkSpaceTool 
import os
import re
import sys
import time
import mathutils
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
import numpy as np
import bmesh



class UVP_OT_UV_Peek(Operator):
	bl_idname = "uvp.uv_peek"
	bl_label = " UV Peek"
	bl_description = "See UVs that share a vertex"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	event = None
	
	def execute(self, context):
		if bpy.context.tool_settings.uv_sticky_select_mode == 'DISABLED':
			bpy.context.preferences.addons['UV Peek'].preferences.uv_sel_mode = 0
		else: 
			if bpy.context.tool_settings.uv_sticky_select_mode =='SHARED_LOCATION':
				bpy.context.preferences.addons['UV Peek'].preferences.uv_sel_mode = 1
			else:				
				bpy.context.preferences.addons['UV Peek'].preferences.uv_sel_mode = 2
				
		bpy.context.tool_settings.uv_sticky_select_mode = 'SHARED_VERTEX'
		bpy.ops.uv.select(extend=False, deselect=False, toggle=False, deselect_all=False, select_passthrough=False, location=(self.texture_coordinates[0], self.texture_coordinates[1]))		
		return {'FINISHED'}		
	
	def modal(self, context, event):
		if event.type  in {'LEFTMOUSE','MIDDLEMOUSE','RIGHTMOUSE','BUTTON4MOUSE','BUTTON5MOUSE','BUTTON6MOUSE','BUTTON7MOUSE'}: 
			if bpy.context.preferences.addons['UV Peek'].preferences.uv_sel_mode == 0:
				bpy.context.tool_settings.uv_sticky_select_mode = 'DISABLED'
			else: 
				if bpy.context.preferences.addons['UV Peek'].preferences.uv_sel_mode == 1:
					bpy.context.tool_settings.uv_sticky_select_mode = 'SHARED_LOCATION'
				else: 
					bpy.context.tool_settings.uv_sticky_select_mode = 'SHARED_VERTEX'
			bpy.ops.uv.select(extend=False, deselect=False, toggle=False, deselect_all=False, select_passthrough=False, location=(self.texture_coordinates[0], self.texture_coordinates[1]))#reselect the vertex to make the effect od the mode change visible
			return {'FINISHED'}				
		else:
			return {'RUNNING_MODAL'}		
		
	def invoke(self, context, event):
		self.event = event
		self.texture_coordinates = context.region.view2d.region_to_view(self.event.mouse_region_x, self.event.mouse_region_y)		
		self.execute(context)
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}
			
class UVP_Preferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	

	uv_sel_mode: IntProperty(
        name="UV select mode",
        default=0,	
		)	

	
			
classes = (				
			UVP_OT_UV_Peek,
			UVP_Preferences
			)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
		




	
def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	



if __name__ == "__main__":
	register()


