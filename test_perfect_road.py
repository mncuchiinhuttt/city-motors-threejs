import bpy
import bmesh
import math
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

# --- 1. CLEAN SOLID MATERIALS (60-30-10 PALETTE) ---
def create_mat(name, color, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

mat_asphalt   = create_mat("MAT_Asphalt",   (0.18, 0.19, 0.22, 1.0), roughness=0.8)
mat_curb      = create_mat("MAT_Curb",      (0.85, 0.86, 0.88, 1.0), roughness=0.6)
mat_stripe    = create_mat("MAT_Stripe",    (0.98, 0.68, 0.05, 1.0), roughness=0.4)
mat_guardrail = create_mat("MAT_Guardrail", (0.98, 0.35, 0.05, 1.0), roughness=0.3, metallic=0.5) # Solid Orange!
mat_post      = create_mat("MAT_Post",      (0.45, 0.47, 0.50, 1.0), roughness=0.3, metallic=0.8)

mat_valley    = create_mat("MAT_Valley",    (0.38, 0.50, 0.30, 1.0), roughness=0.9)
mat_cliff     = create_mat("MAT_Cliff",     (0.50, 0.48, 0.44, 1.0), roughness=0.9)
mat_snow      = create_mat("MAT_Snow",      (0.96, 0.97, 0.99, 1.0), roughness=0.4)
mat_trunk     = create_mat("MAT_Trunk",     (0.30, 0.20, 0.14, 1.0), roughness=0.85)
mat_pine      = create_mat("MAT_Pine",      (0.12, 0.35, 0.18, 1.0), roughness=0.85)

mat_car_body  = create_mat("MAT_CarBody",  (0.98, 0.35, 0.04, 1.0), roughness=0.2, metallic=0.5) # Hero Orange!
mat_car_glass = create_mat("MAT_CarGlass", (0.08, 0.12, 0.16, 1.0), roughness=0.1, metallic=0.9)
mat_wheel     = create_mat("MAT_Wheel",    (0.06, 0.06, 0.07, 1.0), roughness=0.8)
mat_rim       = create_mat("MAT_Rim",      (0.82, 0.84, 0.86, 1.0), roughness=0.25, metallic=0.85)
mat_headlight = create_mat("MAT_Headlight",(1.0, 1.0, 0.95, 1.0), roughness=0.1)
mat_taillight = create_mat("MAT_Taillight",(1.0, 0.05, 0.05, 1.0), roughness=0.1)

# --- 2. AUTHENTIC TOUGE S-CURVE SPLINE (SLOPING MOUNTAIN PASS) ---
ctrl_pts = [
    Vector(( -6.0, -22.0, 0.3)),  # Valley straight
    Vector((  8.0, -22.0, 0.6)),  # Turn into mountain pass
    Vector(( 22.0, -16.0, 1.5)),  # Climb curve 1
    Vector(( 26.0,  -7.0, 2.5)),  # Switchback right
    Vector(( 18.0,   2.0, 3.4)),  # S-turn curve cutting inward
    Vector(( 24.0,  12.0, 4.4)),  # S-turn curve climbing to mountain ridge
    Vector(( 26.0,  20.0, 5.2)),  # Panoramic Summit Overlook!
    Vector(( 16.0,  26.0, 4.4)),  # Hairpin switchback turn
    Vector((  4.0,  26.0, 3.4)),  # Descent curve
    Vector(( -8.0,  22.0, 2.4)),  # Winding descent
    Vector((-18.0,  14.0, 1.5)),  # Lower mountain ridge
    Vector((-24.0,   4.0, 0.8)),  # Valley curve
    Vector((-24.0,  -8.0, 0.4)),  # Southbound valley road
    Vector((-16.0, -18.0, 0.3)),  # Return straight
    Vector(( -6.0, -22.0, 0.3))   # Seamless closed loop
]

def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t
    return 0.5 * (
        (2 * p1) +
        (-p0 + p2) * t +
        (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
        (-p0 + 3 * p1 - 3 * p2 + p3) * t3
    )

num_samples = 160
spline_samples = []
n = len(ctrl_pts) - 1
for i in range(n):
    p0 = ctrl_pts[(i - 1) % n]
    p1 = ctrl_pts[i % n]
    p2 = ctrl_pts[(i + 1) % n]
    p3 = ctrl_pts[(i + 2) % n]
    sub = int(num_samples / n)
    for s in range(sub):
        t = s / float(sub)
        spline_samples.append(catmull_rom(p0, p1, p2, p3, t))

num_pts = len(spline_samples)

# --- 3. SHARED-VERTEX FLAWLESS ROAD MESH ---
bm_road = bmesh.new()
bm_guard = bmesh.new()
bm_stripes = bmesh.new()
bm_posts = bmesh.new()

up = Vector((0, 0, 1))

ring_cl = []
ring_al = []
ring_ar = []
ring_cr = []
ring_gb = []
ring_gt = []

tangents = []
rights = []

for i in range(num_pts):
    curr = spline_samples[i]
    next_pt = spline_samples[(i + 1) % num_pts]
    tan = (next_pt - curr).normalized()
    right = tan.cross(up).normalized()

    tangents.append(tan)
    rights.append(right)

    # Cross section: width 6.4m asphalt + 0.35m curbs
    p_cl = curr - right * 3.55 + Vector((0, 0, 0.10))
    p_al = curr - right * 3.20 + Vector((0, 0, 0.02))
    p_ar = curr + right * 3.20 + Vector((0, 0, 0.02))
    p_cr = curr + right * 3.55 + Vector((0, 0, 0.10))

    ring_cl.append(bm_road.verts.new(p_cl))
    ring_al.append(bm_road.verts.new(p_al))
    ring_ar.append(bm_road.verts.new(p_ar))
    ring_cr.append(bm_road.verts.new(p_cr))

    p_gb = p_cr + right * 0.12 + Vector((0, 0, 0.38))
    p_gt = p_cr + right * 0.12 + Vector((0, 0, 0.70))
    ring_gb.append(bm_guard.verts.new(p_gb))
    ring_gt.append(bm_guard.verts.new(p_gt))

for i in range(num_pts):
    next_i = (i + 1) % num_pts
    bm_road.faces.new((ring_al[i], ring_ar[i], ring_ar[next_i], ring_al[next_i]))
    bm_road.faces.new((ring_cl[i], ring_al[i], ring_al[next_i], ring_cl[next_i]))
    bm_road.faces.new((ring_ar[i], ring_cr[i], ring_cr[next_i], ring_ar[next_i]))
    bm_guard.faces.new((ring_gb[i], ring_gt[i], ring_gt[next_i], ring_gb[next_i]))

    if (i % 3) == 0:
        c = spline_samples[i]
        c_next = spline_samples[next_i]
        r = rights[i]
        p1 = c - r * 0.14 + Vector((0, 0, 0.04))
        p2 = c + r * 0.14 + Vector((0, 0, 0.04))
        p3 = c_next + r * 0.14 + Vector((0, 0, 0.04))
        p4 = c_next - r * 0.14 + Vector((0, 0, 0.04))
        bm_stripes.faces.new((
            bm_stripes.verts.new(p1), bm_stripes.verts.new(p2),
            bm_stripes.verts.new(p3), bm_stripes.verts.new(p4)
        ))

    if (i % 4) == 0:
        p_base = ring_cr[i].co + rights[i] * 0.12
        p_top = p_base + Vector((0, 0, 0.70))
        r_p = rights[i] * 0.08
        v1 = bm_posts.verts.new(p_base - r_p)
        v2 = bm_posts.verts.new(p_base + r_p)
        v3 = bm_posts.verts.new(p_top + r_p)
        v4 = bm_posts.verts.new(p_top - r_p)
        bm_posts.faces.new((v1, v2, v3, v4))

bmesh.ops.recalc_face_normals(bm_road, faces=bm_road.faces)
bmesh.ops.recalc_face_normals(bm_guard, faces=bm_guard.faces)

def finalize_mesh(name, bm, mat):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    m.polygons.foreach_set("use_smooth", [True] * len(m.polygons))
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)
    return o

finalize_mesh("SM_FlawlessRoad", bm_road, mat_asphalt)
finalize_mesh("SM_Stripes", bm_stripes, mat_stripe)
finalize_mesh("SM_GuardrailBeam", bm_guard, mat_guardrail)
finalize_mesh("SM_GuardrailPosts", bm_posts, mat_post)

# --- 4. SCENIC MOUNTAIN TERRAIN ---
print("Building Mountain Terrain Grid...")
bm_terr = bmesh.new()
grid_res = 38
grid_size = 94.0
step = grid_size / (grid_res - 1)

grid_v = []
for iy in range(grid_res):
    row = []
    y = -grid_size / 2.0 + iy * step
    for ix in range(grid_res):
        x = -grid_size / 2.0 + ix * step

        min_d = 999.0
        closest_z = 0.0
        for pt in spline_samples[::2]:
            d = math.hypot(x - pt.x, y - pt.y)
            if d < min_d:
                min_d = d
                closest_z = pt.z

        if min_d < 4.6:
            z = closest_z - 0.30
        else:
            blend = min(1.0, (min_d - 4.6) / 8.0)
            inner_d = math.hypot(x - 2.0, y - 4.0)
            inner_h = max(0.0, 7.5 - inner_d * 0.35)
            border_d = max(0.0, max(abs(x), abs(y)) - 28.0)
            outer_h = border_d * 0.55
            z = (closest_z - 0.30) * (1.0 - blend) + (inner_h + outer_h) * blend

        row.append(bm_terr.verts.new(Vector((x, y, max(0.0, z)))))
    grid_v.append(row)

for iy in range(grid_res - 1):
    for ix in range(grid_res - 1):
        bm_terr.faces.new((
            grid_v[iy][ix], grid_v[iy][ix + 1],
            grid_v[iy + 1][ix + 1], grid_v[iy + 1][ix]
        ))

m_terr = bpy.data.meshes.new("Mesh_Terrain")
bm_terr.to_mesh(m_terr)
bm_terr.free()
m_terr.polygons.foreach_set("use_smooth", [False] * len(m_terr.polygons))
obj_terr = bpy.data.objects.new("SM_Terrain", m_terr)
obj_terr.data.materials.append(mat_valley)
bpy.context.scene.collection.objects.link(obj_terr)

# Background Mountain Summits
distant_peaks = [
    ("Summit_East",  18.0, 24.0, ( 48.0,  12.0, 0.0)),
    ("Summit_North", 16.0, 22.0, (  4.0,  46.0, 0.0)),
    ("Summit_West",  16.0, 20.0, (-44.0,  10.0, 0.0)),
    ("Summit_South", 14.0, 18.0, ( 25.0, -45.0, 0.0))
]
for name, rad, h, loc in distant_peaks:
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=rad, radius2=0.0, depth=h, location=(loc[0], loc[1], h/2))
    p_body = bpy.context.active_object
    p_body.name = f"{name}_Rock"
    p_body.data.materials.append(mat_cliff)
    snow_h = h * 0.32
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=rad * 0.35, radius2=0.0, depth=snow_h, location=(loc[0], loc[1], h - snow_h/2))
    p_snow = bpy.context.active_object
    p_snow.name = f"{name}_Snow"
    p_snow.data.materials.append(mat_snow)

# Pine Trees safely on slopes (> 7.5m from road)
pine_coords = [
    (18.0, -28.0, 0.4), (32.0, -14.0, 1.4), (34.0, 4.0, 2.8), (30.0, 16.0, 3.4),
    (14.0,  30.0, 2.5), (-2.0,  30.0, 1.8), (-16.0, 26.0, 1.0), (-30.0, 14.0, 0.4),
    (-30.0, -4.0, 0.2), (-20.0, -22.0, 0.2), (2.0, -2.0, 4.8), (6.0, 8.0, 5.2)
]
for idx, (px, py, pz) in enumerate(pine_coords):
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.2, depth=1.5, location=(px, py, pz + 0.75))
    t = bpy.context.active_object
    t.data.materials.append(mat_trunk)
    for tier in range(3):
        r_tier = 1.3 - tier * 0.32
        h_tier = 1.6 - tier * 0.15
        z_tier = pz + 1.6 + tier * 0.9
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=r_tier, radius2=0.0, depth=h_tier, location=(px, py, z_tier))
        f = bpy.context.active_object
        f.data.materials.append(mat_pine)

# --- 5. HERO ORANGE SPORTS COUPE ---
print("Building Hero Sports Car...")
car_root = bpy.data.objects.new("Car_BlueCoupe", None) # Matches Three.js ID!
start_pt = spline_samples[0]
start_next = spline_samples[1]
start_tan = (start_next - start_pt).normalized()

car_root.location = start_pt + Vector((0, 0, 0.03))
bpy.context.scene.collection.objects.link(car_root)

# Chassis
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.52))
chassis = bpy.context.active_object
chassis.name = "Car_Chassis"
chassis.scale = (1.9, 4.2, 0.65)
bpy.ops.object.transform_apply(scale=True)
chassis.data.materials.append(mat_car_body)
chassis.parent = car_root

# Cabin
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.25, 1.08))
cabin = bpy.context.active_object
cabin.name = "Car_Cabin"
cabin.scale = (1.52, 2.2, 0.58)
bpy.ops.object.transform_apply(scale=True)
cabin.data.materials.append(mat_car_glass)
cabin.parent = car_root

# Roof Cap
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.25, 1.40))
roof = bpy.context.active_object
roof.name = "Car_Roof"
roof.scale = (1.46, 1.9, 0.08)
bpy.ops.object.transform_apply(scale=True)
roof.data.materials.append(mat_car_body)
roof.parent = car_root

# Rear Sport Spoiler
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.0, 1.05))
spoiler = bpy.context.active_object
spoiler.scale = (1.8, 0.35, 0.08)
bpy.ops.object.transform_apply(scale=True)
spoiler.data.materials.append(mat_car_body)
spoiler.parent = car_root

# 4 Wheels
for w_idx, (wx, wy, wz) in enumerate([(-1.0, 1.2, 0.36), (1.0, 1.2, 0.36), (-1.0, -1.2, 0.36), (1.0, -1.2, 0.36)]):
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.36, depth=0.26, location=(wx, wy, wz), rotation=(0, math.pi/2, 0))
    tire = bpy.context.active_object
    tire.data.materials.append(mat_wheel)
    tire.parent = car_root
    rx = wx + (0.02 if wx > 0 else -0.02)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22, depth=0.28, location=(rx, wy, wz), rotation=(0, math.pi/2, 0))
    rim = bpy.context.active_object
    rim.data.materials.append(mat_rim)
    rim.parent = car_root

# Headlights & Taillights
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.7, 2.11, 0.58))
hl_l = bpy.context.active_object
hl_l.scale = (0.38, 0.1, 0.18)
bpy.ops.object.transform_apply(scale=True)
hl_l.data.materials.append(mat_headlight)
hl_l.parent = car_root

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.7, 2.11, 0.58))
hl_r = bpy.context.active_object
hl_r.scale = (0.38, 0.1, 0.18)
bpy.ops.object.transform_apply(scale=True)
hl_r.data.materials.append(mat_headlight)
hl_r.parent = car_root

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.11, 0.58))
tl = bpy.context.active_object
tl.scale = (1.65, 0.1, 0.18)
bpy.ops.object.transform_apply(scale=True)
tl.data.materials.append(mat_taillight)
tl.parent = car_root

# Rotate car along road direction
yaw = math.atan2(start_tan.y, start_tan.x) - math.pi / 2
car_root.rotation_mode = "XYZ"
car_root.rotation_euler = (0, 0, yaw)

# --- 6. EXPORT FLAWLESS MOUNTAIN.GLB ---
mtn_out = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(filepath=mtn_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Flawless Mountain to {mtn_out}")

# --- 7. RENDER PREVIEW IMAGES FOR USER INSPECTION ---
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

# Camera 1: GÓC GẦN
cam_close_data = bpy.data.cameras.new("Cam_Close")
cam_close_data.lens = 38
cam_close_obj = bpy.data.objects.new("Cam_Close", cam_close_data)
cam_close_pos = start_pt - start_tan * 7.0 + Vector((0, 0, 2.6))
cam_close_obj.location = cam_close_pos
look_target = start_pt + start_tan * 6.0 + Vector((0, 0, 0.8))
dir_vec = (look_target - cam_close_pos).normalized()
cam_close_obj.rotation_euler = dir_vec.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_close_obj)

# Camera 2: GÓC RỘNG
cam_wide_data = bpy.data.cameras.new("Cam_Wide")
cam_wide_data.lens = 22
cam_wide_obj = bpy.data.objects.new("Cam_Wide", cam_wide_data)
cam_wide_pos = Vector((18.0, -38.0, 28.0))
cam_wide_obj.location = cam_wide_pos
dir_wide = (Vector((8.0, 0.0, 2.0)) - cam_wide_pos).normalized()
cam_wide_obj.rotation_euler = dir_wide.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_wide_obj)

bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.image_settings.file_format = "PNG"

bpy.context.scene.camera = cam_close_obj
bpy.context.scene.render.filepath = "/tmp/preview_mountain_close.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_mountain_close.png")

bpy.context.scene.camera = cam_wide_obj
bpy.context.scene.render.filepath = "/tmp/preview_mountain_wide.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_mountain_wide.png")
