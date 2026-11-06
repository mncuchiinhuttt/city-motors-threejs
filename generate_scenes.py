import bpy
import math

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

def get_materials():
    m = {}
    m["road"] = create_mat("MAT_Road", (0.16, 0.17, 0.20, 1.0), roughness=0.75)
    m["stripe_yellow"] = create_mat("MAT_StripeYellow", (0.98, 0.65, 0.05, 1.0), roughness=0.4)
    m["stripe_white"] = create_mat("MAT_StripeWhite", (0.96, 0.96, 0.98, 1.0), roughness=0.4)
    m["guardrail"] = create_mat("MAT_Guardrail", (0.98, 0.35, 0.05, 1.0), roughness=0.4, metallic=0.5)

    m["mtn_stone"] = create_mat("MAT_MtnStone", (0.55, 0.52, 0.48, 1.0), roughness=0.9)
    m["mtn_cliff"] = create_mat("MAT_MtnCliff", (0.42, 0.38, 0.35, 1.0), roughness=0.9)
    m["mtn_grass"] = create_mat("MAT_MtnGrass", (0.35, 0.48, 0.28, 1.0), roughness=0.85)
    m["mtn_snow"] = create_mat("MAT_MtnSnow", (0.95, 0.96, 0.98, 1.0), roughness=0.5)
    m["trunk"] = create_mat("MAT_Trunk", (0.32, 0.22, 0.15, 1.0), roughness=0.85)
    m["pine"] = create_mat("MAT_Pine", (0.14, 0.36, 0.20, 1.0), roughness=0.85)

    m["city_ground"] = create_mat("MAT_CityGround", (0.92, 0.93, 0.95, 1.0), roughness=0.9)
    m["sidewalk"] = create_mat("MAT_Sidewalk", (0.85, 0.86, 0.88, 1.0), roughness=0.7)
    m["bldg_white"] = create_mat("MAT_BldgWhite", (0.95, 0.95, 0.97, 1.0), roughness=0.5)
    m["bldg_slate"] = create_mat("MAT_BldgSlate", (0.24, 0.30, 0.38, 1.0), roughness=0.4)
    m["bldg_orange"] = create_mat("MAT_BldgOrange", (0.98, 0.38, 0.04, 1.0), roughness=0.5)
    m["bldg_roof"] = create_mat("MAT_BldgRoof", (0.18, 0.20, 0.24, 1.0), roughness=0.9)
    m["window"] = create_mat("MAT_Window", (0.98, 0.88, 0.50, 1.0), roughness=0.15, metallic=0.2,
                             emission_color=(1.0, 0.85, 0.40, 1.0), emission_strength=2.2)
    m["metal"] = create_mat("MAT_Metal", (0.50, 0.52, 0.55, 1.0), roughness=0.3, metallic=0.8)
    m["lamp_glow"] = create_mat("MAT_StreetlampGlow", (1.0, 0.95, 0.8, 1.0), roughness=0.1,
                                emission_color=(1.0, 0.92, 0.70, 1.0), emission_strength=4.5)

    m["car_orange"] = create_mat("MAT_CarOrange", (0.98, 0.38, 0.04, 1.0), roughness=0.2, metallic=0.5)
    m["car_white"] = create_mat("MAT_CarWhite", (0.95, 0.95, 0.97, 1.0), roughness=0.25, metallic=0.2)
    m["car_blue"] = create_mat("MAT_CarBlue", (0.08, 0.45, 0.90, 1.0), roughness=0.2, metallic=0.6)
    m["car_taxi"] = create_mat("MAT_CarTaxi", (0.98, 0.75, 0.04, 1.0), roughness=0.25, metallic=0.3)
    m["car_glass"] = create_mat("MAT_CarGlass", (0.10, 0.15, 0.20, 1.0), roughness=0.1, metallic=0.9)
    m["headlight"] = create_mat("MAT_Headlight", (1.0, 1.0, 0.95, 1.0), roughness=0.1,
                                emission_color=(1.0, 1.0, 0.90, 1.0), emission_strength=5.0)
    m["taillight"] = create_mat("MAT_Taillight", (1.0, 0.05, 0.05, 1.0), roughness=0.1,
                                emission_color=(1.0, 0.05, 0.05, 1.0), emission_strength=4.0)
    m["wheel"] = create_mat("MAT_Wheel", (0.08, 0.08, 0.09, 1.0), roughness=0.8)
    m["rim"] = create_mat("MAT_Rim", (0.80, 0.82, 0.85, 1.0), roughness=0.25, metallic=0.85)
    return m

def add_box(name, size, loc, mat, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
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

def build_car(name, body_mat, m, loc=(0,0,0)):
    root = bpy.data.objects.new(name, None)
    root.location = loc
    bpy.context.scene.collection.objects.link(root)

    lower = add_box(f"{name}_LowerBody", (2.0, 4.2, 0.70), (0, 0, 0.55), body_mat)
    lower.parent = root

    cabin = add_box(f"{name}_Cabin", (1.6, 2.3, 0.65), (0, -0.3, 1.15), m["car_glass"])
    cabin.parent = root

    roof = add_box(f"{name}_RoofCap", (1.52, 2.0, 0.08), (0, -0.3, 1.50), body_mat)
    roof.parent = root

    wheel_coords = [(-1.05, 1.2, 0.38), (1.05, 1.2, 0.38), (-1.05, -1.2, 0.38), (1.05, -1.2, 0.38)]
    for w_idx, (wx, wy, wz) in enumerate(wheel_coords):
        tire = add_cylinder(f"{name}_Wheel_{w_idx}", 0.38, 0.28, (wx, wy, wz), m["wheel"], vertices=12, rot=(0, math.pi/2, 0))
        tire.parent = root
        rx = wx + (0.02 if wx > 0 else -0.02)
        rim = add_cylinder(f"{name}_Rim_{w_idx}", 0.24, 0.30, (rx, wy, wz), m["rim"], vertices=8, rot=(0, math.pi/2, 0))
        rim.parent = root

    hl_l = add_box(f"{name}_HL_L", (0.4, 0.1, 0.2), (-0.75, 2.11, 0.60), m["headlight"])
    hl_r = add_box(f"{name}_HL_R", (0.4, 0.1, 0.2), ( 0.75, 2.11, 0.60), m["headlight"])
    hl_l.parent = root
    hl_r.parent = root

    tl = add_box(f"{name}_TL", (1.7, 0.1, 0.2), (0, -2.11, 0.60), m["taillight"])
    tl.parent = root
    return root

# =========================================================================
# 1. SCENE 1: CITY SCENE
# =========================================================================
print("1. Generating city.glb...")
bpy.ops.wm.read_factory_settings(use_empty=True)
m1 = get_materials()

add_box("City_Ground", (90.0, 90.0, 0.4), (0, 0, -0.2), m1["city_ground"])

add_box("City_Road_S", (54.0, 7.5, 0.1), (0, -16.0, 0.05), m1["road"])
add_box("City_Road_N", (54.0, 7.5, 0.1), (0,  16.0, 0.05), m1["road"])
add_box("City_Road_W", (7.5, 39.5, 0.1), (-20.0, 0, 0.05), m1["road"])
add_box("City_Road_E", (7.5, 39.5, 0.1), ( 20.0, 0, 0.05), m1["road"])
add_box("City_Road_C", (7.5, 39.5, 0.1), (  0.0, 0, 0.05), m1["road"])

for x in range(-22, 23, 4):
    if abs(x) < 4: continue
    add_box(f"City_Stripe_S_{x}", (2.2, 0.28, 0.02), (x, -16.0, 0.11), m1["stripe_yellow"])
    add_box(f"City_Stripe_N_{x}", (2.2, 0.28, 0.02), (x,  16.0, 0.11), m1["stripe_yellow"])
for y in range(-14, 15, 4):
    if abs(y) < 4: continue
    add_box(f"City_Stripe_W_{y}", (0.28, 2.2, 0.02), (-20.0, y, 0.11), m1["stripe_yellow"])
    add_box(f"City_Stripe_E_{y}", (0.28, 2.2, 0.02), ( 20.0, y, 0.11), m1["stripe_yellow"])

def build_city_block(name, loc, size, wall_mat, has_orange=False):
    w, d, h = size
    bx, by, bz = loc
    add_box(f"{name}_Plaza", (w + 2.0, d + 2.0, 0.2), (bx, by, bz + 0.1), m1["sidewalk"])
    add_box(f"{name}_Main", (w, d, h), (bx, by, bz + h/2 + 0.2), wall_mat)
    floors = int(h / 1.3) - 1
    cols = max(1, int(w / 1.3))
    for fl in range(1, floors):
        zp = bz + fl * 1.3 + 0.4
        for c in range(cols):
            xp = bx - w/2 + (c + 0.5) * (w / cols)
            add_box(f"{name}_WN_{fl}_{c}", (0.5, 0.08, 0.5), (xp, by + d/2 + 0.02, zp), m1["window"])
            add_box(f"{name}_WS_{fl}_{c}", (0.5, 0.08, 0.5), (xp, by - d/2 - 0.02, zp), m1["window"])
    roof_mat = m1["bldg_orange"] if has_orange else m1["bldg_roof"]
    add_box(f"{name}_Roof", (w * 0.8, d * 0.8, 1.0), (bx, by, bz + h + 0.7), roof_mat)
    if h > 9.0:
        add_cylinder(f"{name}_Antenna", 0.06, 3.5, (bx, by, bz + h + 2.9), m1["metal"], vertices=6)

build_city_block("CTower_SW", (-10.0, -8.0, 0.0), (5.5, 5.5, 14.0), m1["bldg_slate"], has_orange=True)
build_city_block("CTower_SE", ( 10.0, -8.0, 0.0), (5.5, 5.5, 15.0), m1["bldg_white"])
build_city_block("CTower_NW", (-10.0,  8.0, 0.0), (5.5, 5.5, 12.0), m1["bldg_white"], has_orange=True)
build_city_block("CTower_NE", ( 10.0,  8.0, 0.0), (5.5, 5.5, 13.0), m1["bldg_slate"])

city_lamps = [(-4.2, -4.2), (4.2, -4.2), (-4.2, 4.2), (4.2, 4.2), (-4.2, -18.5), (4.2, -18.5)]
for idx, (lx, ly) in enumerate(city_lamps):
    add_cylinder(f"City_Lamp_{idx}", 0.08, 3.4, (lx, ly, 1.7), m1["metal"], vertices=6)
    add_box(f"City_LampArm_{idx}", (0.1, 0.7, 0.1), (lx, ly + 0.3, 3.35), m1["metal"])
    add_box(f"City_LampBulb_{idx}", (0.22, 0.28, 0.06), (lx, ly + 0.6, 3.25), m1["lamp_glow"])

build_car("Car_BlueCoupe", m1["car_orange"], m1, (0, -16.0, 0.05))
build_car("Car_RedSedan",  m1["car_white"],  m1, (-20.0, 0, 0.05))
build_car("Car_Taxi",      m1["car_taxi"],   m1, (0, 0, 0.05))
build_car("Car_WhiteVan",  m1["car_blue"],   m1, (0, 16.0, 0.05))

city_path = "/home/mncuchiinhuttt/city-threejs/public/assets/city.glb"
bpy.ops.export_scene.gltf(filepath=city_path, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported {city_path}")

# =========================================================================
# 2. SCENE 2: SCENIC MOUNTAIN PASS (Cung Đường Núi Uốn Lượn)
# =========================================================================
print("2. Generating mountain.glb...")
bpy.ops.wm.read_factory_settings(use_empty=True)
m2 = get_materials()

add_box("Mtn_Ground_Base", (110.0, 110.0, 0.4), (0, 0, -0.2), m2["mtn_stone"])

mtn_road_slabs = [
    ((0.0,  -24.0, 0.2), (10.0, 7.5, 0.15), 0.0, 0.0),
    ((10.0, -23.0, 0.6), (10.0, 7.5, 0.15), 0.2, 0.05),
    ((20.0, -19.0, 1.4), (10.0, 7.5, 0.15), 0.4, 0.08),
    ((27.0, -12.0, 2.3), (9.0,  7.5, 0.15), 0.6, 0.10),
    ((30.0,  -3.0, 3.3), (9.0,  7.5, 0.15), 0.3, 0.08),
    ((29.0,   7.0, 4.3), (9.0,  7.5, 0.15), -0.2, 0.08),
    ((24.0,  17.0, 5.0), (9.0,  7.5, 0.15), -0.5, 0.04),
    ((15.0,  24.0, 4.2), (10.0, 7.5, 0.15), -0.7, -0.06),
    ((4.0,   27.0, 3.2), (10.0, 7.5, 0.15), -0.2, -0.08),
    ((-7.0,  25.0, 2.2), (10.0, 7.5, 0.15), 0.2, -0.10),
    ((-17.0, 20.0, 1.2), (10.0, 7.5, 0.15), 0.4, -0.08),
    ((-24.0, 11.0, 0.5), (9.0,  7.5, 0.15), 0.7, -0.05),
    ((-26.0,  0.0, 0.2), (9.0,  7.5, 0.15), 0.0, 0.0),
    ((-24.0, -11.0, 0.2), (9.0, 7.5, 0.15), -0.6, 0.0),
    ((-15.0, -20.0, 0.2), (10.0, 7.5, 0.15), -0.4, 0.0),
    ((0.0,  -24.0, 0.2), (10.0, 7.5, 0.15), 0.0, 0.0)
]

for idx, (loc, sz, rz, ry) in enumerate(mtn_road_slabs):
    add_box(f"Mtn_RoadSlab_{idx}", sz, loc, m2["road"], rot=(0, ry, rz))
    gx = loc[0] + 4.1 * math.cos(rz + math.pi/2)
    gy = loc[1] + 4.1 * math.sin(rz + math.pi/2)
    add_box(f"Mtn_Guard_{idx}", (sz[0], 0.2, 0.65), (gx, gy, loc[2] + 0.4), m2["guardrail"], rot=(0, ry, rz))
    add_box(f"Mtn_Stripe_{idx}", (sz[0]*0.4, 0.28, 0.02), (loc[0], loc[1], loc[2] + 0.1), m2["stripe_yellow"], rot=(0, ry, rz))

mountain_peaks = [
    ("Summit_GrandPeak", 20.0, 28.0, (10.0, 5.0, 0.0), 8),
    ("Summit_EastRidge", 18.0, 24.0, (40.0, 8.0, 0.0), 7),
    ("Summit_NorthPeak", 16.0, 22.0, (2.0, 42.0, 0.0), 7),
    ("Summit_WestRidge", 17.0, 20.0, (-38.0, 6.0, 0.0), 8),
    ("Summit_SouthRidge", 14.0, 16.0, (25.0, -38.0, 0.0), 6),
]
for name, rad, h, loc, verts in mountain_peaks:
    add_cone(f"{name}_Body", rad, h, (loc[0], loc[1], h/2), m2["mtn_cliff"], vertices=verts)
    snow_h = h * 0.32
    add_cone(f"{name}_Snow", rad * 0.36, snow_h, (loc[0], loc[1], h - snow_h/2), m2["mtn_snow"], vertices=verts)

hill_mounds = [
    (14.0, 10.0, (32.0, -15.0, 0.0)),
    (15.0, 11.0, (28.0, 28.0, 0.0)),
    (13.0, 9.0,  (-18.0, 32.0, 0.0)),
    (12.0, 8.0,  (-32.0, -18.0, 0.0)),
    (10.0, 7.0,  (0.0, 18.0, 0.0)),
]
for idx, (rad, h, loc) in enumerate(hill_mounds):
    add_cone(f"Hill_Mound_{idx}", rad, h, (loc[0], loc[1], h/2), m2["mtn_grass"], vertices=7)

pine_trees = [
    (22.0, -30.0, 0.2, 1.4),
    (34.0, -18.0, 1.2, 1.6),
    (36.0,   0.0, 2.5, 1.8),
    (35.0,  15.0, 4.0, 1.7),
    (20.0,  32.0, 3.2, 1.6),
    ( 6.0,  36.0, 2.4, 1.5),
    (-12.0, 32.0, 1.5, 1.4),
    (-30.0, 18.0, 0.6, 1.5),
    (-32.0, -2.0, 0.2, 1.4),
    (-26.0, -22.0, 0.2, 1.3),
    (8.0, -2.0, 3.5, 1.5),
    (12.0, 10.0, 4.2, 1.6),
]
for idx, (px, py, pz, psc) in enumerate(pine_trees):
    add_cylinder(f"Mtn_PineTrunk_{idx}", 0.2*psc, 1.6*psc, (px, py, pz + 0.8*psc), m2["trunk"], vertices=6)
    add_cone(f"Mtn_PineF1_{idx}", 1.5*psc, 1.8*psc, (px, py, pz + 1.8*psc), m2["pine"], vertices=7)
    add_cone(f"Mtn_PineF2_{idx}", 1.1*psc, 1.5*psc, (px, py, pz + 2.7*psc), m2["pine"], vertices=6)
    add_cone(f"Mtn_PineF3_{idx}", 0.7*psc, 1.2*psc, (px, py, pz + 3.5*psc), m2["pine"], vertices=5)

# Mountain Scenic Overlook Platform
add_box("Mtn_Overlook_Deck", (9.0, 6.0, 0.5), (28.0, 20.0, 5.2), m2["mtn_stone"])
add_cylinder("Mtn_Overlook_Lamp", 0.12, 3.0, (28.0, 22.0, 6.7), m2["metal"], vertices=6)
add_cylinder("Mtn_Overlook_Bulb", 0.25, 0.3, (28.0, 22.0, 8.0), m2["lamp_glow"])

build_car("Car_BlueCoupe", m2["car_orange"], m2, (0.0, -24.0, 0.2)) # Hero Orange Sports Car!
build_car("Car_RedSedan",  m2["car_white"],  m2, (27.0, -12.0, 2.3))
build_car("Car_Taxi",      m2["car_taxi"],   m2, (4.0,   27.0, 3.2))
build_car("Car_WhiteVan",  m2["car_blue"],   m2, (-24.0, 11.0, 0.5))

mtn_path = "/home/mncuchiinhuttt/city-threejs/public/assets/mountain.glb"
bpy.ops.export_scene.gltf(filepath=mtn_path, export_format="GLB", export_apply=True, export_yup=True)
print(f"Exported {mtn_path}")
print("Both city.glb and mountain.glb exported cleanly!")
