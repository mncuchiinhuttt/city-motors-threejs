import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix

bpy.ops.wm.read_factory_settings(use_empty=True)

# --- 1. REALISTIC PBR MATERIALS (60-30-10 PALETTE) ---
def create_mat(name, color, roughness=0.6, metallic=0.0, alpha=1.0, is_transp=False):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if is_transp and "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
            mat.blend_method = "BLEND"
    return mat

mat_asphalt     = create_mat("MAT_Asphalt",     (0.18, 0.19, 0.21, 1.0), roughness=0.75)
mat_curb        = create_mat("MAT_Curb",        (0.82, 0.84, 0.86, 1.0), roughness=0.6)
mat_stripe_y    = create_mat("MAT_StripeY",     (0.98, 0.68, 0.05, 1.0), roughness=0.3)
mat_stripe_w    = create_mat("MAT_StripeW",     (0.95, 0.95, 0.98, 1.0), roughness=0.3)
mat_guardrail   = create_mat("MAT_Guardrail",   (0.98, 0.35, 0.05, 1.0), roughness=0.3, metallic=0.5) # Solid Orange!
mat_metal_post  = create_mat("MAT_MetalPost",   (0.40, 0.42, 0.45, 1.0), roughness=0.3, metallic=0.85)

# Layered Rock & Nature Materials
mat_rock_cliff  = create_mat("MAT_RockCliff",   (0.44, 0.42, 0.39, 1.0), roughness=0.9)
mat_dark_granite= create_mat("MAT_DarkGranite", (0.32, 0.30, 0.28, 1.0), roughness=0.9)
mat_alpine_moss = create_mat("MAT_AlpineMoss",  (0.28, 0.40, 0.22, 1.0), roughness=0.85)
mat_canyon_depth= create_mat("MAT_CanyonDepth", (0.22, 0.28, 0.20, 1.0), roughness=0.9)
mat_canyon_river= create_mat("MAT_CanyonRiver", (0.18, 0.45, 0.58, 1.0), roughness=0.15, metallic=0.7)
mat_snow_peak   = create_mat("MAT_SnowPeak",    (0.96, 0.97, 0.99, 1.0), roughness=0.4)

# Pine Trees
mat_pine_dark   = create_mat("MAT_PineDark",    (0.08, 0.26, 0.14, 1.0), roughness=0.85)
mat_pine_mid    = create_mat("MAT_PineMid",     (0.14, 0.34, 0.18, 1.0), roughness=0.85)
mat_pine_trunk  = create_mat("MAT_PineTrunk",   (0.28, 0.18, 0.12, 1.0), roughness=0.85)

# Atmospheric Canyon Mist (Semi-transparent fog layer in deep abyss!)
mat_canyon_mist = create_mat("MAT_CanyonMist",  (0.85, 0.92, 0.98, 1.0), roughness=0.9, alpha=0.45, is_transp=True)

# Hero Orange Sports Coupe
mat_car_orange  = create_mat("MAT_CarOrange",   (0.98, 0.35, 0.04, 1.0), roughness=0.18, metallic=0.5)
mat_car_black   = create_mat("MAT_CarBlack",    (0.08, 0.08, 0.10, 1.0), roughness=0.3, metallic=0.5)
mat_car_glass   = create_mat("MAT_CarGlass",    (0.06, 0.10, 0.14, 1.0), roughness=0.08, metallic=0.95)
mat_headlight   = create_mat("MAT_Headlight",   (1.0, 1.0, 0.95, 1.0), roughness=0.1)
mat_taillight   = create_mat("MAT_Taillight",   (1.0, 0.05, 0.05, 1.0), roughness=0.1)
mat_wheel_tire  = create_mat("MAT_WheelTire",   (0.05, 0.05, 0.06, 1.0), roughness=0.8)
mat_wheel_rim   = create_mat("MAT_WheelRim",    (0.82, 0.84, 0.86, 1.0), roughness=0.2, metallic=0.9)

# Helpers
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

# --- 2. AUTHENTIC TOUGE MOUNTAIN PASS SPLINE ---
# Elevated mountain road climbing from Z = 2.0m to 8.5m!
mtn_ctrl = [
    Vector(( -6.0, -22.0, 2.0)),  # Elevated mountain road!
    Vector((  8.0, -22.0, 2.6)),
    Vector(( 20.0, -17.0, 3.8)),
    Vector(( 26.0,  -8.0, 5.2)),
    Vector(( 20.0,   2.0, 6.5)),  # S-turn curve cutting inward
    Vector(( 24.0,  12.0, 7.8)),
    Vector(( 25.0,  20.0, 8.8)),  # High Summit Overlook!
    Vector(( 16.0,  26.0, 7.8)),  # Hairpin curve
    Vector((  4.0,  26.0, 6.4)),
    Vector(( -8.0,  22.0, 5.0)),
    Vector((-18.0,  14.0, 3.8)),
    Vector((-24.0,   4.0, 2.8)),
    Vector((-24.0,  -8.0, 2.4)),
    Vector((-16.0, -18.0, 2.0)),
    Vector(( -6.0, -22.0, 2.0))   # Closed loop
]
mtn_samples = sample_curve(mtn_ctrl, 180)
num_pts = len(mtn_samples)

# --- 3. WATERTIGHT ROAD + LEFT CLIFF WALL + RIGHT DEEP CANYON ---
bm_road       = bmesh.new()
bm_curbs      = bmesh.new()
bm_stripes    = bmesh.new()
bm_edge_lines = bmesh.new()
bm_guard      = bmesh.new()
bm_posts      = bmesh.new()
bm_left_cliff = bmesh.new()
bm_right_abyss= bmesh.new()

up = Vector((0, 0, 1))

# Ring buffers
ring_asphalt_l = []
ring_asphalt_r = []
ring_curb_l    = []
ring_curb_r    = []

# Left mountain wall rings (5 vertical tiers hugging the left side!)
ring_c0 = [] # Exactly at left curb (zero gap!)
ring_c1 = [] # Lower rocky ledge
ring_c2 = [] # Mid cliff face
ring_c3 = [] # Upper mountain ridge
ring_c4 = [] # Mountain summit ridge
ring_c5 = [] # Grounded skirt

# Right canyon abyss rings (Plunging 20 meters down into misty valley!)
ring_a0 = [] # At right curb (guardrail edge)
ring_a1 = [] # Steep cliff drop 4m down
ring_a2 = [] # Mid canyon terrace 10m down
ring_a3 = [] # Lower canyon slope 18m down
ring_a4 = [] # Canyon floor 24m down!

tangents = []
rights = []

for i in range(num_pts):
    curr = mtn_samples[i]
    next_pt = mtn_samples[(i + 1) % num_pts]
    tan = (next_pt - curr).normalized()
    right = tan.cross(up).normalized()
    tangents.append(tan)
    rights.append(right)

    # Road cross-section points (Asphalt width 6.6m, Curbs 0.35m each)
    p_cl = curr - right * 3.65 + Vector((0, 0, 0.08))
    p_al = curr - right * 3.30 + Vector((0, 0, 0.02))
    p_ar = curr + right * 3.30 + Vector((0, 0, 0.02))
    p_cr = curr + right * 3.65 + Vector((0, 0, 0.08))

    ring_curb_l.append(bm_road.verts.new(p_cl))
    ring_asphalt_l.append(bm_road.verts.new(p_al))
    ring_asphalt_r.append(bm_road.verts.new(p_ar))
    ring_curb_r.append(bm_road.verts.new(p_cr))

    # Guardrail W-Beam on the right cliff edge
    p_gb = p_cr + right * 0.10 + Vector((0, 0, 0.38))
    p_gt = p_cr + right * 0.10 + Vector((0, 0, 0.72))
    bm_guard.verts.new(p_gb)
    bm_guard.verts.new(p_gt)

    # LEFT MOUNTAIN WALL HUGGING THE ROAD (Seamless, zero holes!):
    # Tier 0: EXACTLY at p_cl
    ring_c0.append(bm_left_cliff.verts.new(p_cl))
    # Tier 1 (Lower rock shelf): 2.2m left, 2.5m above road
    p_c1 = curr - right * 5.5 + Vector((0, 0, 2.5 + math.sin(i * 0.25) * 0.5))
    ring_c1.append(bm_left_cliff.verts.new(p_c1))
    # Tier 2 (Mid rock cliff): 5.8m left, 6.5m above road
    p_c2 = curr - right * (8.5 + math.cos(i * 0.2) * 0.8) + Vector((0, 0, 6.5 + math.cos(i * 0.25) * 0.8))
    ring_c2.append(bm_left_cliff.verts.new(p_c2))
    # Tier 3 (Upper mountain ridge): 10.0m left, 11.5m above road
    p_c3 = curr - right * (13.5 + math.sin(i * 0.3) * 1.2) + Vector((0, 0, 11.5 + math.sin(i * 0.35) * 1.2))
    ring_c3.append(bm_left_cliff.verts.new(p_c3))
    # Tier 4 (Mountain summit peak): 16.0m left, 18.0m above road
    p_c4 = curr - right * 18.0 + Vector((0, 0, 18.0 + math.cos(i * 0.2) * 2.0))
    ring_c4.append(bm_left_cliff.verts.new(p_c4))
    # Tier 5 (Deep grounded skirt down into bedrock)
    p_c5 = curr - right * 24.0 - Vector((0, 0, 12.0))
    ring_c5.append(bm_left_cliff.verts.new(p_c5))

    # RIGHT DEEP CANYON & ABYSS (VỰC SÂU THĂM THẲM 24M!):
    # Tier 0: EXACTLY at p_cr
    ring_a0.append(bm_right_abyss.verts.new(p_cr))
    # Tier 1: Steep cliff plunge 4m down
    p_a1 = curr + right * 5.2 - Vector((0, 0, 4.0))
    ring_a1.append(bm_right_abyss.verts.new(p_a1))
    # Tier 2: Mid-canyon terrace 10m down
    p_a2 = curr + right * 13.5 - Vector((0, 0, 10.5))
    ring_a2.append(bm_right_abyss.verts.new(p_a2))
    # Tier 3: Lower canyon slope 18m down
    p_a3 = curr + right * 26.0 - Vector((0, 0, 17.5))
    ring_a3.append(bm_right_abyss.verts.new(p_a3))
    # Tier 4: Deep valley floor 24m down!
    p_a4 = curr + right * 42.0 - Vector((0, 0, 24.0))
    ring_a4.append(bm_right_abyss.verts.new(p_a4))

# Build Shared Quad Faces
guard_verts = list(bm_guard.verts)
for i in range(num_pts):
    next_i = (i + 1) % num_pts

    # Asphalt Center
    f_asp = bm_road.faces.new((
        ring_asphalt_l[i], ring_asphalt_r[i],
        ring_asphalt_r[next_i], ring_asphalt_l[next_i]
    ))
    f_asp.material_index = 0

    # Curbs (Connecting curb to asphalt seamlessly)
    f_cl = bm_road.faces.new((
        ring_curb_l[i], ring_asphalt_l[i],
        ring_asphalt_l[next_i], ring_curb_l[next_i]
    ))
    f_cl.material_index = 1

    f_cr = bm_road.faces.new((
        ring_asphalt_r[i], ring_curb_r[i],
        ring_curb_r[next_i], ring_asphalt_r[next_i]
    ))
    f_cr.material_index = 1
    # Guardrail Beam
    gv_b1 = guard_verts[i * 2]
    gv_t1 = guard_verts[i * 2 + 1]
    gv_b2 = guard_verts[next_i * 2]
    gv_t2 = guard_verts[next_i * 2 + 1]
    bm_guard.faces.new((gv_b1, gv_t1, gv_t2, gv_b2))

    # LEFT MOUNTAIN WALL STRIPS (Faceted rocky strata):
    bm_left_cliff.faces.new((ring_c0[i], ring_c1[i], ring_c1[next_i], ring_c0[next_i]))
    bm_left_cliff.faces.new((ring_c1[i], ring_c2[i], ring_c2[next_i], ring_c1[next_i]))
    bm_left_cliff.faces.new((ring_c2[i], ring_c3[i], ring_c3[next_i], ring_c2[next_i]))
    bm_left_cliff.faces.new((ring_c3[i], ring_c4[i], ring_c4[next_i], ring_c3[next_i]))
    bm_left_cliff.faces.new((ring_c4[i], ring_c5[i], ring_c5[next_i], ring_c4[next_i]))

    # RIGHT DEEP CANYON STRIPS (Plunging down 24m!):
    bm_right_abyss.faces.new((ring_a0[i], ring_a1[i], ring_a1[next_i], ring_a0[next_i]))
    bm_right_abyss.faces.new((ring_a1[i], ring_a2[i], ring_a2[next_i], ring_a1[next_i]))
    bm_right_abyss.faces.new((ring_a2[i], ring_a3[i], ring_a3[next_i], ring_a2[next_i]))
    bm_right_abyss.faces.new((ring_a3[i], ring_a4[i], ring_a4[next_i], ring_a3[next_i]))

    # Yellow Centerline Stripes (every 3rd step)
    if (i % 3) == 0:
        c = mtn_samples[i]
        c_next = mtn_samples[next_i]
        r = rights[i]
        bm_stripes.faces.new((
            bm_stripes.verts.new(c - r * 0.14 + Vector((0, 0, 0.04))),
            bm_stripes.verts.new(c + r * 0.14 + Vector((0, 0, 0.04))),
            bm_stripes.verts.new(c_next + r * 0.14 + Vector((0, 0, 0.04))),
            bm_stripes.verts.new(c_next - r * 0.14 + Vector((0, 0, 0.04)))
        ))

    # White Solid Edge Border Lines (Road markings on both edges)
    c = mtn_samples[i]
    c_next = mtn_samples[next_i]
    r = rights[i]
    # Left edge line
    bm_edge_lines.faces.new((
        bm_edge_lines.verts.new(c - r * 3.10 + Vector((0, 0, 0.03))),
        bm_edge_lines.verts.new(c - r * 2.95 + Vector((0, 0, 0.03))),
        bm_edge_lines.verts.new(c_next - r * 2.95 + Vector((0, 0, 0.03))),
        bm_edge_lines.verts.new(c_next - r * 3.10 + Vector((0, 0, 0.03)))
    ))
    # Right edge line
    bm_edge_lines.faces.new((
        bm_edge_lines.verts.new(c + r * 2.95 + Vector((0, 0, 0.03))),
        bm_edge_lines.verts.new(c + r * 3.10 + Vector((0, 0, 0.03))),
        bm_edge_lines.verts.new(c_next + r * 3.10 + Vector((0, 0, 0.03))),
        bm_edge_lines.verts.new(c_next + r * 2.95 + Vector((0, 0, 0.03)))
    ))

    # Metal Guardrail Posts
    if (i % 4) == 0:
        p_base = ring_curb_r[i].co + rights[i] * 0.10
        p_top  = p_base + Vector((0, 0, 0.72))
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

def finalize_obj(name, bm, mat, smooth=True):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    m.polygons.foreach_set("use_smooth", [smooth] * len(m.polygons))
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)
    return o
road_obj = finalize_obj("SM_AsphaltRoad", bm_road, mat_asphalt, smooth=True)
road_obj.data.materials.append(mat_curb)
finalize_obj("SM_StripesYellow", bm_stripes, mat_stripe_y, smooth=True)
finalize_obj("SM_EdgeLinesWhite", bm_edge_lines, mat_stripe_w, smooth=True)
finalize_obj("SM_GuardrailBeam", bm_guard, mat_guardrail, smooth=True)
finalize_obj("SM_GuardrailPosts", bm_posts, mat_metal_post, smooth=False)

# Left Mountain Wall (Faceted, rugged alpine rock face)
finalize_obj("SM_LeftCliffWall", bm_left_cliff, mat_rock_cliff, smooth=False)

# Right Deep Canyon Abyss (Plunging down 24m!)
finalize_obj("SM_RightDeepAbyss", bm_right_abyss, mat_rock_cliff, smooth=False)
# --- 4. DEEP VALLEY FLOOR & MIST POOL (SƯƠNG MÙ DƯỚI ĐÁY VỰC) ---
# Deep canyon floor at Z = -24.0m
add_box("SM_CanyonFloor", (140.0, 140.0, 2.0), (0, 0, -25.0), mat_canyon_depth)

# Winding Mountain River at the bottom of the canyon
add_box("SM_CanyonRiver", (14.0, 120.0, 0.4), (28.0, 0, -23.8), mat_canyon_river)

# Atmospheric Canyon Mist Layer (Semi-transparent floating mist planes pooling at Z = -14m and Z = -8m!)
add_box("SM_CanyonMist_Deep", (120.0, 120.0, 0.2), (15.0, 0, -14.0), mat_canyon_mist)
add_box("SM_CanyonMist_High", (100.0, 100.0, 0.2), (10.0, 0,  -8.0), mat_canyon_mist)

# --- 5. DENSE PINE FORESTS (HUNDREDS OF TREES AT ALL ELEVATIONS!) ---
print("Placing Dense Alpine Pine Forests...")
# 1. Trees on the left mountain cliff ledges (Hugging the left mountain wall!)
for i in range(6, num_pts, 6):
    curr = mtn_samples[i]
    r = rights[i]
    # Left cliff shelf
    px = curr.x - r.x * 6.5
    py = curr.y - r.y * 6.5
    pz = curr.z + 4.2
    add_cylinder(f"Left_PineTrunk_{i}", 0.24, 1.8, (px, py, pz + 0.9), mat_pine_trunk, vertices=6)
    # Tiered pine foliage
    for tier in range(3):
        r_tier = 1.4 - tier * 0.32
        h_tier = 1.6 - tier * 0.15
        z_tier = pz + 1.8 + tier * 0.95
        pine_mat = mat_pine_dark if tier % 2 == 0 else mat_pine_mid
        add_cone(f"Left_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), pine_mat, vertices=6)

# 2. Trees on the right mid-canyon terrace (Tops visible looking down over the guardrail!)
for i in range(4, num_pts, 6):
    curr = mtn_samples[i]
    r = rights[i]
    # 13m right on the terrace, height Z = curr.z - 10.0m
    px = curr.x + r.x * 13.5
    py = curr.y + r.y * 13.5
    pz = curr.z - 10.2
    add_cylinder(f"Terrace_Trunk_{i}", 0.30, 2.5, (px, py, pz + 1.25), mat_pine_trunk, vertices=6)
    for tier in range(3):
        r_tier = 2.1 - tier * 0.45
        h_tier = 2.4 - tier * 0.20
        z_tier = pz + 2.5 + tier * 1.3
        pine_mat = mat_pine_dark if tier % 2 == 0 else mat_pine_mid
        add_cone(f"Terrace_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), pine_mat, vertices=6)

# 3. Dense pine groves deep in the canyon floor emerging from mist (Z = -24m)
deep_canyon_pines = [
    ( 15.0, -35.0, -24.0, 2.2), ( 25.0, -25.0, -24.0, 2.6), ( 35.0, -15.0, -24.0, 2.4),
    ( 38.0,   0.0, -24.0, 2.8), ( 35.0,  15.0, -24.0, 2.4), ( 25.0,  28.0, -24.0, 2.6),
    ( 15.0,  35.0, -24.0, 2.2), ( 42.0,  10.0, -24.0, 2.8), ( 45.0, -10.0, -24.0, 2.6),
    ( 50.0,   5.0, -24.0, 3.0), ( 48.0,  25.0, -24.0, 2.5), ( 45.0, -30.0, -24.0, 2.5),
    (  5.0, -42.0, -24.0, 2.0), ( -5.0, -38.0, -24.0, 2.2), (  5.0,  42.0, -24.0, 2.0)
]
for idx, (px, py, pz, psc) in enumerate(deep_canyon_pines):
    add_cylinder(f"Deep_PineTrunk_{idx}", 0.25 * psc, 2.2 * psc, (px, py, pz + 1.1 * psc), mat_pine_trunk, vertices=6)
    for tier in range(3):
        r_tier = (1.7 - tier * 0.4) * psc
        h_tier = (2.2 - tier * 0.25) * psc
        z_tier = pz + (2.2 + tier * 1.2) * psc
        pine_mat = mat_pine_dark if tier % 2 == 0 else mat_pine_mid
        add_cone(f"Deep_PineF_{idx}_{tier}", r_tier, h_tier, (px, py, z_tier), pine_mat, vertices=6)

# --- 6. MAJESTIC OPPOSITE CANYON WALL PEAKS (RISING ACROSS THE ABYSS) ---
peaks = [
    ("Peak_Canyon_East1", 22.0, 42.0, ( 55.0,  15.0, -24.0), 8),
    ("Peak_Canyon_East2", 20.0, 36.0, ( 52.0, -18.0, -24.0), 7),
    ("Peak_Canyon_North", 18.0, 32.0, (  5.0,  48.0, -24.0), 7),
    ("Peak_Canyon_South", 19.0, 34.0, ( 25.0, -48.0, -24.0), 8),
]
for name, rad, h, loc, verts in peaks:
    add_cone(f"{name}_Rock", rad, h, (loc[0], loc[1], loc[2] + h/2), mat_rock_cliff, vertices=verts)
    snow_h = h * 0.32
    add_cone(f"{name}_Snow", rad * 0.35, snow_h, (loc[0], loc[1], loc[2] + h - snow_h/2), mat_snow_peak, vertices=verts)

# --- 7. DETAILED HERO ORANGE SPORTS CAR ---
print("Building Hero Sports Car...")
car_root = bpy.data.objects.new("Car_BlueCoupe", None) # Matches Three.js ID!
start_pt = mtn_samples[0]
start_next = mtn_samples[1]
start_tan = (start_next - start_pt).normalized()

car_root.location = start_pt + Vector((0, 0, 0.04))
bpy.context.scene.collection.objects.link(car_root)

# Main Aerodynamic Chassis
lower = add_box("Car_Chassis", (2.0, 4.4, 0.65), (0, 0, 0.52), mat_car_orange)
lower.parent = car_root

# Front Lower Splitter (Black sports accent)
splitter = add_box("Car_Splitter", (2.05, 0.6, 0.08), (0, 2.0, 0.24), mat_car_black)
splitter.parent = car_root

# Cabin (Glossy tinted glass)
cabin = add_box("Car_Cabin", (1.56, 2.4, 0.60), (0, -0.28, 1.10), mat_car_glass)
cabin.parent = car_root

# Roof Cap
roof = add_box("Car_Roof", (1.48, 2.0, 0.08), (0, -0.28, 1.42), mat_car_orange)
roof.parent = car_root

# Rear Ducktail Sport Spoiler (At -Y rear!)
spoiler = add_box("Car_Spoiler", (1.85, 0.40, 0.10), (0, -2.15, 1.05), mat_car_orange)
spoiler.parent = car_root

# 4 Alloy Wheels with Brakes
wheel_coords = [(-1.05, 1.25, 0.38), (1.05, 1.25, 0.38), (-1.05, -1.25, 0.38), (1.05, -1.25, 0.38)]
for w_idx, (wx, wy, wz) in enumerate(wheel_coords):
    tire = add_cylinder(f"Car_Wheel_{w_idx}", 0.38, 0.28, (wx, wy, wz), mat_wheel_tire, vertices=12, rot=(0, math.pi/2, 0))
    tire.parent = car_root
    rx = wx + (0.02 if wx > 0 else -0.02)
    rim = add_cylinder(f"Car_Rim_{w_idx}", 0.24, 0.30, (rx, wy, wz), mat_wheel_rim, vertices=8, rot=(0, math.pi/2, 0))
    rim.parent = car_root

# Front LED Headlights (At +Y front!)
hl_l = add_box("Car_HL_L", (0.42, 0.1, 0.20), (-0.75, 2.21, 0.58), mat_headlight)
hl_r = add_box("Car_HL_R", (0.42, 0.1, 0.20), ( 0.75, 2.21, 0.58), mat_headlight)
hl_l.parent = car_root
hl_r.parent = car_root

# Rear Continuous LED Taillight Bar (At -Y rear!)
tl = add_box("Car_TL", (1.75, 0.1, 0.20), (0, -2.21, 0.58), mat_taillight)
tl.parent = car_root

# Orient car forward along road
yaw = math.atan2(start_tan.y, start_tan.x) - math.pi / 2
car_root.rotation_mode = "XYZ"
car_root.rotation_euler = (0, 0, yaw)

# Export mountain.glb
mtn_out = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(filepath=mtn_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Realistic Mountain Pass to {mtn_out}")

# --- 8. RENDER PREVIEWS (CLOSE CHASE VIEW & WIDE CANYON VIEW) ---
sun_data = bpy.data.lights.new(name="SunLight", type="SUN")
sun_data.energy = 3.8
sun_data.color = (1.0, 0.98, 0.93)
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

# Camera 1: GÓC GẦN (Chase Cam: 7.2m behind, 2.7m above, looking forward over hood down the winding pass!)
cam_close_data = bpy.data.cameras.new("Cam_Close")
cam_close_data.lens = 36
cam_close_obj = bpy.data.objects.new("Cam_Close", cam_close_data)
cam_close_pos = start_pt - start_tan * 7.2 + Vector((0, 0, 2.7))
cam_close_obj.location = cam_close_pos
look_target = start_pt + start_tan * 6.5 + Vector((0, 0, 0.6))
dir_vec = (look_target - cam_close_pos).normalized()
cam_close_obj.rotation_euler = dir_vec.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_close_obj)

# Camera 2: GÓC RỘNG (Panoramic Wide Cam looking down into the deep canyon abyss with mist and forests!)
cam_wide_data = bpy.data.cameras.new("Cam_Wide")
cam_wide_data.lens = 22
cam_wide_obj = bpy.data.objects.new("Cam_Wide", cam_wide_data)
cam_wide_pos = Vector((20.0, -44.0, 34.0))
cam_wide_obj.location = cam_wide_pos
dir_wide = (Vector((10.0, 0.0, -6.0)) - cam_wide_pos).normalized()
cam_wide_obj.rotation_euler = dir_wide.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.collection.objects.link(cam_wide_obj)

bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.image_settings.file_format = "PNG"

bpy.context.scene.camera = cam_close_obj
bpy.context.scene.render.filepath = "/tmp/preview_real_canyon_close.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_real_canyon_close.png")

bpy.context.scene.camera = cam_wide_obj
bpy.context.scene.render.filepath = "/tmp/preview_real_canyon_wide.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_real_canyon_wide.png")
