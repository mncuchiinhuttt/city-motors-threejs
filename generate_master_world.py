import bpy
import bmesh
import math
from mathutils import Vector

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

# Hero Car: Front at +Y, Rear at -Y
def build_car(name, body_mat, m, loc=(0,0,0)):
    root = bpy.data.objects.new(name, None)
    root.location = loc
    bpy.context.scene.collection.objects.link(root)

    # Chassis
    lower = add_box(f"{name}_LowerBody", (1.9, 4.2, 0.65), (0, 0, 0.52), body_mat)
    lower.parent = root

    # Cabin
    cabin = add_box(f"{name}_Cabin", (1.52, 2.2, 0.58), (0, -0.25, 1.08), m["car_glass"])
    cabin.parent = root

    # Roof
    roof = add_box(f"{name}_RoofCap", (1.46, 1.9, 0.08), (0, -0.25, 1.40), body_mat)
    roof.parent = root

    # Rear Sport Spoiler (At -Y rear!)
    spoiler = add_box(f"{name}_Spoiler", (1.8, 0.35, 0.08), (0, -2.0, 1.05), body_mat)
    spoiler.parent = root

    # 4 Wheels
    wheel_coords = [(-1.0, 1.2, 0.36), (1.0, 1.2, 0.36), (-1.0, -1.2, 0.36), (1.0, -1.2, 0.36)]
    for w_idx, (wx, wy, wz) in enumerate(wheel_coords):
        tire = add_cylinder(f"{name}_Wheel_{w_idx}", 0.36, 0.26, (wx, wy, wz), m["wheel"], vertices=12, rot=(0, math.pi/2, 0))
        tire.parent = root
        rx = wx + (0.02 if wx > 0 else -0.02)
        rim = add_cylinder(f"{name}_Rim_{w_idx}", 0.22, 0.28, (rx, wy, wz), m["rim"], vertices=8, rot=(0, math.pi/2, 0))
        rim.parent = root

    # FRONT HEADLIGHTS (At +Y front!)
    hl_l = add_box(f"{name}_HL_L", (0.38, 0.1, 0.18), (-0.7, 2.11, 0.58), m["headlight"])
    hl_r = add_box(f"{name}_HL_R", (0.38, 0.1, 0.18), ( 0.7, 2.11, 0.58), m["headlight"])
    hl_l.parent = root
    hl_r.parent = root

    # REAR TAILLIGHT BAR (At -Y rear!)
    tl = add_box(f"{name}_TL", (1.65, 0.1, 0.18), (0, -2.11, 0.58), m["taillight"])
    tl.parent = root
    return root

# =========================================================================
# 1. SCENE 1: DENSE SKYSCRAPER CANYON (city.glb)
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

add_box("City_Ground_Base", (120.0, 120.0, 0.4), (0, 0, -0.2), mc["ground"])
add_box("Avenue_Central", (8.0, 80.0, 0.1), (0, 0, 0.05), mc["asphalt"])

add_box("Street_South", (80.0, 7.0, 0.1), (0, -20.0, 0.05), mc["asphalt"])
add_box("Street_Center", (80.0, 7.0, 0.1), (0,   0.0, 0.05), mc["asphalt"])
add_box("Street_North", (80.0, 7.0, 0.1), (0,  20.0, 0.05), mc["asphalt"])

add_box("Sidewalk_Left",  (4.0, 80.0, 0.25), (-6.0, 0, 0.125), mc["sidewalk"])
add_box("Sidewalk_Right", (4.0, 80.0, 0.25), ( 6.0, 0, 0.125), mc["sidewalk"])

for y in range(-36, 37, 4):
    if abs(y) < 3.5 or abs(y - 20) < 3.5 or abs(y + 20) < 3.5: continue
    add_box(f"Stripe_C_{y}", (0.3, 2.4, 0.02), (0.0, y, 0.11), mc["stripe"])

for iy in [-20.0, 0.0, 20.0]:
    for dx in [-2.5, 2.5]:
        for i in range(-5, 6):
            add_box(f"CW_{iy}_{dx}_{i}", (0.35, 1.0, 0.02), (i * 0.55, iy + dx * 1.5, 0.11), mc["stripe_white"])

def build_fast_tower(name, loc, size, wall_mat, has_orange=False):
    w, d, h = size
    bx, by, bz = loc
    add_box(f"{name}_Plaza", (w + 1.2, d + 1.2, 0.3), (bx, by, bz + 0.15), mc["sidewalk"])
    add_box(f"{name}_Tower", (w, d, h), (bx, by, bz + h/2 + 0.3), wall_mat)
    roof_mat = mc["bldg_orange"] if has_orange else mc["roof"]
    add_box(f"{name}_Roof", (w * 0.85, d * 0.85, 1.2), (bx, by, bz + h + 0.9), roof_mat)
    if h > 10.0:
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.06, depth=4.0, location=(bx, by, bz + h + 3.0))
        ant = bpy.context.active_object
        ant.data.materials.append(mc["metal"])

    bm_win = bmesh.new()
    floors = int(h / 1.4) - 1
    cols = max(1, int(w / 1.4))
    for fl in range(1, floors):
        zp = bz + fl * 1.4 + 0.5
        for c in range(cols):
            xp = bx - w/2 + (c + 0.5) * (w / cols)
            p1 = Vector((xp - 0.25, by + d/2 + 0.02, zp - 0.25))
            p2 = Vector((xp + 0.25, by + d/2 + 0.02, zp - 0.25))
            p3 = Vector((xp + 0.25, by + d/2 + 0.02, zp + 0.25))
            p4 = Vector((xp - 0.25, by + d/2 + 0.02, zp + 0.25))
            bm_win.faces.new((bm_win.verts.new(p1), bm_win.verts.new(p2), bm_win.verts.new(p3), bm_win.verts.new(p4)))
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

# 16 Skyscraper Towers in canyon formation:
build_fast_tower("Tower_L1", (-13.0, -30.0, 0.0), (6.0, 6.0, 16.0), mc["bldg_white"])
build_fast_tower("Tower_L2", (-13.0, -10.0, 0.0), (6.5, 6.5, 20.0), mc["bldg_slate"], has_orange=True)
build_fast_tower("Tower_L3", (-13.0,  10.0, 0.0), (6.0, 6.0, 18.0), mc["bldg_white"], has_orange=True)
build_fast_tower("Tower_L4", (-13.0,  30.0, 0.0), (6.5, 6.5, 22.0), mc["bldg_slate"])
build_fast_tower("Tower_L5", (-22.0, -10.0, 0.0), (5.5, 5.5, 14.0), mc["bldg_white"])
build_fast_tower("Tower_L6", (-22.0,  10.0, 0.0), (5.5, 5.5, 15.0), mc["bldg_slate"])

build_fast_tower("Tower_R1", ( 13.0, -30.0, 0.0), (6.0, 6.0, 15.0), mc["bldg_slate"])
build_fast_tower("Tower_R2", ( 13.0, -10.0, 0.0), (6.5, 6.5, 22.0), mc["bldg_white"], has_orange=True)
build_fast_tower("Tower_R3", ( 13.0,  10.0, 0.0), (6.0, 6.0, 19.0), mc["bldg_slate"], has_orange=True)
build_fast_tower("Tower_R4", ( 13.0,  30.0, 0.0), (6.5, 6.5, 25.0), mc["bldg_white"])
build_fast_tower("Tower_R5", ( 22.0, -10.0, 0.0), (5.5, 5.5, 13.0), mc["bldg_white"])
build_fast_tower("Tower_R6", ( 22.0,  10.0, 0.0), (5.5, 5.5, 16.0), mc["bldg_slate"])

build_fast_tower("Terminal_Spire", (0.0, 44.0, 0.0), (8.0, 8.0, 26.0), mc["bldg_slate"], has_orange=True)

for sy in range(-32, 33, 8):
    for sx, arm_x in [(-4.6, 0.5), (4.6, -0.5)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.08, depth=3.4, location=(sx, sy, 1.7))
        p = bpy.context.active_object
        p.data.materials.append(mc["metal"])
        add_box(f"Lamp_Arm_{sy}_{sx}", (0.7, 0.1, 0.1), (sx + arm_x*0.35, sy, 3.35), mc["metal"])
        add_box(f"Lamp_Bulb_{sy}_{sx}", (0.28, 0.22, 0.06), (sx + arm_x*0.6, sy, 3.25), mc["lamp_glow"])

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

build_car("Car_BlueCoupe", mc["car_orange"], mc, (0, -25.0, 0.05)) # Hero Orange Car!
build_car("Car_RedSedan",  mc["car_white"],  mc, (0,  -5.0, 0.05))
build_car("Car_Taxi",      mc["car_taxi"],   mc, (0,  15.0, 0.05))

city_out = "/home/mncuchiinhuttt/city-threejs/public/assets/city.glb"
bpy.ops.export_scene.gltf(filepath=city_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Rich City to {city_out}")

# =========================================================================
# 2. SCENE 2: SCENIC MOUNTAIN PASS WITH CONTINUOUS LEFT CLIFF WALL (mountain.glb)
# =========================================================================
print("2. Generating Mountain Pass with Left Cliff Wall (mountain.glb)...")
bpy.ops.wm.read_factory_settings(use_empty=True)

mm = {}
mm["asphalt"]   = create_mat("MAT_Road", (0.18, 0.19, 0.22, 1.0), roughness=0.8)
mm["stripe"]    = create_mat("MAT_StripeYellow", (0.98, 0.68, 0.05, 1.0), roughness=0.4)
mm["guardrail"] = create_mat("MAT_Guardrail", (0.98, 0.35, 0.05, 1.0), roughness=0.3, metallic=0.5)
mm["post"]      = create_mat("MAT_Post", (0.45, 0.47, 0.50, 1.0), roughness=0.3, metallic=0.8)

mm["valley"]    = create_mat("MAT_Valley", (0.40, 0.52, 0.32, 1.0), roughness=0.9)
mm["cliff"]     = create_mat("MAT_Cliff",  (0.46, 0.44, 0.40, 1.0), roughness=0.88)
mm["snow"]      = create_mat("MAT_Snow",   (0.96, 0.97, 0.99, 1.0), roughness=0.4)
mm["trunk"]     = create_mat("MAT_Trunk",  (0.30, 0.20, 0.14, 1.0), roughness=0.85)
mm["pine"]      = create_mat("MAT_Pine",   (0.12, 0.35, 0.18, 1.0), roughness=0.85)

mm["car_orange"]= create_mat("MAT_CarOrange", (0.98, 0.35, 0.04, 1.0), roughness=0.2, metallic=0.5)
mm["car_glass"] = create_mat("MAT_CarGlass", (0.08, 0.12, 0.16, 1.0), roughness=0.1, metallic=0.9)
mm["wheel"]     = create_mat("MAT_Wheel",    (0.06, 0.06, 0.07, 1.0), roughness=0.8)
mm["rim"]       = create_mat("MAT_Rim",      (0.82, 0.84, 0.86, 1.0), roughness=0.25, metallic=0.85)
mm["headlight"] = create_mat("MAT_Headlight",(1.0, 1.0, 0.95, 1.0), roughness=0.1)
mm["taillight"] = create_mat("MAT_Taillight",(1.0, 0.05, 0.05, 1.0), roughness=0.1)

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
bm_left_cliff = bmesh.new() # CONTINUOUS ROCK CLIFF WALL HUGGING LEFT SIDE!

up = Vector((0, 0, 1))
ring_al = []
ring_ar = []
ring_cl = []
ring_cr = []
ring_gb = []
ring_gt = []

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

    # Right Guardrail
    p_gb = p_cr + right * 0.12 + Vector((0, 0, 0.38))
    p_gt = p_cr + right * 0.12 + Vector((0, 0, 0.70))
    ring_gb.append(bm_guard.verts.new(p_gb))
    ring_gt.append(bm_guard.verts.new(p_gt))

    # CONTINUOUS MOUNTAIN ROCK CLIFF WALL HUGGING THE ENTIRE LEFT SIDE OF ROAD!
    p_c_foot = curr - right * 4.6 + Vector((0, 0, 0.85))
    p_c_mid  = curr - right * (6.5 + math.sin(i * 0.3)*0.6) + Vector((0, 0, 4.2 + math.cos(i * 0.2)*0.8))
    p_c_top  = curr - right * (9.0 + math.cos(i * 0.2)*0.8) + Vector((0, 0, 8.5 + math.sin(i * 0.3)*1.2))
    p_c_peak = curr - right * 13.5 + Vector((0, 0, 14.5 + math.cos(i * 0.4)*2.0))

    ring_cliff_foot.append(bm_left_cliff.verts.new(p_c_foot))
    ring_cliff_mid.append(bm_left_cliff.verts.new(p_c_mid))
    ring_cliff_top.append(bm_left_cliff.verts.new(p_c_top))
    ring_cliff_peak.append(bm_left_cliff.verts.new(p_c_peak))

for i in range(num_pts):
    next_i = (i + 1) % num_pts
    bm_road.faces.new((ring_al[i], ring_ar[i], ring_ar[next_i], ring_al[next_i]))
    bm_road.faces.new((ring_cl[i], ring_al[i], ring_al[next_i], ring_cl[next_i]))
    bm_road.faces.new((ring_ar[i], ring_cr[i], ring_cr[next_i], ring_ar[next_i]))
    bm_guard.faces.new((ring_gb[i], ring_gt[i], ring_gt[next_i], ring_gb[next_i]))

    # LEFT MOUNTAIN CLIFF WALL STRIPS:
    bm_left_cliff.faces.new((ring_cliff_foot[i], ring_cliff_mid[i], ring_cliff_mid[next_i], ring_cliff_foot[next_i]))
    bm_left_cliff.faces.new((ring_cliff_mid[i], ring_cliff_top[i], ring_cliff_top[next_i], ring_cliff_mid[next_i]))
    bm_left_cliff.faces.new((ring_cliff_top[i], ring_cliff_peak[i], ring_cliff_peak[next_i], ring_cliff_top[next_i]))

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

def finalize_mesh_m(name, bm, mat, smooth=True):
    m = bpy.data.meshes.new(f"Mesh_{name}")
    bm.to_mesh(m)
    bm.free()
    m.polygons.foreach_set("use_smooth", [smooth] * len(m.polygons))
    o = bpy.data.objects.new(name, m)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)
    return o

finalize_mesh_m("SM_MtnRoad", bm_road, mm["asphalt"], smooth=True)
finalize_mesh_m("SM_MtnStripes", bm_stripes, mm["stripe"], smooth=True)
finalize_mesh_m("SM_MtnGuardrail", bm_guard, mm["guardrail"], smooth=True)
finalize_mesh_m("SM_MtnPosts", bm_posts, mm["post"], smooth=False)
finalize_mesh_m("SM_LeftCliffWall", bm_left_cliff, mm["cliff"], smooth=False)

# Valley Base Terrain
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
        z = math.sin(x*0.06)*math.cos(y*0.06)*2.0 - 0.5
        row.append(bm_terr.verts.new(Vector((x, y, max(-0.2, z)))))
    grid_v.append(row)

for iy in range(grid_res - 1):
    for ix in range(grid_res - 1):
        bm_terr.faces.new((grid_v[iy][ix], grid_v[iy][ix+1], grid_v[iy+1][ix+1], grid_v[iy+1][ix]))

finalize_mesh_m("SM_ValleyBase", bm_terr, mm["valley"], smooth=False)

# Background Snow-capped Mountain Summits
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

# Pine trees on left cliff ridge!
for i in range(12, num_pts, 10):
    curr = mtn_samples[i]
    r = rights[i]
    px = curr.x - r.x * 8.0
    py = curr.y - r.y * 8.0
    pz = curr.z + 5.5
    add_cylinder(f"Cliff_PineTrunk_{i}", 0.2, 1.6, (px, py, pz + 0.8), mm["trunk"], vertices=6)
    for tier in range(3):
        r_tier = 1.3 - tier * 0.32
        h_tier = 1.6 - tier * 0.15
        z_tier = pz + 1.6 + tier * 0.9
        add_cone(f"Cliff_PineF_{i}_{tier}", r_tier, h_tier, (px, py, z_tier), mm["pine"], vertices=6)

# Hero Car: Car_BlueCoupe
build_car("Car_BlueCoupe", mm["car_orange"], mm, (mtn_samples[0].x, mtn_samples[0].y, mtn_samples[0].z + 0.04))

mtn_out = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(filepath=mtn_out, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported Mountain to {mtn_out}")

print("Master World Generation Complete!")
