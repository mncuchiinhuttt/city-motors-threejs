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

mat_asphalt    = create_mat("MAT_Road",         (0.18, 0.19, 0.22, 1.0), roughness=0.8)
mat_stripe     = create_mat("MAT_StripeYellow", (0.98, 0.68, 0.05, 1.0), roughness=0.4)
mat_guardrail  = create_mat("MAT_Guardrail",    (0.98, 0.35, 0.05, 1.0), roughness=0.3, metallic=0.5) # Solid Orange!
mat_post       = create_mat("MAT_Post",         (0.45, 0.47, 0.50, 1.0), roughness=0.3, metallic=0.8)

mat_cliff      = create_mat("MAT_Cliff",        (0.48, 0.46, 0.42, 1.0), roughness=0.9)
mat_canyon_rock= create_mat("MAT_CanyonRock",   (0.40, 0.38, 0.35, 1.0), roughness=0.9)
mat_valley_deep= create_mat("MAT_ValleyDeep",   (0.28, 0.42, 0.24, 1.0), roughness=0.85) # Deep forest floor
mat_river      = create_mat("MAT_River",        (0.20, 0.48, 0.65, 1.0), roughness=0.1, metallic=0.7) # River at bottom!
mat_snow       = create_mat("MAT_Snow",         (0.96, 0.97, 0.99, 1.0), roughness=0.4)
mat_trunk      = create_mat("MAT_Trunk",        (0.30, 0.20, 0.14, 1.0), roughness=0.85)
mat_pine       = create_mat("MAT_Pine",         (0.10, 0.30, 0.16, 1.0), roughness=0.85)

mat_car_body   = create_mat("MAT_CarBody",      (0.98, 0.35, 0.04, 1.0), roughness=0.2, metallic=0.5) # Hero Orange!
mat_car_glass  = create_mat("MAT_CarGlass",     (0.08, 0.12, 0.16, 1.0), roughness=0.1, metallic=0.9)
mat_wheel      = create_mat("MAT_Wheel",        (0.06, 0.06, 0.07, 1.0), roughness=0.8)
mat_rim        = create_mat("MAT_Rim",          (0.82, 0.84, 0.86, 1.0), roughness=0.25, metallic=0.85)
mat_headlight  = create_mat("MAT_Headlight",    (1.0, 1.0, 0.95, 1.0), roughness=0.1)
mat_taillight  = create_mat("MAT_Taillight",    (1.0, 0.05, 0.05, 1.0), roughness=0.1)

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

def add_box(name, size, loc, mat, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    return obj

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

# --- 2. ELEVATED TOUGE MOUNTAIN PASS SPLINE ---
# Mountain pass runs at high elevation (Z = 4.0m to 12.0m!) so looking over the guardrail
# drops into an immense deep abyss!
mtn_ctrl = [
    Vector(( -6.0, -22.0, 4.0)),  # Elevated mountain road!
    Vector((  8.0, -22.0, 4.6)),
    Vector(( 20.0, -17.0, 5.8)),
    Vector(( 26.0,  -8.0, 7.2)),
    Vector(( 20.0,   2.0, 8.5)),  # S-turn curve cutting inward
    Vector(( 24.0,  12.0, 10.2)),
    Vector(( 25.0,  20.0, 11.5)), # High Summit Overlook!
    Vector(( 16.0,  26.0, 10.5)), # Hairpin curve
    Vector((  4.0,  26.0, 9.0)),
    Vector(( -8.0,  22.0, 7.5)),
    Vector((-18.0,  14.0, 6.0)),
    Vector((-24.0,   4.0, 5.0)),
    Vector((-24.0,  -8.0, 4.4)),
    Vector((-16.0, -18.0, 4.0)),
    Vector(( -6.0, -22.0, 4.0))   # Closed loop
]
mtn_samples = sample_curve(mtn_ctrl, 160)
num_pts = len(mtn_samples)

# --- 3. WATERTIGHT UNIFIED MESH: ROAD + LEFT CLIFF + RIGHT DEEP ABYSS ---
bm_road = bmesh.new()
bm_guard = bmesh.new()
bm_stripes = bmesh.new()
bm_posts = bmesh.new()
bm_left_cliff = bmesh.new() # Vách núi sừng sững bên trái
bm_right_abyss = bmesh.new() # VỰC SÂU THĂM THẲM BÊN PHẢI!

up = Vector((0, 0, 1))

ring_cl = []
ring_al = []
ring_ar = []
ring_cr = []

# Left Cliff Rings (Hugging road curb!)
ring_c0 = []
ring_c1 = []
ring_c2 = []
ring_c3 = []

# Right Abyss Rings (Plunging down 15m to 25m into the valley floor!)
ring_a0 = [] # At right curb
ring_a1 = [] # Steep cliff drop 4m down
ring_a2 = [] # Mid terrace 10m down
ring_a3 = [] # Deep canyon floor 22m down!

tangents = []
rights = []

for i in range(num_pts):
    curr = mtn_samples[i]
    next_pt = mtn_samples[(i + 1) % num_pts]
    tan = (next_pt - curr).normalized()
    right = tan.cross(up).normalized()
    tangents.append(tan)
    rights.append(right)

    # Road cross-section points (width = 6.4m asphalt + 0.35m curbs)
    p_cl = curr - right * 3.55 + Vector((0, 0, 0.10))
    p_al = curr - right * 3.20 + Vector((0, 0, 0.02))
    p_ar = curr + right * 3.20 + Vector((0, 0, 0.02))
    p_cr = curr + right * 3.55 + Vector((0, 0, 0.10))

    ring_cl.append(bm_road.verts.new(p_cl))
    ring_al.append(bm_road.verts.new(p_al))
    ring_ar.append(bm_road.verts.new(p_ar))
    ring_cr.append(bm_road.verts.new(p_cr))

    # Guardrail points along the cliff edge
    p_gb = p_cr + right * 0.10 + Vector((0, 0, 0.38))
    p_gt = p_cr + right * 0.10 + Vector((0, 0, 0.72))
    bm_guard.verts.new(p_gb)
    bm_guard.verts.new(p_gt)

    # LEFT MOUNTAIN CLIFF WALL (Rises straight up from the left curb!):
    # Tier 0 (Foot): EXACTLY at p_cl (Zero gap!)
    v_c0 = bm_left_cliff.verts.new(p_cl)
    # Tier 1 (Lower rock cliff): 2.5m left, rises 3.5m above road
    p_c1 = curr - right * 5.8 + Vector((0, 0, 3.5 + math.sin(i * 0.25) * 0.6))
    v_c1 = bm_left_cliff.verts.new(p_c1)
    # Tier 2 (Mid mountain ridge): 6.5m left, rises 8.5m above road
    p_c2 = curr - right * (9.5 + math.cos(i * 0.2) * 0.8) + Vector((0, 0, 8.5 + math.cos(i * 0.25) * 1.0))
    v_c2 = bm_left_cliff.verts.new(p_c2)
    # Tier 3 (Peak summit): 12.0m left, rises 16.0m above road
    p_c3 = curr - right * 15.0 + Vector((0, 0, 16.0 + math.sin(i * 0.3) * 1.5))
    v_c3 = bm_left_cliff.verts.new(p_c3)

    ring_c0.append(v_c0)
    ring_c1.append(v_c1)
    ring_c2.append(v_c2)
    ring_c3.append(v_c3)

    # RIGHT-SIDE DEEP ABYSS & CANYON (VỰC SÂU THĂM THẲM BÊN PHẢI!):
    # Tier 0 (Edge): EXACTLY at p_cr (Right on the guardrail edge!)
    v_a0 = bm_right_abyss.verts.new(p_cr)
    # Tier 1 (Steep cliff plunge): Drops 4.5m down at steep 75-degree angle!
    p_a1 = curr + right * 5.2 - Vector((0, 0, 4.5))
    v_a1 = bm_right_abyss.verts.new(p_a1)
    # Tier 2 (Mid-canyon terrace): Spans outward 12m, drops 12.0m down!
    p_a2 = curr + right * 14.0 - Vector((0, 0, 12.0))
    v_a2 = bm_right_abyss.verts.new(p_a2)
    # Tier 3 (Deep valley floor): Spans outward 32m into the canyon, drops 22.0m down!
    p_a3 = curr + right * 36.0 - Vector((0, 0, 22.0))
    v_a3 = bm_right_abyss.verts.new(p_a3)

    ring_a0.append(v_a0)
    ring_a1.append(v_a1)
    ring_a2.append(v_a2)
    ring_a3.append(v_a3)

# Build Shared Quad Faces
guard_verts = list(bm_guard.verts)
for i in range(num_pts):
    next_i = (i + 1) % num_pts

    # Road surface
    bm_road.faces.new((ring_al[i], ring_ar[i], ring_ar[next_i], ring_al[next_i]))
    bm_road.faces.new((ring_cl[i], ring_al[i], ring_al[next_i], ring_cl[next_i]))
    bm_road.faces.new((ring_ar[i], ring_cr[i], ring_cr[next_i], ring_ar[next_i]))

    # Guardrail beam
    gv_b1 = guard_verts[i * 2]
    gv_t1 = guard_verts[i * 2 + 1]
    gv_b2 = guard_verts[next_i * 2]
    gv_t2 = guard_verts[next_i * 2 + 1]
    bm_guard.faces.new((gv_b1, gv_t1, gv_t2, gv_b2))

    # LEFT MOUNTAIN WALL (Connected to left curb):
    bm_left_cliff.faces.new((ring_c0[i], ring_c1[i], ring_c1[next_i], ring_c0[next_i]))
    bm_left_cliff.faces.new((ring_c1[i], ring_c2[i], ring_c2[next_i], ring_c1[next_i]))
    bm_left_cliff.faces.new((ring_c2[i], ring_c3[i], ring_c3[next_i], ring_c2[next_i]))

    # RIGHT DEEP ABYSS (Connected to right curb, plunging deep down!):
    bm_right_abyss.faces.new((ring_a0[i], ring_a1[i], ring_a1[next_i], ring_a0[next_i]))
    bm_right_abyss.faces.new((ring_a1[i], ring_a2[i], ring_a2[next_i], ring_a1[next_i]))
    bm_right_abyss.faces.new((ring_a2[i], ring_a3[i], ring_a3[next_i], ring_a2[next_i]))

    # Yellow stripes
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
        p_base = ring_cr[i].co + rights[i] * 0.10
        p_top = p_base + Vector((0, 0, 0.72))
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
bmesh.ops.recalc_face_normals(bm_right_abyss, faces=bm_right_abyss.faces)

def finalize_mesh_obj(name, bm, mat, smooth=True):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    m.polygons.foreach_set("use_smooth", [smooth] * len(m.polygons))
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)
    return o

finalize_mesh_obj("SM_MtnRoad", bm_road, mat_asphalt, smooth=True)
finalize_mesh_obj("SM_MtnStripes", bm_stripes, mat_stripe, smooth=True)
finalize_mesh_obj("SM_MtnGuardrail", bm_guard, mat_guardrail, smooth=True)
finalize_mesh_obj("SM_MtnPosts", bm_posts, mat_post, smooth=False)

# Left Mountain Cliff Wall (Faceted, rugged rock face)
finalize_mesh_obj("SM_LeftCliffWall", bm_left_cliff, mat_cliff, smooth=False)

# Right Deep Abyss & Canyon Slopes (Plunging down 22m below the road!)
finalize_mesh_obj("SM_RightDeepAbyss", bm_right_abyss, mat_canyon_rock, smooth=False)

# Deep Valley Floor at bottom of the canyon (Z = -22.0m!)
add_box("SM_DeepValleyFloor", (140.0, 140.0, 2.0), (0, 0, -23.0), mat_valley_deep)

# Winding Mountain River at the bottom of the canyon
add_box("SM_CanyonRiver", (12.0, 120.0, 0.4), (28.0, 0, -21.8), mat_river)

# DENSE ALPINE PINE FORESTS IN THE DEEP VALLEY & CANYON TERRACES:
# 1. Trees on the mid-canyon terrace below the road (tops visible looking down over guardrail!)
for i in range(5, num_pts, 8):
    curr = mtn_samples[i]
    r = rights[i]
    # 14m right on mid-terrace, height Z = curr.z - 11.5m
    px = curr.x + r.x * 14.0
    py = curr.y + r.y * 14.0
    pz = curr.z - 11.5
    add_cylinder(f"Terrace_PineTrunk_{i}", 0.3, 2.8, (px, py, pz + 1.4), mat_trunk, vertices=6)
    for tier in range(3):
        r_tier = 2.0 - tier * 0.45
        h_tier = 2.4 - tier * 0.25
        z_tier = pz + 2.6 + tier * 1.3
        add_cone(f"Terrace_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), mat_pine, vertices=6)

# 2. Dense pine groves in the deep valley floor (Z = -22m)
deep_pines = [
    ( 15.0, -35.0, -22.0, 1.8), ( 25.0, -25.0, -22.0, 2.2), ( 35.0, -15.0, -22.0, 2.0),
    ( 38.0,   0.0, -22.0, 2.5), ( 35.0,  15.0, -22.0, 2.0), ( 25.0,  28.0, -22.0, 2.2),
    ( 15.0,  35.0, -22.0, 1.8), ( 42.0,  10.0, -22.0, 2.4), ( 45.0, -10.0, -22.0, 2.2),
    ( 50.0,   5.0, -22.0, 2.6), ( 48.0,  25.0, -22.0, 2.0), ( 45.0, -30.0, -22.0, 2.0)
]
for idx, (px, py, pz, psc) in enumerate(deep_pines):
    add_cylinder(f"Valley_PineTrunk_{idx}", 0.25 * psc, 2.0 * psc, (px, py, pz + 1.0 * psc), mat_trunk, vertices=6)
    for tier in range(3):
        r_tier = (1.6 - tier * 0.4) * psc
        h_tier = (2.0 - tier * 0.25) * psc
        z_tier = pz + (2.0 + tier * 1.1) * psc
        add_cone(f"Valley_PineF_{idx}_{tier}", r_tier, h_tier, (px, py, z_tier), mat_pine, vertices=6)

# 3. Pine trees on the left cliff mountain ridge
for i in range(8, num_pts, 10):
    curr = mtn_samples[i]
    r = rights[i]
    px = curr.x - r.x * 7.5
    py = curr.y - r.y * 7.5
    pz = curr.z + 5.5
    add_cylinder(f"Cliff_PineTrunk_{i}", 0.22, 1.8, (px, py, pz + 0.9), mat_trunk, vertices=6)
    for tier in range(3):
        r_tier = 1.35 - tier * 0.32
        h_tier = 1.6 - tier * 0.15
        z_tier = pz + 1.8 + tier * 0.95
        add_cone(f"Cliff_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), mat_pine, vertices=6)

# OPPOSITE CANYON WALL: Majestic Mountain Peaks on the other side of the abyss (X >= 50)!
opposite_peaks = [
    ("CanyonPeak_1", 22.0, 38.0, ( 55.0,  15.0, -22.0), 8),
    ("CanyonPeak_2", 20.0, 32.0, ( 52.0, -18.0, -22.0), 7),
    ("CanyonPeak_3", 18.0, 28.0, ( 48.0,  35.0, -22.0), 7),
    ("CanyonPeak_4", 19.0, 30.0, ( 46.0, -40.0, -22.0), 8),
]
for name, rad, h, loc, verts in opposite_peaks:
    add_cone(f"{name}_Rock", rad, h, (loc[0], loc[1], loc[2] + h/2), mat_cliff, vertices=verts)
    snow_h = h * 0.32
    add_cone(f"{name}_Snow", rad * 0.35, snow_h, (loc[0], loc[1], loc[2] + h - snow_h/2), mat_snow, vertices=verts)

# HERO ORANGE SPORTS COUPE:
# Sits directly on the elevated mountain road at sample 0!
start_pt = mtn_samples[0]
start_next = mtn_samples[1]
start_tan = (start_next - start_pt).normalized()

# Build car with Front at +Y, Rear at -Y
def build_car(name, body_mat, loc=(0,0,0)):
    root = bpy.data.objects.new(name, None)
    root.location = loc
    bpy.context.scene.collection.objects.link(root)

    lower = add_box(f"{name}_LowerBody", (1.9, 4.2, 0.65), (0, 0, 0.52), body_mat)
    lower.parent = root

    cabin = add_box(f"{name}_Cabin", (1.52, 2.2, 0.58), (0, -0.25, 1.08), mat_car_glass)
    cabin.parent = root

    roof = add_box(f"{name}_RoofCap", (1.46, 1.9, 0.08), (0, -0.25, 1.40), body_mat)
    roof.parent = root

    spoiler = add_box(f"{name}_Spoiler", (1.8, 0.35, 0.08), (0, -2.0, 1.05), body_mat)
    spoiler.parent = root

    wheel_coords = [(-1.0, 1.2, 0.36), (1.0, 1.2, 0.36), (-1.0, -1.2, 0.36), (1.0, -1.2, 0.36)]
    for w_idx, (wx, wy, wz) in enumerate(wheel_coords):
        tire = add_cylinder(f"{name}_Wheel_{w_idx}", 0.36, 0.26, (wx, wy, wz), mat_wheel, vertices=12, rot=(0, math.pi/2, 0))
        tire.parent = root
        rx = wx + (0.02 if wx > 0 else -0.02)
        rim = add_cylinder(f"{name}_Rim_{w_idx}", 0.22, 0.28, (rx, wy, wz), mat_rim, vertices=8, rot=(0, math.pi/2, 0))
        rim.parent = root

    hl_l = add_box(f"{name}_HL_L", (0.38, 0.1, 0.18), (-0.7, 2.11, 0.58), mat_headlight)
    hl_r = add_box(f"{name}_HL_R", (0.38, 0.1, 0.18), ( 0.7, 2.11, 0.58), mat_headlight)
    hl_l.parent = root
    hl_r.parent = root

    tl = add_box(f"{name}_TL", (1.65, 0.1, 0.18), (0, -2.11, 0.58), mat_taillight)
    tl.parent = root
    return root

car_obj = build_car("Car_HeroOrange", mat_car_body, (start_pt.x, start_pt.y, start_pt.z + 0.04))
yaw = math.atan2(start_tan.y, start_tan.x) - math.pi / 2
car_obj.rotation_mode = "XYZ"
car_obj.rotation_euler = (0, 0, yaw)

# Export mountain.glb
mtn_out = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(filepath=mtn_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Deep Canyon Mountain Pass to {mtn_out}")

# --- RENDER CHASE VIEW PREVIEW ---
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

# Camera 1: GÓC GẦN (Chase Cam - angled so you look forward at road AND see the deep canyon on right!)
cam_close_data = bpy.data.cameras.new("Cam_Close")
cam_close_data.lens = 36
cam_close_obj = bpy.data.objects.new("Cam_Close", cam_close_data)
# 7.2m behind, 2.7m above
cam_close_pos = start_pt - start_tan * 7.2 + Vector((0, 0, 2.7))
cam_close_obj.location = cam_close_pos

look_target = start_pt + start_tan * 6.5 + Vector((0, 0, 0.6))
dir_vec = (look_target - cam_close_pos).normalized()
cam_close_obj.rotation_euler = dir_vec.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_close_obj)

# Camera 2: GÓC RỘNG (Panoramic Canyon View looking down into the deep valley!)
cam_wide_data = bpy.data.cameras.new("Cam_Wide")
cam_wide_data.lens = 22
cam_wide_obj = bpy.data.objects.new("Cam_Wide", cam_wide_data)
cam_wide_pos = Vector((18.0, -42.0, 32.0))
cam_wide_obj.location = cam_wide_pos
dir_wide = (Vector((10.0, 0.0, -5.0)) - cam_wide_pos).normalized()
cam_wide_obj.rotation_euler = dir_wide.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_wide_obj)

bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.image_settings.file_format = "PNG"

# Render Close
bpy.context.scene.camera = cam_close_obj
bpy.context.scene.render.filepath = "/tmp/preview_deep_canyon_close.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_deep_canyon_close.png")

# Render Wide
bpy.context.scene.camera = cam_wide_obj
bpy.context.scene.render.filepath = "/tmp/preview_deep_canyon_wide.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_deep_canyon_wide.png")

print("Deep Canyon Mountain Renders Complete!")
