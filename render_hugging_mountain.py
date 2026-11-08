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

mat_asphalt   = create_mat("MAT_Road", (0.18, 0.19, 0.22, 1.0), roughness=0.8)
mat_stripe    = create_mat("MAT_StripeYellow", (0.98, 0.68, 0.05, 1.0), roughness=0.4)
mat_guardrail = create_mat("MAT_Guardrail", (0.98, 0.35, 0.05, 1.0), roughness=0.3, metallic=0.5) # Solid Orange!
mat_post      = create_mat("MAT_Post", (0.45, 0.47, 0.50, 1.0), roughness=0.3, metallic=0.8)

mat_valley    = create_mat("MAT_Valley", (0.40, 0.52, 0.32, 1.0), roughness=0.9)
mat_cliff     = create_mat("MAT_Cliff",  (0.46, 0.44, 0.40, 1.0), roughness=0.88)
mat_dark_rock = create_mat("MAT_DarkRock",(0.36, 0.34, 0.32, 1.0), roughness=0.9)
mat_snow      = create_mat("MAT_Snow",   (0.96, 0.97, 0.99, 1.0), roughness=0.4)
mat_trunk     = create_mat("MAT_Trunk",  (0.30, 0.20, 0.14, 1.0), roughness=0.85)
mat_pine      = create_mat("MAT_Pine",   (0.12, 0.35, 0.18, 1.0), roughness=0.85)

mat_car_orange= create_mat("MAT_CarOrange", (0.98, 0.35, 0.04, 1.0), roughness=0.2, metallic=0.5) # Hero Orange!
mat_car_glass = create_mat("MAT_CarGlass", (0.08, 0.12, 0.16, 1.0), roughness=0.1, metallic=0.9)
mat_wheel     = create_mat("MAT_Wheel",    (0.06, 0.06, 0.07, 1.0), roughness=0.8)
mat_rim       = create_mat("MAT_Rim",      (0.82, 0.84, 0.86, 1.0), roughness=0.25, metallic=0.85)
mat_headlight = create_mat("MAT_Headlight",(1.0, 1.0, 0.95, 1.0), roughness=0.1)
mat_taillight = create_mat("MAT_Taillight",(1.0, 0.05, 0.05, 1.0), roughness=0.1)

mm = {
    "asphalt": mat_asphalt,
    "stripe": mat_stripe,
    "guardrail": mat_guardrail,
    "post": mat_post,
    "valley": mat_valley,
    "cliff": mat_cliff,
    "dark_rock": mat_dark_rock,
    "snow": mat_snow,
    "trunk": mat_trunk,
    "pine": mat_pine,
    "car_orange": mat_car_orange,
    "car_glass": mat_car_glass,
    "wheel": mat_wheel,
    "rim": mat_rim,
    "headlight": mat_headlight,
    "taillight": mat_taillight
}
def add_box(name, size, loc, mat, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    return obj

def add_cylinder(name, radius, depth, loc, mat, vertices=12, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj

def add_cone(name, radius, depth, loc, mat, vertices=7, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=0.0, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj

# Hero Car: Forward orientation (-Y front, +Y rear)
def build_car(name, body_mat, loc=(0,0,0)):
    root = bpy.data.objects.new(name, None)
    root.location = loc
    bpy.context.scene.collection.objects.link(root)

    lower = add_box(f"{name}_LowerBody", (1.9, 4.2, 0.65), (0, 0, 0.52), body_mat)
    lower.parent = root

    cabin = add_box(f"{name}_Cabin", (1.52, 2.2, 0.58), (0, 0.25, 1.08), mat_car_glass)
    cabin.parent = root

    roof = add_box(f"{name}_RoofCap", (1.46, 1.9, 0.08), (0, 0.25, 1.40), body_mat)
    roof.parent = root

    # Rear Sport Spoiler (At -Y!)
    spoiler = add_box(f"{name}_Spoiler", (1.8, 0.35, 0.08), (0, -2.0, 1.05), body_mat)
    spoiler.parent = root
    wheel_coords = [(-1.0, -1.2, 0.36), (1.0, -1.2, 0.36), (-1.0, 1.2, 0.36), (1.0, 1.2, 0.36)]
    for w_idx, (wx, wy, wz) in enumerate(wheel_coords):
        tire = add_cylinder(f"{name}_Wheel_{w_idx}", 0.36, 0.26, (wx, wy, wz), mat_wheel, vertices=12, rot=(0, math.pi/2, 0))
        tire.parent = root
        rx = wx + (0.02 if wx > 0 else -0.02)
        rim = add_cylinder(f"{name}_Rim_{w_idx}", 0.22, 0.28, (rx, wy, wz), mat_rim, vertices=8, rot=(0, math.pi/2, 0))
        rim.parent = root

    # FRONT HEADLIGHTS (At +Y!)
    hl_l = add_box(f"{name}_HL_L", (0.38, 0.1, 0.18), (-0.7, 2.11, 0.58), mat_headlight)
    hl_r = add_box(f"{name}_HL_R", (0.38, 0.1, 0.18), ( 0.7, 2.11, 0.58), mat_headlight)
    hl_l.parent = root
    hl_r.parent = root

    # REAR TAILLIGHT (At -Y!)
    tl = add_box(f"{name}_TL", (1.65, 0.1, 0.18), (0, -2.11, 0.58), mat_taillight)
    tl.parent = root
    return root
# Spline interpolation
def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t
    return 0.5 * (
        (2 * p1) +
        (-p0 + p2) * t +
        (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
        (-p0 + 3 * p1 - 3 * p2 + p3) * t3
    )

def sample_curve(ctrl_pts, num_samples):
    samples = []
    n = len(ctrl_pts) - 1
    for i in range(n):
        p0 = ctrl_pts[(i - 1) % n]
        p1 = ctrl_pts[i % n]
        p2 = ctrl_pts[(i + 1) % n]
        p3 = ctrl_pts[(i + 2) % n]
        sub = int(num_samples / n)
        for s in range(sub):
            t = s / float(sub)
            samples.append(catmull_rom(p0, p1, p2, p3, t))
    return samples

# =========================================================================
# MOUNTAIN TOUGE SPLINE & CLIFF WALL (HUGGING THE LEFT SIDE!)
# =========================================================================
print("Building Mountain Pass with Left-Side Cliff Wall...")

mtn_ctrl = [
    Vector(( -6.0, -22.0, 0.3)),
    Vector((  8.0, -22.0, 0.6)),
    Vector(( 20.0, -17.0, 1.4)),
    Vector(( 26.0,  -8.0, 2.2)),
    Vector(( 20.0,   2.0, 3.0)), # S-turn cutting inward
    Vector(( 24.0,  12.0, 3.8)),
    Vector(( 25.0,  20.0, 4.4)), # Summit Overlook
    Vector(( 16.0,  26.0, 3.8)), # Hairpin switchback
    Vector((  4.0,  26.0, 3.0)),
    Vector(( -8.0,  22.0, 2.2)),
    Vector((-18.0,  14.0, 1.4)),
    Vector((-24.0,   4.0, 0.8)),
    Vector((-24.0,  -8.0, 0.4)),
    Vector((-16.0, -18.0, 0.3)),
    Vector(( -6.0, -22.0, 0.3))
]
mtn_samples = sample_curve(mtn_ctrl, 160)
num_pts = len(mtn_samples)

bm_road = bmesh.new()
bm_guard = bmesh.new()
bm_stripes = bmesh.new()
bm_posts = bmesh.new()
bm_left_cliff = bmesh.new() # CONTINUOUS ROCK CLIFF WALL HUGGING LEFT SIDE OF ROAD!

up = Vector((0, 0, 1))
ring_al = []
ring_ar = []
ring_cl = []
ring_cr = []
ring_gb = []
ring_gt = []

# Left Cliff Wall rings (4 vertical elevation tiers along the left side!)
ring_cliff_foot = []
ring_cliff_mid  = []
ring_cliff_top  = []
ring_cliff_peak = []

tangents = []
rights = []

for i in range(num_pts):
    curr = mtn_samples[i]
    next_pt = mtn_samples[(i + 1) % num_pts]
    tan = (next_pt - curr).normalized()
    right = tan.cross(up).normalized()
    tangents.append(tan)
    rights.append(right)

    # Road surface (asphalt width 6.4m, curbs 0.35m)
    p_cl = curr - right * 3.55 + Vector((0, 0, 0.10))
    p_al = curr - right * 3.20 + Vector((0, 0, 0.02))
    p_ar = curr + right * 3.20 + Vector((0, 0, 0.02))
    p_cr = curr + right * 3.55 + Vector((0, 0, 0.10))

    ring_cl.append(bm_road.verts.new(p_cl))
    ring_al.append(bm_road.verts.new(p_al))
    ring_ar.append(bm_road.verts.new(p_ar))
    ring_cr.append(bm_road.verts.new(p_cr))

    # Right Guardrail (along cliff drop-off side)
    p_gb = p_cr + right * 0.12 + Vector((0, 0, 0.38))
    p_gt = p_cr + right * 0.12 + Vector((0, 0, 0.70))
    ring_gb.append(bm_guard.verts.new(p_gb))
    ring_gt.append(bm_guard.verts.new(p_gt))

    # LEFT-SIDE CONTINUOUS MOUNTAIN CLIFF WALL (HUGGING THE ROAD!):
    # Tier 1 (Foot of cliff): 4.5m left, rises 0.8m above road
    p_c_foot = curr - right * 4.6 + Vector((0, 0, 0.85))
    # Tier 2 (Mid rock face): 6.5m left, rises 4.2m above road
    p_c_mid  = curr - right * (6.5 + math.sin(i * 0.3)*0.6) + Vector((0, 0, 4.2 + math.cos(i * 0.2)*0.8))
    # Tier 3 (Upper cliff ridge): 9.0m left, rises 8.5m above road
    p_c_top  = curr - right * (9.0 + math.cos(i * 0.2)*0.8) + Vector((0, 0, 8.5 + math.sin(i * 0.3)*1.2))
    # Tier 4 (Mountain peak summit): 13.0m left, rises 14.5m above road
    p_c_peak = curr - right * 13.5 + Vector((0, 0, 14.5 + math.cos(i * 0.4)*2.0))

    ring_cliff_foot.append(bm_left_cliff.verts.new(p_c_foot))
    ring_cliff_mid.append(bm_left_cliff.verts.new(p_c_mid))
    ring_cliff_top.append(bm_left_cliff.verts.new(p_c_top))
    ring_cliff_peak.append(bm_left_cliff.verts.new(p_c_peak))

# SHARED QUAD FACES
for i in range(num_pts):
    next_i = (i + 1) % num_pts

    # Road & Curbs
    bm_road.faces.new((ring_al[i], ring_ar[i], ring_ar[next_i], ring_al[next_i]))
    bm_road.faces.new((ring_cl[i], ring_al[i], ring_al[next_i], ring_cl[next_i]))
    bm_road.faces.new((ring_ar[i], ring_cr[i], ring_cr[next_i], ring_ar[next_i]))
    bm_guard.faces.new((ring_gb[i], ring_gt[i], ring_gt[next_i], ring_gb[next_i]))

    # LEFT MOUNTAIN CLIFF WALL: Connected quad strips running along the entire road!
    # Foot to curb
    bm_left_cliff.faces.new((ring_cliff_foot[i], ring_cliff_mid[i], ring_cliff_mid[next_i], ring_cliff_foot[next_i]))
    # Mid to top
    bm_left_cliff.faces.new((ring_cliff_mid[i], ring_cliff_top[i], ring_cliff_top[next_i], ring_cliff_mid[next_i]))
    # Top to peak summit
    bm_left_cliff.faces.new((ring_cliff_top[i], ring_cliff_peak[i], ring_cliff_peak[next_i], ring_cliff_top[next_i]))

    # Yellow dashed stripes
    if (i % 3) == 0:
        c = mtn_samples[i]
        c_next = mtn_samples[next_i]
        r = rights[i]
        bm_stripes.faces.new((
            bm_stripes.verts.new(c - r*0.14 + Vector((0,0,0.04))),
            bm_stripes.verts.new(c + r*0.14 + Vector((0,0,0.04))),
            bm_stripes.verts.new(c_next + r*0.14 + Vector((0,0,0.04))),
            bm_stripes.verts.new(c_next - r*0.14 + Vector((0,0,0.04)))
        ))

    # Guardrail posts
    if (i % 4) == 0:
        p_base = ring_cr[i].co + rights[i] * 0.12
        p_top = p_base + Vector((0, 0, 0.70))
        r_p = rights[i] * 0.08
        bm_posts.faces.new((
            bm_posts.verts.new(p_base - r_p),
            bm_posts.verts.new(p_base + r_p),
            bm_posts.verts.new(p_top + r_p),
            bm_posts.verts.new(p_top - r_p)
        ))

bmesh.ops.recalc_face_normals(bm_road, faces=bm_road.faces)
bmesh.ops.recalc_face_normals(bm_guard, faces=bm_guard.faces)
bmesh.ops.recalc_face_normals(bm_left_cliff, faces=bm_left_cliff.faces)

def finalize_mesh_obj(name, bm, mat, smooth=True):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    m.polygons.foreach_set("use_smooth", [smooth] * len(m.polygons))
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)
    return o

finalize_mesh_obj("SM_MtnRoad", bm_road, mm["asphalt"], smooth=True)
finalize_mesh_obj("SM_MtnStripes", bm_stripes, mm["stripe"], smooth=True)
finalize_mesh_obj("SM_MtnGuardrail", bm_guard, mm["guardrail"], smooth=True)
finalize_mesh_obj("SM_MtnPosts", bm_posts, mm["post"], smooth=False)

# The Left-Side Mountain Cliff Wall (Faceted, rugged rock face hugging the road!):
finalize_mesh_obj("SM_LeftCliffWall", bm_left_cliff, mm["cliff"], smooth=False)

# Valley Base Terrain (Resting under the valley)
bm_terr = bmesh.new()
grid_res = 36
grid_size = 94.0
step = grid_size / (grid_res - 1)
grid_v = []
for iy in range(grid_res):
    row = []
    y = -grid_size / 2.0 + iy * step
    for ix in range(grid_res):
        x = -grid_size / 2.0 + ix * step
        # Base terrain depth
        z = math.sin(x*0.06)*math.cos(y*0.06)*2.0 - 0.5
        row.append(bm_terr.verts.new(Vector((x, y, max(-0.2, z)))))
    grid_v.append(row)

for iy in range(grid_res - 1):
    for ix in range(grid_res - 1):
        bm_terr.faces.new((grid_v[iy][ix], grid_v[iy][ix+1], grid_v[iy+1][ix+1], grid_v[iy+1][ix]))

finalize_mesh_obj("SM_ValleyBase", bm_terr, mm["valley"], smooth=False)

# Additional Majestic Mountain Peaks in background with Snowcaps
peaks = [
    ("Peak_East_Giant", 18.0, 28.0, ( 46.0,  12.0, 0.0), 8),
    ("Peak_North_Giant", 17.0, 26.0, (  4.0,  46.0, 0.0), 7),
    ("Peak_West_Giant", 18.0, 24.0, (-45.0,  12.0, 0.0), 8),
    ("Peak_South_Giant", 16.0, 20.0, ( 25.0, -45.0, 0.0), 7)
]
for name, rad, h, loc, verts in peaks:
    add_cone(f"{name}_Rock", rad, h, (loc[0], loc[1], loc[2] + h/2), mm["cliff"], vertices=verts)
    snow_h = h * 0.32
    add_cone(f"{name}_Snow", rad * 0.35, snow_h, (loc[0], loc[1], loc[2] + h - snow_h/2), mm["snow"], vertices=verts)

# Alpine Pine Groves placed along the left mountain cliff ledges!
for i in range(12, num_pts, 10):
    curr = mtn_samples[i]
    r = rights[i]
    # Place pine trees on the cliff ridge (7.5m to 10m left)
    px = curr.x - r.x * 8.0
    py = curr.y - r.y * 8.0
    pz = curr.z + 5.5
    add_cylinder(f"Cliff_PineTrunk_{i}", 0.2, 1.6, (px, py, pz + 0.8), mm["trunk"], vertices=6)
    for tier in range(3):
        r_tier = 1.3 - tier * 0.32
        h_tier = 1.6 - tier * 0.15
        z_tier = pz + 1.6 + tier * 0.9
        add_cone(f"Cliff_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), mm["pine"], vertices=6)

# Hero Orange Sports Coupe on Road
car_obj = build_car("Car_HeroOrange", mm["car_orange"], (mtn_samples[0].x, mtn_samples[0].y, mtn_samples[0].z + 0.04))

# Orient car forward
start_pt = mtn_samples[0]
start_next = mtn_samples[1]
start_tan = (start_next - start_pt).normalized()
yaw = math.atan2(start_tan.y, start_tan.x) - math.pi / 2
car_obj.rotation_mode = "XYZ"
car_obj.rotation_euler = (0, 0, yaw)

# Export mountain.glb
mtn_out = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(filepath=mtn_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Mountain Pass to {mtn_out}")

# --- RENDER SETUP ---
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

# Camera 1: GÓC GẦN (Chase Cam)
cam_close_data = bpy.data.cameras.new("Cam_Close")
cam_close_data.lens = 38
cam_close_obj = bpy.data.objects.new("Cam_Close", cam_close_data)
cam_close_pos = start_pt - start_tan * 7.0 + Vector((0, 0, 2.6))
cam_close_obj.location = cam_close_pos
look_target = start_pt + start_tan * 6.0 + Vector((0, 0, 0.8))
dir_vec = (look_target - cam_close_pos).normalized()
cam_close_obj.rotation_euler = dir_vec.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_close_obj)

# Camera 2: GÓC RỘNG (Panoramic Wide Cam)
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
bpy.context.scene.render.filepath = "/tmp/preview_mountain_cliff_close.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_mountain_cliff_close.png")

bpy.context.scene.camera = cam_wide_obj
bpy.context.scene.render.filepath = "/tmp/preview_mountain_cliff_wide.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_mountain_cliff_wide.png")
