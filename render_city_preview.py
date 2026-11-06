import bpy
import math
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

# Load existing city.glb or render from Blender
bpy.ops.import_scene.gltf(filepath="/home/mncuchiinhuttt/city-threejs/public/assets/city.glb")

# Sunlight
sun_data = bpy.data.lights.new(name="SunLight", type="SUN")
sun_data.energy = 3.6
sun_data.color = (1.0, 0.98, 0.94)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
sun_obj.location = (25, -25, 45)
sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(-35))
bpy.context.scene.collection.objects.link(sun_obj)

if not bpy.context.scene.world:
    bpy.context.scene.world = bpy.data.worlds.new("World")
bpy.context.scene.world.use_nodes = True
bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.65, 0.82, 0.96, 1.0)
    bg_node.inputs["Strength"].default_value = 1.05

# Find hero car
hero = bpy.data.objects.get("Car_BlueCoupe")
hero_pos = hero.location if hero else Vector((0, -16.0, 0.05))

# Camera 1: City Close Chase Cam
cam_close_data = bpy.data.cameras.new("City_Cam_Close")
cam_close_data.lens = 38
cam_close_obj = bpy.data.objects.new("City_Cam_Close", cam_close_data)
cam_close_pos = hero_pos + Vector((0, -7.5, 2.6))
cam_close_obj.location = cam_close_pos
dir_close = (hero_pos + Vector((0, 6.0, 0.8)) - cam_close_pos).normalized()
cam_close_obj.rotation_euler = dir_close.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_close_obj)

# Camera 2: City Wide Cam
cam_wide_data = bpy.data.cameras.new("City_Cam_Wide")
cam_wide_data.lens = 22
cam_wide_obj = bpy.data.objects.new("City_Cam_Wide", cam_wide_data)
cam_wide_pos = Vector((0.0, -36.0, 26.0))
cam_wide_obj.location = cam_wide_pos
dir_wide = (Vector((0.0, 0.0, 2.0)) - cam_wide_pos).normalized()
cam_wide_obj.rotation_euler = dir_wide.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_wide_obj)

# Render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.image_settings.file_format = "PNG"

# Render Close
bpy.context.scene.camera = cam_close_obj
bpy.context.scene.render.filepath = "/tmp/preview_city_close.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_city_close.png")

# Render Wide
bpy.context.scene.camera = cam_wide_obj
bpy.context.scene.render.filepath = "/tmp/preview_city_wide.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_city_wide.png")
