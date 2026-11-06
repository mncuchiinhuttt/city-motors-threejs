import bpy
import bmesh
import math
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

def create_mat(name, color, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

# --- Enhanced 60/30/10 Natural Color Palette ---
# 60% Dominant: Warm Alpine Stone & Mountain Slopes
mat_ground_grass = create_mat("MAT_GroundGrass", (0.32, 0.46, 0.28, 1.0), roughness=0.85)
mat_rock_cliff   = create_mat("MAT_RockCliff",   (0.48, 0.46, 0.42, 1.0), roughness=0.9)
mat_dark_rock    = create_mat("MAT_DarkRock",    (0.36, 0.34, 0.32, 1.0), roughness=0.9)
mat_snow_summit  = create_mat("MAT_SnowSummit",  (0.96, 0.97, 0.98, 1.0), roughness=0.5)

# 30% Secondary: Dark Asphalt Road & Alpine Pine
mat_asphalt      = create_mat("MAT_Asphalt",      (0.14, 0.15, 0.18, 1.0), roughness=0.75)
mat_curb_stone   = create_mat("MAT_CurbStone",   (0.78, 0.80, 0.82, 1.0), roughness=0.7)
mat_pine_needles = create_mat("MAT_PineNeedles", (0.12, 0.32, 0.18, 1.0), roughness=0.85)
mat_pine_trunk   = create_mat("MAT_PineTrunk",   (0.30, 0.20, 0.14, 1.0), roughness=0.85)

# 10% Accent: Solid Sunset Orange
mat_guardrail    = create_mat("MAT_Guardrail",    (0.98, 0.35, 0.05, 1.0), roughness=0.4, metallic=0.4)
mat_stripe_yellow= create_mat("MAT_StripeYellow", (0.98, 0.65, 0.05, 1.0), roughness=0.4)
mat_car_orange   = create_mat("MAT_CarOrange",   (0.98, 0.35, 0.04, 1.0), roughness=0.2, metallic=0.5)
mat_car_glass    = create_mat("MAT_CarGlass",    (0.08, 0.12, 0.16, 1.0), roughness=0.1, metallic=0.9)
mat_wheel        = create_mat("MAT_Wheel",       (0.06, 0.06, 0.07, 1.0), roughness=0.8)
mat_rim          = create_mat("MAT_Rim",         (0.82, 0.84, 0.86, 1.0), roughness=0.25, metallic=0.85)
mat_taillight    = create_mat("MAT_Taillight",   (1.0, 0.05, 0.05, 1.0), roughness=0.1)
mat_headlight    = create_mat("MAT_Headlight",   (1.0, 1.0, 0.95, 1.0), roughness=0.1)

# --- 1. CONTINUOUS MOUNTAIN PASS SPLINE ---
ctrl_pts = [
    Vector((  0.0, -24.0, 0.3)),
    Vector(( 14.0, -22.0, 0.9)),
    Vector(( 22.0, -16.0, 1.9)),
    Vector(( 28.0,  -7.0, 3.1)),
    Vector(( 29.0,   3.0, 4.2)),
    Vector(( 25.0,  14.0, 5.4)), # Summit Ridge Overlook!
    Vector(( 15.0,  22.0, 4.4)), # Hairpin curve
    Vector((  4.0,  24.0, 3.2)),
    Vector(( -6.0,  22.0, 2.2)),
    Vector((-16.0,  15.0, 1.4)),
    Vector((-22.0,   5.0, 0.7)),
    Vector((-22.0,  -8.0, 0.3)),
    Vector((-14.0, -19.0, 0.3)),
    Vector((  0.0, -24.0, 0.3))
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

num_samples = 150
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
        pt = catmull_rom(p0, p1, p2, p3, t)
        spline_samples.append(pt)

num_pts = len(spline_samples)

# --- 2. MULTI-LAYER ROAD: FOUNDATION BED + ASPHALT + CURBS + GUARDRAIL ---
bm_bed = bmesh.new()
bm_asphalt = bmesh.new()
bm_stripes = bmesh.new()
bm_guard = bmesh.new()

road_w = 6.2
half_w = road_w / 2.0
bed_w = road_w + 1.6 # Extra width for clean road shoulder
half_bed = bed_w / 2.0

for i in range(num_pts):
    curr = spline_samples[i]
    next_pt = spline_samples[(i + 1) % num_pts]
    tangent = (next_pt - curr).normalized()
    up = Vector((0, 0, 1))
    right = tangent.cross(up).normalized()

    # 1. Road bed foundation (raised 0.15m to cleanly clear terrain!)
    b_l1 = curr - right * half_bed - Vector((0, 0, 0.25))
    b_r1 = curr + right * half_bed - Vector((0, 0, 0.25))
    b_l2 = next_pt - right * half_bed - Vector((0, 0, 0.25))
    b_r2 = next_pt + right * half_bed - Vector((0, 0, 0.25))
    bm_bed.faces.new((
        bm_bed.verts.new(b_l1), bm_bed.verts.new(b_r1),
        bm_bed.verts.new(b_r2), bm_bed.verts.new(b_l2)
    ))

    # 2. Asphalt ribbon (on top of bed)
    r_l1 = curr - right * half_w + Vector((0, 0, 0.05))
    r_r1 = curr + right * half_w + Vector((0, 0, 0.05))
    r_l2 = next_pt - right * half_w + Vector((0, 0, 0.05))
    r_r2 = next_pt + right * half_w + Vector((0, 0, 0.05))
    bm_asphalt.faces.new((
        bm_asphalt.verts.new(r_l1), bm_asphalt.verts.new(r_r1),
        bm_asphalt.verts.new(r_r2), bm_asphalt.verts.new(r_l2)
    ))

    # 3. Outer Guardrail barrier along cliff edge
    g_base1 = r_r1 + right * 0.2 + Vector((0, 0, 0.05))
    g_top1  = g_base1 + Vector((0, 0, 0.70))
    g_base2 = r_r2 + right * 0.2 + Vector((0, 0, 0.05))
    g_top2  = g_base2 + Vector((0, 0, 0.70))
    bm_guard.faces.new((
        bm_guard.verts.new(g_base1), bm_guard.verts.new(g_top1),
        bm_guard.verts.new(g_top2), bm_guard.verts.new(g_base2)
    ))

    # 4. Yellow dashed line
    if (i % 3) == 0:
        c1 = curr - right * 0.15 + Vector((0, 0, 0.07))
        c2 = curr + right * 0.15 + Vector((0, 0, 0.07))
        c3 = next_pt + right * 0.15 + Vector((0, 0, 0.07))
        c4 = next_pt - right * 0.15 + Vector((0, 0, 0.07))
        bm_stripes.faces.new((
            bm_stripes.verts.new(c1), bm_stripes.verts.new(c2),
            bm_stripes.verts.new(c3), bm_stripes.verts.new(c4)
        ))

# Create Road Objects
def create_mesh_obj(name, bm, mat):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)
    return o

create_mesh_obj("SM_RoadBed", bm_bed, mat_curb_stone)
create_mesh_obj("SM_Asphalt", bm_asphalt, mat_asphalt)
create_mesh_obj("SM_Guardrail", bm_guard, mat_guardrail)
create_mesh_obj("SM_Stripes", bm_stripes, mat_stripe_yellow)

# --- 3. MOUNTAIN TERRAIN (TERRACED & FACETED TO REST CLEANLY BENEATH ROAD) ---
print("Building Mountain Pass Terrain...")
bm_terrain = bmesh.new()
grid_res = 40
grid_size = 96.0
step = grid_size / (grid_res - 1)

verts_grid = []
for iy in range(grid_res):
    row = []
    y = -grid_size / 2.0 + iy * step
    for ix in range(grid_res):
        x = -grid_size / 2.0 + ix * step

        # Distance to closest point on road spline
        min_d = 999.0
        closest_z = 0.0
        for pt in spline_samples[::2]:
            d = math.hypot(x - pt.x, y - pt.y)
            if d < min_d:
                min_d = d
                closest_z = pt.z

        # Road corridor shelf:
        if min_d < 4.8:
            z = closest_z - 0.28 # Cleanly below road bed!
        else:
            blend = min(1.0, (min_d - 4.8) / 9.0)
            # Center mountain mass inside the loop
            inner_peak_d = math.hypot(x - 5.0, y - 4.0)
            inner_h = max(0.0, 19.0 - inner_peak_d * 0.50)
            # Outer mountain range
            outer_peak_d = math.hypot(x - 38.0, y - 8.0)
            outer_h = max(0.0, 24.0 - outer_peak_d * 0.45)
            # Valley slope
            val_h = math.cos(x * 0.07) * 3.0 + math.sin(y * 0.07) * 2.5 + 1.5
            z = (closest_z - 0.28) * (1.0 - blend) + (max(inner_h, outer_h) + val_h) * blend

        row.append(bm_terrain.verts.new(Vector((x, y, max(0.0, z)))))
    verts_grid.append(row)

for iy in range(grid_res - 1):
    for ix in range(grid_res - 1):
        bm_terrain.faces.new((
            verts_grid[iy][ix], verts_grid[iy][ix + 1],
            verts_grid[iy + 1][ix + 1], verts_grid[iy + 1][ix]
        ))

mesh_terrain = bpy.data.meshes.new("Mesh_MountainTerrain")
bm_terrain.to_mesh(mesh_terrain)
bm_terrain.free()
mesh_terrain.polygons.foreach_set("use_smooth", [False] * len(mesh_terrain.polygons))
obj_terrain = bpy.data.objects.new("SM_MountainTerrain", mesh_terrain)
obj_terrain.data.materials.append(mat_ground_grass)
bpy.context.scene.collection.objects.link(obj_terrain)

# Grand Alpine Peaks in background with Snowcaps
peaks = [
    ("Peak_EastGiant",  18.0, 26.0, (40.0, 8.0, 0.0)),
    ("Peak_NorthGiant", 17.0, 22.0, (2.0, 42.0, 0.0)),
    ("Peak_WestRidge",  16.0, 20.0, (-38.0, 8.0, 0.0)),
]
for name, rad, h, loc in peaks:
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=rad, radius2=0.0, depth=h, location=(loc[0], loc[1], h/2))
    p_body = bpy.context.active_object
    p_body.name = f"{name}_Rock"
    p_body.data.materials.append(mat_rock_cliff)
    # Snowcap
    snow_h = h * 0.32
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=rad*0.35, radius2=0.0, depth=snow_h, location=(loc[0], loc[1], h - snow_h/2))
    p_snow = bpy.context.active_object
    p_snow.name = f"{name}_Snow"
    p_snow.data.materials.append(mat_snow_summit)

# Pine Trees (Placed at safe distances > 7.5m from road)
pine_locs = [
    (20.0, -32.0, 0.5), (34.0, -18.0, 1.8), (35.0, 0.0, 3.8), (34.0, 15.0, 4.8),
    (18.0,  32.0, 3.8), (-4.0, 34.0, 2.5), (-18.0, 28.0, 1.6), (-28.0, 16.0, 0.8),
    (-28.0, -6.0, 0.4), (-22.0, -22.0, 0.2), (6.0, -2.0, 5.0), (10.0, 10.0, 5.8)
]
for idx, (px, py, pz) in enumerate(pine_locs):
    # Trunk
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.22, depth=1.6, location=(px, py, pz + 0.8))
    t_obj = bpy.context.active_object
    t_obj.data.materials.append(mat_pine_trunk)
    # 3-tier cone foliage
    for tier in range(3):
        r_tier = 1.4 - tier * 0.35
        h_tier = 1.8 - tier * 0.2
        z_tier = pz + 1.8 + tier * 0.95
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=r_tier, radius2=0.0, depth=h_tier, location=(px, py, z_tier))
        fol_obj = bpy.context.active_object
        fol_obj.data.materials.append(mat_pine_needles)

# --- 4. HERO ORANGE SPORTS COUPE (PROPORTIONED, SLEEK, ON THE ROAD) ---
print("Building Hero Sports Car...")
car_root = bpy.data.objects.new("Car_HeroOrange", None)
start_pt = spline_samples[0]
start_next = spline_samples[1]
start_tan = (start_next - start_pt).normalized()

# Sit car tires directly on asphalt surface!
car_root.location = start_pt + Vector((0, 0, 0.06))
bpy.context.scene.collection.objects.link(car_root)

# Main Aerodynamic Body
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.52))
chassis = bpy.context.active_object
chassis.name = "Car_Chassis"
chassis.scale = (1.9, 4.2, 0.65)
bpy.ops.object.transform_apply(scale=True)
chassis.data.materials.append(mat_car_orange)
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
roof.data.materials.append(mat_car_orange)
roof.parent = car_root

# Rear Sport Spoiler
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.0, 1.05))
spoiler = bpy.context.active_object
spoiler.scale = (1.8, 0.35, 0.08)
bpy.ops.object.transform_apply(scale=True)
spoiler.data.materials.append(mat_car_orange)
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

# --- 5. RENDER SETUP: LIGHTING & 2 CAMERAS ---
# Sunlight
sun_data = bpy.data.lights.new(name="SunLight", type="SUN")
sun_data.energy = 3.6
sun_data.color = (1.0, 0.98, 0.94)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
sun_obj.location = (25, -25, 45)
sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(-35))
bpy.context.scene.collection.objects.link(sun_obj)

# Azure Sky
if not bpy.context.scene.world:
    bpy.context.scene.world = bpy.data.worlds.new("World")
bpy.context.scene.world.use_nodes = True
bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.65, 0.82, 0.96, 1.0)
    bg_node.inputs["Strength"].default_value = 1.05

# Camera 1: GÓC GẦN (Chase Cam - 7.5m behind, 2.7m above, looking directly forward over hood!)
cam_close_data = bpy.data.cameras.new("Cam_Close")
cam_close_data.lens = 38
cam_close_obj = bpy.data.objects.new("Cam_Close", cam_close_data)
cam_close_pos = start_pt - start_tan * 7.5 + Vector((0, 0, 2.7))
cam_close_obj.location = cam_close_pos

look_target = start_pt + start_tan * 5.0 + Vector((0, 0, 0.8))
dir_vec = (look_target - cam_close_pos).normalized()
cam_close_obj.rotation_euler = dir_vec.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_close_obj)

# Camera 2: GÓC RỘNG (Panoramic Wide Cam - High overlook overlooking mountain pass)
cam_wide_data = bpy.data.cameras.new("Cam_Wide")
cam_wide_data.lens = 22
cam_wide_obj = bpy.data.objects.new("Cam_Wide", cam_wide_data)
cam_wide_pos = Vector((22.0, -42.0, 32.0))
cam_wide_obj.location = cam_wide_pos
dir_wide = (Vector((10.0, 0.0, 3.0)) - cam_wide_pos).normalized()
cam_wide_obj.rotation_euler = dir_wide.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_wide_obj)

# Render settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.image_settings.file_format = "PNG"

# Render Camera 1
bpy.context.scene.camera = cam_close_obj
bpy.context.scene.render.filepath = "/tmp/preview_close.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_close.png")

# Render Camera 2
bpy.context.scene.camera = cam_wide_obj
bpy.context.scene.render.filepath = "/tmp/preview_wide.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_wide.png")

print("Mountain Pass Renders Complete!")
