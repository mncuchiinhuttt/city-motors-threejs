import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix

bpy.ops.wm.read_factory_settings(use_empty=True)

# ==============================================================================
# 1. SCENE COLLECTIONS (ORGANIZED PER BLENDER-DIRECTOR STANDARDS)
# ==============================================================================
def create_collection(name, parent=None):
    col = bpy.data.collections.new(name)
    if parent:
        parent.children.link(col)
    else:
        bpy.context.scene.collection.children.link(col)
    return col

col_main   = create_collection("COL_TougeCanyonScene")
col_road   = create_collection("COL_RoadInfrastructure", col_main)
col_left   = create_collection("COL_LeftMountainCliff",  col_main)
col_canyon = create_collection("COL_RightCanyonAbyss",   col_main)
col_deck   = create_collection("COL_ObservationDeck",    col_main)
col_props  = create_collection("COL_HighwayProps",       col_main)
col_forest = create_collection("COL_AlpineForest",       col_main)
col_car    = create_collection("COL_HeroVehicle",        col_main)

# ==============================================================================
# 2. PBR SOLID MATERIALS (60-30-10 PALETTE - STRICT COLOR SCHEME)
# ==============================================================================
def create_mat(name, color, roughness=0.6, metallic=0.0, alpha=1.0, is_transp=False):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if is_transp:
            if "Alpha" in bsdf.inputs:
                bsdf.inputs["Alpha"].default_value = alpha
            try:
                mat.surface_render_method = 'BLENDED'
            except Exception:
                pass
    return mat

# Road Materials
mat_asphalt    = create_mat("MAT_Asphalt",     (0.12, 0.13, 0.14, 1.0), roughness=0.85)
mat_curb       = create_mat("MAT_Curb",        (0.82, 0.84, 0.86, 1.0), roughness=0.6)
mat_stripe_y   = create_mat("MAT_StripeY",     (0.98, 0.68, 0.05, 1.0), roughness=0.3)
mat_stripe_w   = create_mat("MAT_StripeW",     (0.95, 0.95, 0.98, 1.0), roughness=0.3)
mat_guardrail  = create_mat("MAT_Guardrail",   (0.98, 0.35, 0.05, 1.0), roughness=0.3, metallic=0.5) # Solid Orange!
mat_metal_post = create_mat("MAT_MetalPost",   (0.35, 0.37, 0.40, 1.0), roughness=0.3, metallic=0.85)

# Geological & Nature Materials
mat_rock_cliff = create_mat("MAT_RockCliff",   (0.44, 0.42, 0.39, 1.0), roughness=0.9)
mat_dark_rock  = create_mat("MAT_DarkRock",    (0.28, 0.27, 0.25, 1.0), roughness=0.9)
mat_canyon_bot = create_mat("MAT_CanyonBot",   (0.20, 0.25, 0.18, 1.0), roughness=0.95)
mat_river_water= create_mat("MAT_RiverWater",  (0.15, 0.52, 0.65, 1.0), roughness=0.15, metallic=0.7)
mat_waterfall  = create_mat("MAT_Waterfall",   (0.85, 0.95, 1.00, 1.0), roughness=0.2, metallic=0.1)
mat_snow_peak  = create_mat("MAT_SnowPeak",    (0.96, 0.97, 0.99, 1.0), roughness=0.4)

# Alpine Vegetation Materials
mat_pine_dark  = create_mat("MAT_PineDark",    (0.08, 0.26, 0.14, 1.0), roughness=0.85)
mat_pine_mid   = create_mat("MAT_PineMid",     (0.14, 0.35, 0.18, 1.0), roughness=0.85)
mat_pine_trunk = create_mat("MAT_PineTrunk",   (0.28, 0.18, 0.12, 1.0), roughness=0.85)
mat_moss_shrub = create_mat("MAT_MossShrub",   (0.22, 0.42, 0.18, 1.0), roughness=0.85)

# Atmospheric Mist Volumes (Soft blue-tinted atmospheric haze pooling in canyon)
mat_canyon_mist= create_mat("MAT_CanyonMist",  (0.85, 0.92, 0.98, 0.45), roughness=0.1, is_transp=True)

# Highway Props Materials
mat_chev_yellow= create_mat("MAT_ChevYellow",  (0.98, 0.85, 0.05, 1.0), roughness=0.3)
mat_chev_black = create_mat("MAT_ChevBlack",   (0.05, 0.05, 0.06, 1.0), roughness=0.5)
mat_km_red     = create_mat("MAT_KmRed",       (0.88, 0.15, 0.10, 1.0), roughness=0.4)
mat_km_white   = create_mat("MAT_KmWhite",     (0.92, 0.92, 0.95, 1.0), roughness=0.5)
mat_deck_floor = create_mat("MAT_DeckFloor",   (0.32, 0.33, 0.35, 1.0), roughness=0.8)
mat_deck_rail  = create_mat("MAT_DeckRail",    (0.18, 0.19, 0.22, 1.0), roughness=0.3, metallic=0.7)
mat_wood_bench = create_mat("MAT_WoodBench",   (0.45, 0.28, 0.16, 1.0), roughness=0.7)

# Vehicle Materials
mat_car_orange = create_mat("MAT_CarOrange",   (0.98, 0.42, 0.05, 1.0), roughness=0.25)
mat_car_glass  = create_mat("MAT_CarGlass",    (0.15, 0.18, 0.24, 1.0), roughness=0.1, metallic=0.8)
mat_wheel      = create_mat("MAT_Wheel",       (0.08, 0.08, 0.08, 1.0), roughness=0.8)
mat_rim        = create_mat("MAT_Rim",         (0.85, 0.85, 0.88, 1.0), roughness=0.2, metallic=0.9)
mat_headlight  = create_mat("MAT_Headlight",   (1.0, 1.0, 0.95, 1.0),   roughness=0.1)
mat_taillight  = create_mat("MAT_Taillight",   (1.0, 0.05, 0.05, 1.0),  roughness=0.1)

# Helpers for adding primitives directly into a specific collection
def add_box(name, size, loc, mat, col=col_props, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def add_cylinder(name, radius, depth, loc, mat, col=col_forest, vertices=8, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def add_cone(name, radius1, depth, loc, mat, col=col_forest, vertices=7, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, depth=depth, location=loc, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj

# ==============================================================================
# 3. SPLINE GEOMETRY - AUTHENTIC TOUGE MOUNTAIN PASS
# ==============================================================================
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

# Mountain control points in Blender (Z is Up, elevation 2.0m to 8.8m)
mtn_ctrl = [
    Vector(( -6.0, -22.0, 2.0)),  # Elevated mountain road
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

# ==============================================================================
# 4. WATERTIGHT ROAD + LEFT CLIFF WALL + RIGHT CANYON ABYSS
# ==============================================================================
bm_road        = bmesh.new()
bm_stripes_y   = bmesh.new()
bm_edge_lines  = bmesh.new()
bm_guard       = bmesh.new()
bm_posts       = bmesh.new()
bm_left_cliff  = bmesh.new()
bm_right_abyss = bmesh.new()

up = Vector((0, 0, 1))

# Rings for road and terrain
ring_curb_l = []
ring_asphalt_l = []
ring_asphalt_r = []
ring_curb_r = []

# Left mountain wall rings (5 vertical tiers hugging the left side!)
ring_c0 = [] # Exactly at left curb (zero gap!)
ring_c1 = [] # Lower rock shelf
ring_c2 = [] # Mid cliff face
ring_c3 = [] # Upper mountain ridge
ring_c4 = [] # Mountain summit ridge
ring_c5 = [] # Grounded skirt

# Right canyon abyss rings (Plunging 24m down into misty valley!)
ring_a0 = [] # At right curb (guardrail edge)
ring_a1 = [] # Steep cliff drop 4.5m down
ring_a2 = [] # Mid canyon terrace 11m down
ring_a3 = [] # Lower canyon slope 18m down
ring_a4 = [] # Canyon floor 24m down

tangents = []
rights = []

for i in range(num_pts):
    curr = mtn_samples[i]
    next_pt = mtn_samples[(i + 1) % num_pts]
    tan = (next_pt - curr).normalized()
    right = tan.cross(up).normalized()
    tangents.append(tan)
    rights.append(right)

    # Road cross-section points (Asphalt width 6.6m: Left lane [-3.3m..0], Right lane [0..+3.3m])
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

    # Yellow Dashed Center Line (Separating Left and Right Lanes)
    if (i % 6) < 4:
        p_yl = curr - right * 0.10 + Vector((0, 0, 0.035))
        p_yr = curr + right * 0.10 + Vector((0, 0, 0.035))
        next_curr = next_pt
        next_right = (mtn_samples[(i + 2) % num_pts] - next_curr).normalized().cross(up).normalized()
        p_ynl = next_curr - next_right * 0.10 + Vector((0, 0, 0.035))
        p_ynr = next_curr + next_right * 0.10 + Vector((0, 0, 0.035))
        bm_stripes_y.faces.new((
            bm_stripes_y.verts.new(p_yl),
            bm_stripes_y.verts.new(p_yr),
            bm_stripes_y.verts.new(p_ynr),
            bm_stripes_y.verts.new(p_ynl)
        ))

    # White Edge Lines (Left and Right lane outer boundaries)
    p_wl1 = curr - right * 3.15 + Vector((0, 0, 0.035))
    p_wl2 = curr - right * 2.95 + Vector((0, 0, 0.035))
    next_curr = next_pt
    next_right = (mtn_samples[(i + 2) % num_pts] - next_curr).normalized().cross(up).normalized()
    p_wnl1 = next_curr - next_right * 3.15 + Vector((0, 0, 0.035))
    p_wnl2 = next_curr - next_right * 2.95 + Vector((0, 0, 0.035))
    bm_edge_lines.faces.new((
        bm_edge_lines.verts.new(p_wl1),
        bm_edge_lines.verts.new(p_wl2),
        bm_edge_lines.verts.new(p_wnl2),
        bm_edge_lines.verts.new(p_wnl1)
    ))

    p_wr1 = curr + right * 2.95 + Vector((0, 0, 0.035))
    p_wr2 = curr + right * 3.15 + Vector((0, 0, 0.035))
    p_wnr1 = next_curr + next_right * 2.95 + Vector((0, 0, 0.035))
    p_wnr2 = next_curr + next_right * 3.15 + Vector((0, 0, 0.035))
    bm_edge_lines.faces.new((
        bm_edge_lines.verts.new(p_wr1),
        bm_edge_lines.verts.new(p_wr2),
        bm_edge_lines.verts.new(p_wnr2),
        bm_edge_lines.verts.new(p_wnr1)
    ))

    # SOLID CENTRAL MOUNTAIN MASSIF:
    # Interpolating from central summit peak (3.36, 2.21, 26.5) down to the left curb p_cl
    ring_c0.append(bm_left_cliff.verts.new(p_cl)) # Exactly at curb edge

    peak_x, peak_y, peak_z = 3.36, 2.21, 26.5
    # Tier 1 (Lower mountain slope - 80% distance from peak to curb)
    p1_x = 0.20 * peak_x + 0.80 * p_cl.x
    p1_y = 0.20 * peak_y + 0.80 * p_cl.y
    p1_z = p_cl.z + 2.2 + math.sin(i * 0.35) * 0.5
    ring_c1.append(bm_left_cliff.verts.new(Vector((p1_x, p1_y, p1_z))))

    # Tier 2 (Mid alpine shelf - 55% distance)
    p2_x = 0.45 * peak_x + 0.55 * p_cl.x
    p2_y = 0.45 * peak_y + 0.55 * p_cl.y
    p2_z = 0.45 * peak_z + 0.55 * p_cl.z + math.cos(i * 0.3) * 0.8
    ring_c2.append(bm_left_cliff.verts.new(Vector((p2_x, p2_y, p2_z))))

    # Tier 3 (High rocky crags - 30% distance)
    p3_x = 0.70 * peak_x + 0.30 * p_cl.x
    p3_y = 0.70 * peak_y + 0.30 * p_cl.y
    p3_z = 0.70 * peak_z + 0.30 * p_cl.z + math.sin(i * 0.25) * 1.0
    ring_c3.append(bm_left_cliff.verts.new(Vector((p3_x, p3_y, p3_z))))

    # Tier 4 (Summit crown around peak - 12% distance)
    p4_x = 0.88 * peak_x + 0.12 * p_cl.x
    p4_y = 0.88 * peak_y + 0.12 * p_cl.y
    p4_z = 24.2 + math.cos(i * 0.2) * 0.6
    ring_c4.append(bm_left_cliff.verts.new(Vector((p4_x, p4_y, p4_z))))
    # RIGHT CANYON ABYSS PLUNGING 24 METERS DOWN:
    ring_a0.append(bm_right_abyss.verts.new(p_cr))
    p_a1 = curr + right * 5.4 - Vector((0, 0, 4.5))
    ring_a1.append(bm_right_abyss.verts.new(p_a1))
    p_a2 = curr + right * 14.0 - Vector((0, 0, 11.0))
    ring_a2.append(bm_right_abyss.verts.new(p_a2))
    p_a3 = curr + right * 26.0 - Vector((0, 0, 18.0))
    ring_a3.append(bm_right_abyss.verts.new(p_a3))
    p_a4 = curr + right * 44.0 - Vector((0, 0, 24.0))
    ring_a4.append(bm_right_abyss.verts.new(p_a4))

# Build Quads for Road & Terrain
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

    # Guardrail W-Beam
    gv_b1 = guard_verts[i * 2]
    gv_t1 = guard_verts[i * 2 + 1]
    gv_b2 = guard_verts[next_i * 2]
    gv_t2 = guard_verts[next_i * 2 + 1]
    bm_guard.faces.new((gv_b1, gv_t1, gv_t2, gv_b2))

# Summit Apex Vertex for Solid Mountain Peak
v_summit_apex = bm_left_cliff.verts.new(Vector((3.36, 2.21, 26.5)))

for i in range(num_pts):
    next_i = (i + 1) % num_pts
    # Solid Mountain Facets connecting all tiers down to road curb seamlessly!
    bm_left_cliff.faces.new((v_summit_apex, ring_c4[i], ring_c4[next_i])) # Summit fan
    bm_left_cliff.faces.new((ring_c4[i], ring_c3[i], ring_c3[next_i], ring_c4[next_i]))
    bm_left_cliff.faces.new((ring_c3[i], ring_c2[i], ring_c2[next_i], ring_c3[next_i]))
    bm_left_cliff.faces.new((ring_c2[i], ring_c1[i], ring_c1[next_i], ring_c2[next_i]))
    bm_left_cliff.faces.new((ring_c1[i], ring_c0[i], ring_c0[next_i], ring_c1[next_i]))
    # Right Canyon Abyss Strips
    bm_right_abyss.faces.new((ring_a0[i], ring_a1[i], ring_a1[next_i], ring_a0[next_i]))
    bm_right_abyss.faces.new((ring_a1[i], ring_a2[i], ring_a2[next_i], ring_a1[next_i]))
    bm_right_abyss.faces.new((ring_a2[i], ring_a3[i], ring_a3[next_i], ring_a2[next_i]))
    bm_right_abyss.faces.new((ring_a3[i], ring_a4[i], ring_a4[next_i], ring_a3[next_i]))

    # Metal Guardrail Posts
    if (i % 4) == 0:
        p_base = ring_curb_r[i].co + rights[i] * 0.10
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

def finalize_obj(name, bm, mat, col, smooth=True):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    m.polygons.foreach_set("use_smooth", [smooth] * len(m.polygons))
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    col.objects.link(o)
    return o

road_obj = finalize_obj("SM_AsphaltRoad", bm_road, mat_asphalt, col_road, smooth=True)
road_obj.data.materials.append(mat_curb) # Slot 1 for curbs

finalize_obj("SM_StripesYellow", bm_stripes_y, mat_stripe_y, col_road, smooth=True)
finalize_obj("SM_EdgeLinesWhite", bm_edge_lines, mat_stripe_w, col_road, smooth=True)
finalize_obj("SM_GuardrailBeam", bm_guard, mat_guardrail, col_road, smooth=True)
finalize_obj("SM_GuardrailPosts", bm_posts, mat_metal_post, col_road, smooth=False)

finalize_obj("SM_LeftCliffWall", bm_left_cliff, mat_rock_cliff, col_left, smooth=False)
finalize_obj("SM_RightDeepAbyss", bm_right_abyss, mat_rock_cliff, col_canyon, smooth=False)

# ==============================================================================
# 5. CANYON FLOOR, TURQUOISE RIVER & WATERFALL
# ==============================================================================
# Deep valley floor at Z = -24.0m
add_box("SM_CanyonFloor", (150.0, 150.0, 2.0), (0, 0, -25.0), mat_canyon_bot, col=col_canyon)

# Meandering Mountain River at the bottom of the canyon
add_box("SM_CanyonRiver", (16.0, 140.0, 0.4), (28.0, 0, -23.8), mat_river_water, col=col_canyon)

# Mountain Waterfall cascading down the canyon cliff into the river
add_box("SM_WaterfallCascade", (3.0, 0.6, 22.0), (38.0, -12.0, -13.0), mat_waterfall, col=col_canyon)
add_box("SM_WaterfallSplash", (7.0, 7.0, 0.4), (38.0, -12.0, -23.6), mat_waterfall, col=col_canyon)

# Atmospheric Canyon Mist Volumes (Stepped triple-layer fog pooling in the canyon)
add_box("SM_CanyonMist_Deep", (130.0, 130.0, 0.25), (15.0, 0, -18.0), mat_canyon_mist, col=col_canyon)
add_box("SM_CanyonMist_Mid",  (110.0, 110.0, 0.25), (12.0, 0, -12.0), mat_canyon_mist, col=col_canyon)
add_box("SM_CanyonMist_High", (90.0,  90.0,  0.25), (10.0, 0,  -6.0), mat_canyon_mist, col=col_canyon)

# ==============================================================================
# 6. DISTANCE VALIDATION HELPER (PREVENT ANY CLIPPING WITH THE ROAD)
# ==============================================================================
def is_road_clear(x, y, min_dist=5.2):
    min_dist_sq = min_dist * min_dist
    for s in mtn_samples:
        if (x - s.x)**2 + (y - s.y)**2 < min_dist_sq:
            return False
    return True

# ==============================================================================
# 7. CANYON ROCK SPIRES & JAGGED GEOLOGICAL MONOLITHS (DEEP IN THE ABYSS)
# ==============================================================================
spires = [
    ("Spire_Needle_1", 3.2, 18.0, ( 18.0, -38.0, -24.0), 6),
    ("Spire_Needle_2", 4.2, 22.0, ( 35.0,  -8.0, -24.0), 7),
    ("Spire_Needle_3", 3.8, 20.0, ( 38.0,  18.0, -24.0), 6),
    ("Spire_Needle_4", 3.0, 16.0, ( 22.0,  38.0, -24.0), 5),
    ("Spire_Needle_5", 4.8, 24.0, ( 48.0,   2.0, -24.0), 7),
    ("Spire_Needle_6", 3.6, 17.0, ( 28.0, -32.0, -24.0), 6),
]
for name, rad, h, (sx, sy, sz), verts in spires:
    if is_road_clear(sx, sy, min_dist=rad + 2.5):
        add_cone(f"SM_{name}", rad, h, (sx, sy, sz + h/2), mat_dark_rock, col=col_canyon, vertices=verts)
        add_cone(f"SM_{name}_Base", rad * 1.5, h * 0.25, (sx, sy, sz + h * 0.12), mat_rock_cliff, col=col_canyon, vertices=verts)

# Canyon Boulders safely placed on lower slopes and valley floor
boulders = [
    (( 32.0, -14.0, -16.0), (3.2, 2.8, 2.5)),
    (( 36.0,  -8.0, -18.0), (2.8, 3.4, 2.2)),
    (( 42.0,   8.0, -20.0), (3.5, 3.0, 2.8)),
    (( 34.0,  22.0, -18.0), (2.8, 2.6, 2.3)),
    (( 28.0,  32.0, -17.0), (2.6, 3.2, 2.2)),
]
for idx, (bloc, bsize) in enumerate(boulders):
    if is_road_clear(bloc[0], bloc[1], min_dist=4.5):
        add_box(f"SM_CanyonBoulder_{idx}", bsize, bloc, mat_dark_rock, col=col_canyon, rotation=(0.2, 0.4, idx * 0.7))
print("Generating 250+ Alpine Pine Trees...")
# 1. Trees on the left mountain cliff ledges
for i in range(2, num_pts, 4):
    curr = mtn_samples[i]
    px = 0.45 * 3.36 + 0.55 * curr.x
    py = 0.45 * 2.21 + 0.55 * curr.y
    ground_z = 0.45 * 26.5 + 0.55 * curr.z
    if not is_road_clear(px, py, min_dist=5.2):
        continue
    # Trunk height 4.5m, embedded 2.0m deep into solid rock
    add_cylinder(f"L_Trunk_{i}", 0.30, 4.5, (px, py, ground_z + 0.25), mat_pine_trunk, col=col_forest, vertices=6)
    for tier in range(3):
        r_tier = 1.7 - tier * 0.38
        h_tier = 2.0 - tier * 0.20
        z_tier = ground_z + 2.4 + tier * 1.2
        pine_mat = mat_pine_dark if tier % 2 == 0 else mat_pine_mid
        add_cone(f"L_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), pine_mat, col=col_forest, vertices=6)

# 2. Trees on the right canyon slope (Deeply anchored 2.5m into rock slope, 100% zero floating!)
for i in range(1, num_pts, 3):
    curr = mtn_samples[i]
    r = rights[i]
    # Place on the slope between p_a1 (5.4m, drop 4.5m) and p_a2 (14.0m, drop 11.0m)
    u = 0.35 + ((i * 7) % 5) * 0.12 # u in [0.35..0.83]
    dist_r = 5.4 + u * (14.0 - 5.4)
    # Exact polygon surface height on the slope:
    ground_z = curr.z - (4.5 + u * (11.0 - 4.5))

    px = curr.x + r.x * dist_r
    py = curr.y + r.y * dist_r

    if not is_road_clear(px, py, min_dist=5.4):
        continue

    sc = 0.9 + (i % 3) * 0.25
    trunk_h = 5.2 * sc
    # Center trunk so bottom is sunk 2.2m UNDERGROUND!
    trunk_cz = ground_z + (trunk_h / 2.0 - 2.2 * sc)
    add_cylinder(f"R_Slope_Trunk_{i}", 0.32 * sc, trunk_h, (px, py, trunk_cz), mat_pine_trunk, col=col_forest, vertices=6)

    for tier in range(3):
        r_tier = (1.9 - tier * 0.40) * sc
        h_tier = (2.4 - tier * 0.25) * sc
        z_tier = ground_z + (2.6 + tier * 1.3) * sc
        pine_mat = mat_pine_dark if (i + tier) % 2 == 0 else mat_pine_mid
        add_cone(f"R_Slope_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), pine_mat, col=col_forest, vertices=6)

# 3. Dense groves deep in the canyon floor (Floor at Z = -24.0m, trunks sunk 2.0m deep)
random.seed(42)
for idx in range(45):
    px = random.uniform(5.0, 55.0)
    py = random.uniform(-45.0, 45.0)
    ground_z = -24.0
    if not is_road_clear(px, py, min_dist=5.2):
        continue
    psc = random.uniform(1.8, 3.2)
    trunk_h = 5.0 * psc
    trunk_cz = ground_z + (trunk_h / 2.0 - 2.0 * psc) # Sunk 2m below floor
    add_cylinder(f"Deep_Trunk_{idx}", 0.26 * psc, trunk_h, (px, py, trunk_cz), mat_pine_trunk, col=col_forest, vertices=6)
    for tier in range(3):
        r_tier = (1.8 - tier * 0.4) * psc
        h_tier = (2.4 - tier * 0.25) * psc
        z_tier = ground_z + (2.5 + tier * 1.3) * psc
        pine_mat = mat_pine_dark if tier % 2 == 0 else mat_pine_mid
        add_cone(f"Deep_PineF_{idx}_{tier}", r_tier, h_tier, (px, py, z_tier), pine_mat, col=col_forest, vertices=6)
# ==============================================================================
# 10. MAJESTIC OPPOSITE CANYON WALL PEAKS
# ==============================================================================
peaks = [
    ("Peak_Canyon_East1", 24.0, 46.0, ( 58.0,  15.0, -24.0), 8),
    ("Peak_Canyon_East2", 22.0, 40.0, ( 54.0, -18.0, -24.0), 7),
    ("Peak_Canyon_North", 20.0, 36.0, (  5.0,  52.0, -24.0), 7),
    ("Peak_Canyon_South", 21.0, 38.0, ( 25.0, -52.0, -24.0), 8),
]
for name, rad, h, loc, verts in peaks:
    add_cone(f"{name}_Rock", rad, h, (loc[0], loc[1], loc[2] + h/2), mat_rock_cliff, col=col_canyon, vertices=verts)
    snow_h = h * 0.32
    add_cone(f"{name}_Snow", rad * 0.35, snow_h, (loc[0], loc[1], loc[2] + h - snow_h/2), mat_snow_peak, col=col_canyon, vertices=verts)

# ==============================================================================
# 11. DETAILED HERO SPORTS CAR (POSITIONED IN RIGHT-HAND LANE!)
# ==============================================================================
print("Building Hero Sports Car...")
car_root = bpy.data.objects.new("Car_BlueCoupe", None) # Matches Three.js ID!
col_car.objects.link(car_root)

# Position car in right-hand traffic lane: +1.65m along the right vector!
start_idx = 8 # Around 5% along the spline
start_pt = mtn_samples[start_idx]
start_tan = tangents[start_idx]
start_r = rights[start_idx]
car_lane_pos = start_pt + start_r * 1.65 + Vector((0, 0, 0.04))
car_root.location = car_lane_pos

# Forward orientation along start_tan
yaw = math.atan2(start_tan.y, start_tan.x)
car_root.rotation_euler = (0, 0, yaw)

def add_car_box(name, size, loc, mat, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col_car.objects.link(obj)
    obj.parent = car_root
    return obj

def add_car_cylinder(name, radius, depth, loc, mat, vertices=12, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col_car.objects.link(obj)
    obj.parent = car_root
    return obj

# Body Lower
add_car_box("Car_Body_Lower", (1.9, 4.2, 0.65), (0, 0, 0.52), mat_car_orange)
# Cabin (Tapered sports greenhouse)
add_car_box("Car_Cabin", (1.52, 2.2, 0.58), (0, 0.25, 1.08), mat_car_glass)
# Roof cap
add_car_box("Car_Roof", (1.46, 1.9, 0.08), (0, 0.25, 1.40), mat_car_orange)
# Rear Sport Spoiler
add_car_box("Car_Spoiler", (1.8, 0.35, 0.08), (0, -2.0, 1.05), mat_car_orange)
add_car_box("Car_Spoiler_PostL", (0.08, 0.12, 0.32), (-0.7, -2.0, 0.85), mat_metal_post)
add_car_box("Car_Spoiler_PostR", (0.08, 0.12, 0.32), ( 0.7, -2.0, 0.85), mat_metal_post)

# 4 Wheels & Rims
wheel_coords = [(-1.0, -1.2, 0.36), (1.0, -1.2, 0.36), (-1.0, 1.2, 0.36), (1.0, 1.2, 0.36)]
for w_idx, (wx, wy, wz) in enumerate(wheel_coords):
    add_car_cylinder(f"Wheel_{w_idx}", 0.36, 0.26, (wx, wy, wz), mat_wheel, rot=(0, math.pi/2, 0))
    rim_x = wx + (0.02 if wx > 0 else -0.02)
    add_car_cylinder(f"Rim_{w_idx}", 0.22, 0.28, (rim_x, wy, wz), mat_rim, rot=(0, math.pi/2, 0))

# FRONT HEADLIGHTS (At +Y - pointing in direction of travel!)
add_car_box("Headlight_L", (0.38, 0.1, 0.18), (-0.7, 2.11, 0.58), mat_headlight)
add_car_box("Headlight_R", (0.38, 0.1, 0.18), ( 0.7, 2.11, 0.58), mat_headlight)

# REAR TAILLIGHT BAR (At -Y - facing backwards towards the chase cam!)
add_car_box("Taillight_Bar", (1.65, 0.1, 0.18), (0, -2.11, 0.58), mat_taillight)

# ==============================================================================
# 12. GLTF / GLB EXPORT
# ==============================================================================
glb_path = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    export_apply=True,
    export_yup=True
)
print(f"Exported Rich Mountain Canyon Pass to {glb_path}")

# ==============================================================================
# 13. CINEMATIC VALIDATION RENDERS (CLOSE CHASE CAM & WIDE PANORAMIC)
# ==============================================================================
col_cams = create_collection("COL_Cameras", col_main)

# Lighting Setup (Warm Sunlight + Soft Blue Sky Dome)
sun_data = bpy.data.lights.new(name="Sun_Main", type='SUN')
sun_data.energy = 3.5
sun_data.color = (1.0, 0.95, 0.88)
sun_obj = bpy.data.objects.new("Sun_Light", sun_data)
sun_obj.location = (20.0, -30.0, 40.0)
sun_obj.rotation_euler = (math.radians(48), math.radians(18), math.radians(-35))
col_cams.objects.link(sun_obj)

# Blue sky fill
sky_data = bpy.data.lights.new(name="Sky_Fill", type='SUN')
sky_data.energy = 1.2
sky_data.color = (0.75, 0.88, 1.0)
sky_obj = bpy.data.objects.new("Sky_Light", sky_data)
sky_obj.location = (-20.0, 30.0, 30.0)
sky_obj.rotation_euler = (math.radians(-50), 0, math.radians(145))
col_cams.objects.link(sky_obj)

# World background
if not bpy.context.scene.world:
    bpy.context.scene.world = bpy.data.worlds.new("World")
bpy.context.scene.world.use_nodes = True
bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.70, 0.85, 0.98, 1.0)
    bg_node.inputs["Strength"].default_value = 1.0
# 1. CLOSE CHASE CAM (Bám sát sau đuôi xe, nhìn theo làn đường bên phải, vách núi bên trái, vực sâu & đài vọng cảnh bên phải)
cam_close_data = bpy.data.cameras.new(name="Cam_Chase")
cam_close_data.lens = 32
cam_close_obj = bpy.data.objects.new("Cam_Chase_Obj", cam_close_data)
# Camera 7.5m behind car in right lane, 2.7m above road
cam_pos = car_lane_pos - start_tan * 7.5 + Vector((0, 0, 2.7))
cam_close_obj.location = cam_pos
cam_target = car_lane_pos + start_tan * 5.0 + Vector((0, 0, 0.9))
cam_dir = (cam_target - cam_pos).normalized()
cam_rot_z = math.atan2(cam_dir.y, cam_dir.x) - math.pi/2
cam_rot_x = math.atan2(cam_dir.z, math.sqrt(cam_dir.x**2 + cam_dir.y**2))
cam_close_obj.rotation_euler = (math.pi/2 - cam_rot_x, 0, cam_rot_z)
col_cams.objects.link(cam_close_obj)

# 2. WIDE PANORAMIC CAM (Toàn cảnh đỉnh đèo nhìn trọn vẹn vực sâu, đài vọng cảnh, rừng thông và con đường)
cam_wide_data = bpy.data.cameras.new(name="Cam_Wide")
cam_wide_data.lens = 28
cam_wide_obj = bpy.data.objects.new("Cam_Wide_Obj", cam_wide_data)
cam_wide_obj.location = (18.0, -42.0, 35.0)
wide_target = Vector((15.0, 5.0, 4.0))
w_dir = (wide_target - cam_wide_obj.location).normalized()
w_rot_z = math.atan2(w_dir.y, w_dir.x) - math.pi/2
w_rot_x = math.atan2(w_dir.z, math.sqrt(w_dir.x**2 + w_dir.y**2))
cam_wide_obj.rotation_euler = (math.pi/2 - w_rot_x, 0, w_rot_z)
col_cams.objects.link(cam_wide_obj)

# Render Settings
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.film_transparent = False

# Render Close Chase View
bpy.context.scene.camera = cam_close_obj
bpy.context.scene.render.filepath = "/tmp/preview_real_canyon_close.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_real_canyon_close.png")

# Render Wide Panoramic View
bpy.context.scene.camera = cam_wide_obj
bpy.context.scene.render.filepath = "/tmp/preview_real_canyon_wide.png"
bpy.ops.render.render(write_still=True)
print("Rendered /tmp/preview_real_canyon_wide.png")
