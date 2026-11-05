import bpy
import sys
import math
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
input_stl, output_png = args[0], args[1]

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

bpy.ops.wm.stl_import(filepath=input_stl)
mesh_objects = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not mesh_objects:
    raise RuntimeError("No mesh found in STL")

bpy.context.view_layer.update()
mins = [min((o.matrix_world @ Vector(c))[i] for o in mesh_objects for c in o.bound_box) for i in range(3)]
maxs = [max((o.matrix_world @ Vector(c))[i] for o in mesh_objects for c in o.bound_box) for i in range(3)]
center = Vector(tuple((mins[i] + maxs[i]) / 2 for i in range(3)))
dims = Vector(tuple(maxs[i] - mins[i] for i in range(3)))
span = max(dims)
if span <= 0:
    raise RuntimeError("Invalid STL dimensions")

mat = bpy.data.materials.new("Skyline | graphite")
mat.diffuse_color = (0.72, 0.74, 0.78, 1)
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (0.58, 0.62, 0.68, 1)
bsdf.inputs["Metallic"].default_value = 0.32
bsdf.inputs["Roughness"].default_value = 0.3
for obj in mesh_objects:
    obj.data.materials.clear()
    obj.data.materials.append(mat)

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
shading = scene.display.shading
shading.light = "STUDIO"
shading.color_type = "MATERIAL"
shading.background_type = "WORLD"
shading.show_shadows = True
shading.show_cavity = True
shading.cavity_type = "BOTH"
scene.render.resolution_x = 1600
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = False
scene.world.color = (0.008, 0.008, 0.01)
scene.view_settings.view_transform = "AgX"

# Dark graphite studio background and soft neutral lighting.
world = bpy.data.worlds.new("Near black studio") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.008, 0.008, 0.01, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.35

def area_light(name, location, energy, size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    obj.location = Vector(location)
    obj.rotation_euler = (center - obj.location).to_track_quat("-Z", "Y").to_euler()

area_light("Key softbox", center + Vector((span*0.8, -span*1.0, span*1.35)), span*span*18, span*0.9)
area_light("Fill softbox", center + Vector((-span*1.0, -span*0.15, span*0.8)), span*span*9, span*0.8)
area_light("Rim softbox", center + Vector((span*0.25, span*1.0, span*1.1)), span*span*22, span*0.7)

cam_data = bpy.data.cameras.new("Skyline camera")
cam = bpy.data.objects.new("Skyline camera", cam_data)
scene.collection.objects.link(cam)
cam.location = center + Vector((span*1.65, -span*1.9, span*1.45))
cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
cam_data.type = "ORTHO"
cam_data.ortho_scale = span * 2.55
scene.camera = cam

# Keep the model centered with comfortable margins.
scene.render.filepath = output_png
scene.camera.data.lens = 50
bpy.ops.render.render(write_still=True)
