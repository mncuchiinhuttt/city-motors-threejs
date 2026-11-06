import bpy
import bmesh
import math
from mathutils import Matrix, Vector

def create_mat(name, color, roughness=0.6, metallic=0.0, emission_color=(0,0,0,1), emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

def build_car(name, body_mat, m, loc=(0,0,0)):
    root = bpy.data.objects.new(name, None)
    root.location = loc
    bpy.context.scene.collection.objects.link(root)

    # Chassis
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.52))
    chassis = bpy.context.active_object
    chassis.name = f"{name}_Chassis"
    chassis.scale = (1.9, 4.2, 0.65)
    bpy.ops.object.transform_apply(scale=True)
    chassis.data.materials.append(body_mat)
    chassis.parent = root

    # Cabin
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.25, 1.08))
    cabin = bpy.context.active_object
    cabin.name = f"{name}_Cabin"
    cabin.scale = (1.52, 2.2, 0.58)
    bpy.ops.object.transform_apply(scale=True)
    cabin.data.materials.append(m["car_glass"])
    cabin.parent = root

    # Roof
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.25, 1.40))
    roof = bpy.context.active_object
    roof.name = f"{name}_Roof"
    roof.scale = (1.46, 1.9, 0.08)
    bpy.ops.object.transform_apply(scale=True)
    roof.data.materials.append(body_mat)
    roof.parent = root

    # Spoiler
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.0, 1.05))
    spoiler = bpy.context.active_object
    spoiler.scale = (1.8, 0.35, 0.08)
    bpy.ops.object.transform_apply(scale=True)
    spoiler.data.materials.append(body_mat)
    spoiler.parent = root

    # 4 Wheels
    for w_idx, (wx, wy, wz) in enumerate([(-1.0, 1.2, 0.36), (1.0, 1.2, 0.36), (-1.0, -1.2, 0.36), (1.0, -1.2, 0.36)]):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.36, depth=0.26, location=(wx, wy, wz), rotation=(0, math.pi/2, 0))
        tire = bpy.context.active_object
        tire.data.materials.append(m["wheel"])
        tire.parent = root
        rx = wx + (0.02 if wx > 0 else -0.02)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22, depth=0.28, location=(rx, wy, wz), rotation=(0, math.pi/2, 0))
        rim = bpy.context.active_object
        rim.data.materials.append(m["rim"])
        rim.parent = root

    hl_l = bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.7, 2.11, 0.58))
    hl_l_obj = bpy.context.active_object
    hl_l_obj.scale = (0.38, 0.1, 0.18)
    bpy.ops.object.transform_apply(scale=True)
    hl_l_obj.data.materials.append(m["headlight"])
    hl_l_obj.parent = root

    hl_r = bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.7, 2.11, 0.58))
    hl_r_obj = bpy.context.active_object
    hl_r_obj.scale = (0.38, 0.1, 0.18)
    bpy.ops.object.transform_apply(scale=True)
    hl_r_obj.data.materials.append(m["headlight"])
    hl_r_obj.parent = root

    tl = bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.11, 0.58))
    tl_obj = bpy.context.active_object
    tl_obj.scale = (1.65, 0.1, 0.18)
    bpy.ops.object.transform_apply(scale=True)
    tl_obj.data.materials.append(m["taillight"])
    tl_obj.parent = root
    return root

# =========================================================================
# 1. SCENE 1: DENSE DOWNTOWN SKYSCRAPER CITY (city.glb)
# =========================================================================
print("1. Generating Rich Dense City (city.glb)...")
bpy.ops.wm.read_factory_settings(use_empty=True)

mc = {}
mc["asphalt"]      = create_mat("MAT_Road", (0.16, 0.17, 0.20, 1.0), roughness=0.75)
mc["stripe"]       = create_mat("MAT_StripeYellow", (0.98, 0.65, 0.05, 1.0), roughness=0.4)
mc["stripe_white"] = create_mat("MAT_StripeWhite", (0.96, 0.96, 0.98, 1.0), roughness=0.4)
mc["sidewalk"]     = create_mat("MAT_Sidewalk", (0.86, 0.88, 0.90, 1.0), roughness=0.7)
mc["ground"]       = create_mat("MAT_CityGround", (0.92, 0.93, 0.95, 1.0), roughness=0.9)

mc["bldg_white"]   = create_mat("MAT_BldgWhite", (0.95, 0.95, 0.97, 1.0), roughness=0.5)
mc["bldg_slate"]   = create_mat("MAT_BldgSlate", (0.24, 0.30, 0.38, 1.0), roughness=0.4)
mc["bldg_orange"]  = create_mat("MAT_BldgOrange", (0.98, 0.38, 0.04, 1.0), roughness=0.5)
mc["roof"]         = create_mat("MAT_BldgRoof", (0.18, 0.20, 0.24, 1.0), roughness=0.9)
mc["window"]       = create_mat("MAT_Window", (0.98, 0.88, 0.50, 1.0), roughness=0.15, metallic=0.2,
                                emission_color=(1.0, 0.85, 0.40, 1.0), emission_strength=2.2)

mc["metal"]        = create_mat("MAT_Metal", (0.50, 0.52, 0.55, 1.0), roughness=0.3, metallic=0.8)
mc["lamp_glow"]    = create_mat("MAT_StreetlampGlow", (1.0, 0.95, 0.8, 1.0), roughness=0.1,
                                emission_color=(1.0, 0.92, 0.70, 1.0), emission_strength=4.5)
mc["tree_trunk"]   = create_mat("MAT_Trunk", (0.32, 0.22, 0.15, 1.0), roughness=0.85)
mc["tree_foliage"] = create_mat("MAT_Foliage", (0.20, 0.55, 0.28, 1.0), roughness=0.8)

mc["car_orange"]   = create_mat("MAT_CarOrange", (0.98, 0.38, 0.04, 1.0), roughness=0.2, metallic=0.5)
mc["car_white"]    = create_mat("MAT_CarWhite", (0.95, 0.95, 0.97, 1.0), roughness=0.25, metallic=0.2)
mc["car_blue"]     = create_mat("MAT_CarBlue", (0.08, 0.45, 0.90, 1.0), roughness=0.2, metallic=0.6)
mc["car_taxi"]     = create_mat("MAT_CarTaxi", (0.98, 0.75, 0.04, 1.0), roughness=0.25, metallic=0.3)
mc["car_glass"]    = create_mat("MAT_CarGlass", (0.10, 0.15, 0.20, 1.0), roughness=0.1, metallic=0.9)
mc["headlight"]    = create_mat("MAT_Headlight", (1.0, 1.0, 0.95, 1.0), roughness=0.1,
                                emission_color=(1.0, 1.0, 0.90, 1.0), emission_strength=5.0)
mc["taillight"]    = create_mat("MAT_Taillight", (1.0, 0.05, 0.05, 1.0), roughness=0.1,
                                emission_color=(1.0, 0.05, 0.05, 1.0), emission_strength=4.0)
mc["wheel"]        = create_mat("MAT_Wheel", (0.08, 0.08, 0.09, 1.0), roughness=0.8)
mc["rim"]          = create_mat("MAT_Rim", (0.80, 0.82, 0.85, 1.0), roughness=0.25, metallic=0.85)

def add_box_m(name, size, loc, mat, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    return obj

# Base ground
add_box_m("City_Ground_Base", (120.0, 120.0, 0.4), (0, 0, -0.2), mc["ground"])

# Central Avenue (The main avenue where the car drives): length 80m, width 8m!
add_box_m("Avenue_Central", (8.0, 80.0, 0.1), (0, 0, 0.05), mc["asphalt"])

# Cross streets
add_box_m("Street_South", (80.0, 7.0, 0.1), (0, -20.0, 0.05), mc["asphalt"])
add_box_m("Street_Center", (80.0, 7.0, 0.1), (0,   0.0, 0.05), mc["asphalt"])
add_box_m("Street_North", (80.0, 7.0, 0.1), (0,  20.0, 0.05), mc["asphalt"])

# Sidewalks flanking the central avenue
add_box_m("Sidewalk_Left",  (4.0, 80.0, 0.25), (-6.0, 0, 0.125), mc["sidewalk"])
add_box_m("Sidewalk_Right", (4.0, 80.0, 0.25), ( 6.0, 0, 0.125), mc["sidewalk"])

# Center yellow dashed stripes
for y in range(-36, 37, 4):
    if abs(y) < 3.5 or abs(y - 20) < 3.5 or abs(y + 20) < 3.5: continue
    add_box_m(f"Stripe_C_{y}", (0.3, 2.4, 0.02), (0.0, y, 0.11), mc["stripe"])

# Crosswalks
for iy in [-20.0, 0.0, 20.0]:
    for dx in [-2.5, 2.5]:
        for i in range(-5, 6):
            add_box_m(f"CW_{iy}_{dx}_{i}", (0.35, 1.0, 0.02), (i * 0.55, iy + dx * 1.5, 0.11), mc["stripe_white"])

# ULTRA-FAST SKYSCRAPER CREATION (Using bmesh so 16 skyscrapers generate in 0.2s!):
def build_fast_tower(name, loc, size, wall_mat, has_orange=False):
    w, d, h = size
    bx, by, bz = loc

    # Sidewalk plaza
    add_box_m(f"{name}_Plaza", (w + 1.2, d + 1.2, 0.3), (bx, by, bz + 0.15), mc["sidewalk"])

    # Main tower body
    add_box_m(f"{name}_Tower", (w, d, h), (bx, by, bz + h/2 + 0.3), wall_mat)

    # Roof
    roof_mat = mc["bldg_orange"] if has_orange else mc["roof"]
    add_box_m(f"{name}_Roof", (w * 0.85, d * 0.85, 1.2), (bx, by, bz + h + 0.9), roof_mat)
    if h > 10.0:
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.06, depth=4.0, location=(bx, by, bz + h + 3.0))
        ant = bpy.context.active_object
        ant.data.materials.append(mc["metal"])

    # Windows using a single unified bmesh object!
    bm_win = bmesh.new()
    floors = int(h / 1.4) - 1
    cols = max(1, int(w / 1.4))
    for fl in range(1, floors):
        zp = bz + fl * 1.4 + 0.5
        for c in range(cols):
            xp = bx - w/2 + (c + 0.5) * (w / cols)
            # Front face (+Y)
            p1 = Vector((xp - 0.25, by + d/2 + 0.02, zp - 0.25))
            p2 = Vector((xp + 0.25, by + d/2 + 0.02, zp - 0.25))
            p3 = Vector((xp + 0.25, by + d/2 + 0.02, zp + 0.25))
            p4 = Vector((xp - 0.25, by + d/2 + 0.02, zp + 0.25))
            bm_win.faces.new((bm_win.verts.new(p1), bm_win.verts.new(p2), bm_win.verts.new(p3), bm_win.verts.new(p4)))
            # Back face (-Y)
            q1 = Vector((xp - 0.25, by - d/2 - 0.02, zp - 0.25))
            q2 = Vector((xp + 0.25, by - d/2 - 0.02, zp - 0.25))
            q3 = Vector((xp + 0.25, by - d/2 - 0.02, zp + 0.25))
            q4 = Vector((xp - 0.25, by - d/2 - 0.02, zp + 0.25))
            bm_win.faces.new((bm_win.verts.new(q1), bm_win.verts.new(q4), bm_win.verts.new(q3), bm_win.verts.new(q2)))

    m_w = bpy.data.meshes.new(f"Mesh_{name}_Windows")
    bm_win.to_mesh(m_w)
    bm_win.free()
    o_w = bpy.data.objects.new(f"{name}_Windows", m_w)
    o_w.data.materials.append(mc["window"])
    bpy.context.scene.collection.objects.link(o_w)

# Left Side Skyscraper Row:
build_fast_tower("Tower_L1", (-13.0, -30.0, 0.0), (6.0, 6.0, 16.0), mc["bldg_white"])
build_fast_tower("Tower_L2", (-13.0, -10.0, 0.0), (6.5, 6.5, 20.0), mc["bldg_slate"], has_orange=True)
build_fast_tower("Tower_L3", (-13.0,  10.0, 0.0), (6.0, 6.0, 18.0), mc["bldg_white"], has_orange=True)
build_fast_tower("Tower_L4", (-13.0,  30.0, 0.0), (6.5, 6.5, 22.0), mc["bldg_slate"])

build_fast_tower("Tower_L5", (-22.0, -10.0, 0.0), (5.5, 5.5, 14.0), mc["bldg_white"])
build_fast_tower("Tower_L6", (-22.0,  10.0, 0.0), (5.5, 5.5, 15.0), mc["bldg_slate"])

# Right Side Skyscraper Row:
build_fast_tower("Tower_R1", ( 13.0, -30.0, 0.0), (6.0, 6.0, 15.0), mc["bldg_slate"])
build_fast_tower("Tower_R2", ( 13.0, -10.0, 0.0), (6.5, 6.5, 22.0), mc["bldg_white"], has_orange=True)
build_fast_tower("Tower_R3", ( 13.0,  10.0, 0.0), (6.0, 6.0, 19.0), mc["bldg_slate"], has_orange=True)
build_fast_tower("Tower_R4", ( 13.0,  30.0, 0.0), (6.5, 6.5, 25.0), mc["bldg_white"])

build_fast_tower("Tower_R5", ( 22.0, -10.0, 0.0), (5.5, 5.5, 13.0), mc["bldg_white"])
build_fast_tower("Tower_R6", ( 22.0,  10.0, 0.0), (5.5, 5.5, 16.0), mc["bldg_slate"])

# Terminal Spire directly ahead at Y = 44 (Three.js Z = -44) in front of the car!
build_fast_tower("Terminal_Spire", (0.0, 44.0, 0.0), (8.0, 8.0, 26.0), mc["bldg_slate"], has_orange=True)

# Streetlights lining both sides
for sy in range(-32, 33, 8):
    for sx, arm_x in [(-4.6, 0.5), (4.6, -0.5)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.08, depth=3.4, location=(sx, sy, 1.7))
        p = bpy.context.active_object
        p.data.materials.append(mc["metal"])
        add_box_m(f"Lamp_Arm_{sy}_{sx}", (0.7, 0.1, 0.1), (sx + arm_x*0.35, sy, 3.35), mc["metal"])
        add_box_m(f"Lamp_Bulb_{sy}_{sx}", (0.28, 0.22, 0.06), (sx + arm_x*0.6, sy, 3.25), mc["lamp_glow"])

# Street Trees
for ty in [-26, -14, -6, 6, 14, 26]:
    for tx in [-6.5, 6.5]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.18, depth=1.5, location=(tx, ty, 0.75))
        tr = bpy.context.active_object
        tr.data.materials.append(mc["tree_trunk"])
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=1.2, radius2=0.0, depth=1.6, location=(tx, ty, 1.8))
        f1 = bpy.context.active_object
        f1.data.materials.append(mc["tree_foliage"])
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.9, radius2=0.0, depth=1.4, location=(tx, ty, 2.6))
        f2 = bpy.context.active_object
        f2.data.materials.append(mc["tree_foliage"])

# Cars
build_car("Car_BlueCoupe", mc["car_orange"], mc, (0, -25.0, 0.05)) # Hero Orange Sports Car!
build_car("Car_RedSedan",  mc["car_white"],  mc, (0,  -5.0, 0.05))
build_car("Car_Taxi",      mc["car_taxi"],   mc, (0,  15.0, 0.05))

city_out = "/home/mncuchiinhuttt/city-threejs/public/assets/city.glb"
bpy.ops.export_scene.gltf(filepath=city_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Rich City to {city_out} successfully!")

# =========================================================================
# 2. SCENE 2: MAJESTIC MOUNTAIN TOUGE PASS (mountain.glb)
# =========================================================================
print("2. Generating Majestic Mountain Pass (mountain.glb)...")
bpy.ops.wm.read_factory_settings(use_empty=True)

mm = {}
mm["asphalt"]   = create_mat("MAT_Road", (0.18, 0.19, 0.22, 1.0), roughness=0.8)
mm["stripe"]    = create_mat("MAT_StripeYellow", (0.98, 0.68, 0.05, 1.0), roughness=0.4)
mm["guardrail"] = create_mat("MAT_Guardrail", (0.98, 0.35, 0.05, 1.0), roughness=0.3, metallic=0.5)
mm["post"]      = create_mat("MAT_Post", (0.45, 0.47, 0.50, 1.0), roughness=0.3, metallic=0.8)

mm["valley"]    = create_mat("MAT_Valley", (0.38, 0.50, 0.30, 1.0), roughness=0.9)
mm["cliff"]     = create_mat("MAT_Cliff", (0.48, 0.46, 0.42, 1.0), roughness=0.9)
mm["snow"]      = create_mat("MAT_Snow", (0.96, 0.97, 0.99, 1.0), roughness=0.4)
mm["trunk"]     = create_mat("MAT_Trunk", (0.30, 0.20, 0.14, 1.0), roughness=0.85)
mm["pine"]      = create_mat("MAT_Pine", (0.12, 0.35, 0.18, 1.0), roughness=0.85)

mm["car_orange"]= create_mat("MAT_CarOrange", (0.98, 0.35, 0.04, 1.0), roughness=0.2, metallic=0.5)
mm["car_glass"] = create_mat("MAT_CarGlass", (0.08, 0.12, 0.16, 1.0), roughness=0.1, metallic=0.9)
mm["wheel"]     = create_mat("MAT_Wheel", (0.06, 0.06, 0.07, 1.0), roughness=0.8)
mm["rim"]       = create_mat("MAT_Rim", (0.82, 0.84, 0.86, 1.0), roughness=0.25, metallic=0.85)
mm["headlight"] = create_mat("MAT_Headlight", (1.0, 1.0, 0.95, 1.0), roughness=0.1)
mm["taillight"] = create_mat("MAT_Taillight", (1.0, 0.05, 0.05, 1.0), roughness=0.1)

# Mountain Pass 3D Spline:
ctrl_pts = [
    Vector(( -6.0, -22.0, 0.3)),
    Vector((  8.0, -22.0, 0.6)),
    Vector(( 22.0, -16.0, 1.5)),
    Vector(( 26.0,  -7.0, 2.5)),
    Vector(( 18.0,   2.0, 3.4)),
    Vector(( 24.0,  12.0, 4.4)),
    Vector(( 26.0,  20.0, 5.2)),
    Vector(( 16.0,  26.0, 4.4)),
    Vector((  4.0,  26.0, 3.4)),
    Vector(( -8.0,  22.0, 2.4)),
    Vector((-18.0,  14.0, 1.5)),
    Vector((-24.0,   4.0, 0.8)),
    Vector((-24.0,  -8.0, 0.4)),
    Vector((-16.0, -18.0, 0.3)),
    Vector(( -6.0, -22.0, 0.3))
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

# SHARED QUAD FACES
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

def finalize_mesh_m(name, bm, mat):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    m.polygons.foreach_set("use_smooth", [True] * len(m.polygons))
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)
    return o

finalize_mesh_m("SM_MtnRoad", bm_road, mm["asphalt"])
finalize_mesh_m("SM_MtnStripes", bm_stripes, mm["stripe"])
finalize_mesh_m("SM_MtnGuardrail", bm_guard, mm["guardrail"])
finalize_mesh_m("SM_MtnPosts", bm_posts, mm["post"])

# Mountain Terrain Grid (Cleanly carved 0.35m below road to prevent z-fighting)
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
            z = closest_z - 0.35
        else:
            blend = min(1.0, (min_d - 4.6) / 8.0)
            inner_d = math.hypot(x - 2.0, y - 4.0)
            inner_h = max(0.0, 7.5 - inner_d * 0.35)
            border_d = max(0.0, max(abs(x), abs(y)) - 28.0)
            outer_h = border_d * 0.55
            z = (closest_z - 0.35) * (1.0 - blend) + (inner_h + outer_h) * blend

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
obj_terr.data.materials.append(mm["valley"])
bpy.context.scene.collection.objects.link(obj_terr)

# MOUNTAIN PEAKS EVERYWHERE IN SIGHT:
peaks = [
    # Summit_Ahead: Rising 26m right in front of the car on the S-turn climb!
    ("Summit_Ahead",   15.0, 26.0, ( 14.0,  -8.0, 1.5), 7),
    ("Summit_East",    18.0, 28.0, ( 44.0,  12.0, 0.0), 8),
    ("Summit_North",   17.0, 24.0, (  4.0,  44.0, 0.0), 7),
    ("Summit_West",    16.0, 20.0, (-42.0,  10.0, 0.0), 8),
    ("Summit_South",   15.0, 18.0, ( 25.0, -42.0, 0.0), 6)
]
for name, rad, h, loc, verts in peaks:
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=rad, radius2=0.0, depth=h, location=(loc[0], loc[1], loc[2] + h/2))
    p_body = bpy.context.active_object
    p_body.name = f"{name}_Rock"
    p_body.data.materials.append(mm["cliff"])
    snow_h = h * 0.32
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=rad * 0.35, radius2=0.0, depth=snow_h, location=(loc[0], loc[1], loc[2] + h - snow_h/2))
    p_snow = bpy.context.active_object
    p_snow.name = f"{name}_Snow"
    p_snow.data.materials.append(mm["snow"])

# Pine trees on slopes (> 7.5m from road)
pine_coords = [
    (18.0, -28.0, 0.4), (32.0, -14.0, 1.4), (34.0, 4.0, 2.8), (30.0, 16.0, 3.4),
    (14.0,  30.0, 2.5), (-2.0,  30.0, 1.8), (-16.0, 26.0, 1.0), (-30.0, 14.0, 0.4),
    (-30.0, -4.0, 0.2), (-20.0, -22.0, 0.2), (2.0, -2.0, 4.8), (6.0, 8.0, 5.2)
]
for idx, (px, py, pz) in enumerate(pine_coords):
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.2, depth=1.5, location=(px, py, pz + 0.75))
    t = bpy.context.active_object
    t.data.materials.append(mm["trunk"])
    for tier in range(3):
        r_tier = 1.3 - tier * 0.32
        h_tier = 1.6 - tier * 0.15
        z_tier = pz + 1.6 + tier * 0.9
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=r_tier, radius2=0.0, depth=h_tier, location=(px, py, z_tier))
        f = bpy.context.active_object
        f.data.materials.append(mm["pine"])

build_car("Car_BlueCoupe", mm["car_orange"], mm, (spline_samples[0].x, spline_samples[0].y, spline_samples[0].z + 0.03))

mtn_out = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(filepath=mtn_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Mountain Pass to {mtn_out}")

print("All scenes generated successfully!")
