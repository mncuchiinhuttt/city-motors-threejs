import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

def create_mat(name, color, roughness=0.5, metallic=0.0, emission_color=(0,0,0,1), emission_strength=0.0):
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

# --- 60 / 30 / 10 SOLID COLOR PALETTE ---
# 60% Dominant: Clean warm porcelain terrain & sidewalks
mat_ground = create_mat("MAT_Ground", (0.94, 0.95, 0.96, 1.0), roughness=0.9)
mat_sidewalk = create_mat("MAT_Sidewalk", (0.88, 0.90, 0.92, 1.0), roughness=0.7)

# 30% Secondary: Deep solid slate/charcoal for roads & architectural contrasts
mat_road = create_mat("MAT_Road", (0.16, 0.17, 0.20, 1.0), roughness=0.75)
mat_stripe_white = create_mat("MAT_StripeWhite", (0.96, 0.96, 0.98, 1.0), roughness=0.4)
mat_stripe_yellow = create_mat("MAT_StripeYellow", (0.98, 0.65, 0.05, 1.0), roughness=0.4)
mat_bldg_slate = create_mat("MAT_BldgSlate", (0.24, 0.30, 0.38, 1.0), roughness=0.4)
mat_bldg_white = create_mat("MAT_BldgWhite", (0.96, 0.96, 0.97, 1.0), roughness=0.5)
mat_bldg_roof = create_mat("MAT_BldgRoof", (0.18, 0.20, 0.24, 1.0), roughness=0.9)
mat_mountain_rock = create_mat("MAT_MountainRock", (0.45, 0.44, 0.42, 1.0), roughness=0.9)
mat_mountain_snow = create_mat("MAT_MountainSnow", (0.96, 0.97, 0.98, 1.0), roughness=0.5)

# 10% Accent: Solid Warm Sunset Orange (Focal Point!)
mat_accent_orange = create_mat("MAT_AccentOrange", (0.98, 0.38, 0.04, 1.0), roughness=0.3, metallic=0.4)
mat_guardrail = create_mat("MAT_Guardrail", (0.95, 0.35, 0.05, 1.0), roughness=0.4, metallic=0.5)
mat_neon_orange = create_mat("MAT_NeonOrange", (1.0, 0.45, 0.0, 1.0), roughness=0.2,
                             emission_color=(1.0, 0.45, 0.0, 1.0), emission_strength=3.5)

# Window glow for night / reflective for day
mat_window = create_mat("MAT_Window", (0.98, 0.88, 0.50, 1.0), roughness=0.15, metallic=0.2,
                        emission_color=(1.0, 0.85, 0.40, 1.0), emission_strength=2.2)

# Cars
mat_car_orange = create_mat("MAT_CarOrange", (0.98, 0.38, 0.04, 1.0), roughness=0.2, metallic=0.5) # Hero Sports Car!
mat_car_white = create_mat("MAT_CarWhite", (0.95, 0.95, 0.97, 1.0), roughness=0.25, metallic=0.2)
mat_car_blue = create_mat("MAT_CarBlue", (0.08, 0.45, 0.90, 1.0), roughness=0.2, metallic=0.6)
mat_car_taxi = create_mat("MAT_CarTaxi", (0.98, 0.75, 0.04, 1.0), roughness=0.25, metallic=0.3)
mat_car_glass = create_mat("MAT_CarGlass", (0.10, 0.15, 0.20, 1.0), roughness=0.1, metallic=0.9)
mat_headlight = create_mat("MAT_Headlight", (1.0, 1.0, 0.95, 1.0), roughness=0.1,
                           emission_color=(1.0, 1.0, 0.90, 1.0), emission_strength=5.0)
mat_taillight = create_mat("MAT_Taillight", (1.0, 0.05, 0.05, 1.0), roughness=0.1,
                           emission_color=(1.0, 0.05, 0.05, 1.0), emission_strength=4.0)
mat_wheel = create_mat("MAT_Wheel", (0.08, 0.08, 0.09, 1.0), roughness=0.8)
mat_rim = create_mat("MAT_Rim", (0.80, 0.82, 0.85, 1.0), roughness=0.25, metallic=0.85)

# Props
mat_trunk = create_mat("MAT_Trunk", (0.35, 0.24, 0.16, 1.0), roughness=0.85)
mat_pine = create_mat("MAT_Pine", (0.14, 0.42, 0.22, 1.0), roughness=0.85)
mat_metal = create_mat("MAT_Metal", (0.50, 0.52, 0.55, 1.0), roughness=0.3, metallic=0.8)
mat_lamp_glow = create_mat("MAT_StreetlampGlow", (1.0, 0.95, 0.8, 1.0), roughness=0.1,
                           emission_color=(1.0, 0.92, 0.70, 1.0), emission_strength=4.5)

# Collections
def get_col(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

col_roads = get_col("COL_Roads")
col_buildings = get_col("COL_Buildings")
col_mountains = get_col("COL_Mountains")
col_props = get_col("COL_Props")
col_vehicles = get_col("COL_Vehicles")

def link_to_col(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)

def add_box(name, size, loc, mat, col=col_props, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj

def add_cylinder(name, radius, depth, loc, mat, vertices=12, rot=(0,0,0), col=col_props):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj

def add_cone(name, radius, depth, loc, mat, vertices=8, rot=(0,0,0), col=col_props):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=0.0, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj

print("1. Building Clean Foreground Highway & Background Skyline...")

# Ground Terrain (Warm porcelain white)
add_box("Ground_Base", (120.0, 120.0, 0.4), (0, 0, -0.2), mat_ground, col_roads)

# ROAD NETWORK:
# The road is 8.0 meters wide with bright solid markings.
# Road layout in Blender (X, Y, Z):
# Note: Blender exports (X, Y, Z) -> Three.js (X, Z, -Y) with export_yup=True!
# South Boulevard (Foreground): Y = -16.0 (Three.js Z = 16.0)
add_box("Road_South", (56.0, 8.0, 0.1), (0, -16.0, 0.05), mat_road, col_roads)
# North Boulevard (Midground): Y = 16.0 (Three.js Z = -16.0)
add_box("Road_North", (56.0, 8.0, 0.1), (0, 16.0, 0.05), mat_road, col_roads)
# West Avenue: X = -22.0
add_box("Road_West", (8.0, 40.0, 0.1), (-22.0, 0, 0.05), mat_road, col_roads)
# Central Crossing: X = 0
add_box("Road_Center", (8.0, 40.0, 0.1), (0, 0, 0.05), mat_road, col_roads)

# Mountain Pass Road Slabs (East Side, climbing from Y=-16 to Y=16 at X=22..28, Z=0.4..3.5m)
mountain_steps = [
    ((22.0, -14.0, 0.4), (8.0, 5.0, 0.15), 0.06),
    ((24.5, -9.0, 1.1),  (8.0, 6.0, 0.15), 0.12),
    ((26.5, -3.0, 2.0),  (8.0, 6.5, 0.15), 0.10),
    ((27.5, 3.0, 2.8),   (8.0, 6.5, 0.15), 0.08),
    ((27.0, 9.0, 3.4),   (8.0, 6.5, 0.15), 0.04), # Overlook summit!
    ((24.5, 14.0, 1.9),  (8.0, 6.0, 0.15), -0.15),
    ((22.0, 16.0, 0.6),  (8.0, 5.0, 0.15), -0.08),
]
for idx, (loc, sz, r_pitch) in enumerate(mountain_steps):
    add_box(f"Mtn_Road_{idx}", sz, loc, mat_road, col_roads, rot=(0, r_pitch, 0))
    # Outer guardrails
    add_box(f"Guardrail_{idx}", (0.25, sz[1], 0.65), (loc[0] + 4.1, loc[1], loc[2] + 0.4), mat_guardrail, col_props)

# Solid Yellow Center Road Stripes (High visibility!)
for x in range(-24, 25, 4):
    if abs(x) < 4: continue
    add_box(f"Stripe_S_{x}", (2.4, 0.3, 0.02), (x, -16.0, 0.11), mat_stripe_yellow, col_roads)
    add_box(f"Stripe_N_{x}", (2.4, 0.3, 0.02), (x, 16.0, 0.11), mat_stripe_yellow, col_roads)
for y in range(-14, 15, 4):
    if abs(y) < 4: continue
    add_box(f"Stripe_W_{y}", (0.3, 2.4, 0.02), (-22.0, y, 0.11), mat_stripe_yellow, col_roads)
    add_box(f"Stripe_C_{y}", (0.3, 2.4, 0.02), (0.0, y, 0.11), mat_stripe_yellow, col_roads)

# 2. MOUNTAIN PEAKS & SCENIC SLOPES (Set far East at X >= 36)
print("2. Generating Mountain Mass...")
peaks = [
    ("Peak_A", 18.0, 24.0, (44.0, 8.0, 0)),
    ("Peak_B", 16.0, 20.0, (46.0, -12.0, 0)),
    ("Peak_C", 16.0, 21.0, (38.0, 26.0, 0)),
    ("Peak_D", 14.0, 16.0, (42.0, -24.0, 0)),
]
for name, rad, h, loc in peaks:
    add_cone(f"{name}_Rock", rad, h, (loc[0], loc[1], h/2), mat_mountain_rock, vertices=7, col=col_mountains)
    snow_h = h * 0.3
    add_cone(f"{name}_Snow", rad * 0.35, snow_h, (loc[0], loc[1], h - snow_h/2), mat_mountain_snow, vertices=7, col=col_mountains)

add_box("Mtn_Slope_Base", (28.0, 60.0, 1.8), (36.0, 2.0, 0.6), mat_mountain_rock, col=col_mountains)

# 3. BACKGROUND SKYLINE (BUILDINGS PLACED IN THE BACKGROUND AT Y > 0)
# This guarantees that looking at the road, the buildings are in the BACKGROUND, NEVER blocking the car!
print("3. Building Skyline...")
def build_tower(name, loc, size, wall_mat, has_orange_accent=False):
    w, d, h = size
    bx, by, bz = loc
    add_box(f"{name}_Plaza", (w + 2.0, d + 2.0, 0.25), (bx, by, bz + 0.12), mat_sidewalk, col_buildings)
    add_box(f"{name}_Main", (w, d, h), (bx, by, bz + h/2 + 0.25), wall_mat, col_buildings)

    # Windows on facade
    floors = int(h / 1.3) - 1
    cols_x = max(1, int(w / 1.3))
    for fl in range(1, floors):
        zp = bz + fl * 1.3 + 0.5
        for cx in range(cols_x):
            xp = bx - w/2 + (cx + 0.5) * (w / cols_x)
            add_box(f"{name}_W_{fl}_{cx}", (0.5, 0.08, 0.5), (xp, by - d/2 - 0.02, zp), mat_window, col_buildings)

    # Roof & Accent
    roof_mat = mat_accent_orange if has_orange_accent else mat_bldg_roof
    add_box(f"{name}_Roof", (w * 0.8, d * 0.8, 1.0), (bx, by, bz + h + 0.75), roof_mat, col_buildings)
    if h > 9.0:
        add_cylinder(f"{name}_Antenna", 0.06, 3.5, (bx, by, bz + h + 3.0), mat_metal, vertices=6, col=col_buildings)

# Background Towers (Y in [4, 12] and [20, 28])
build_tower("Skyline_Tower_1", (-10.0, 8.0, 0.0), (6.0, 6.0, 16.0), mat_bldg_slate, has_orange_accent=True)
build_tower("Skyline_Tower_2", (-17.0, 8.0, 0.0), (5.0, 5.0, 11.0), mat_bldg_white)
build_tower("Skyline_Tower_3", ( 10.0, 8.0, 0.0), (6.0, 6.0, 18.0), mat_bldg_white, has_orange_accent=True)
build_tower("Skyline_Tower_4", ( 17.0, 8.0, 0.0), (5.0, 5.0, 12.0), mat_bldg_slate)

# 4. TREES (Placed in plazas safely away from the road lanes)
print("4. Adding Trees...")
safe_trees = [
    (-10.0, 0.0, 0.2, 1.2),
    ( 10.0, 0.0, 0.2, 1.2),
    (-10.0, -8.0, 0.2, 1.1),
    ( 10.0, -8.0, 0.2, 1.1),
    ( 36.0, -14.0, 1.2, 1.5),
    ( 38.0, 4.0, 3.8, 1.7),
    ( 36.0, 18.0, 2.5, 1.5),
]
for idx, (tx, ty, tz, tsc) in enumerate(safe_trees):
    add_cylinder(f"Tree_Trunk_{idx}", 0.2 * tsc, 1.6 * tsc, (tx, ty, tz + 0.8 * tsc), mat_trunk, vertices=6, col=col_props)
    add_cone(f"Tree_F1_{idx}", 1.4 * tsc, 1.8 * tsc, (tx, ty, tz + 1.8 * tsc), mat_pine, vertices=7, col=col_props)
    add_cone(f"Tree_F2_{idx}", 1.0 * tsc, 1.5 * tsc, (tx, ty, tz + 2.7 * tsc), mat_pine, vertices=6, col=col_props)

# 5. HIGH-VISIBILITY HERO SPORTS CARS
print("5. Crafting Hero Cars...")
def build_car(name, body_mat, loc=(0,0,0)):
    root = bpy.data.objects.new(name, None)
    root.location = loc
    col_vehicles.objects.link(root)

    # Aerodynamic sports chassis
    lower = add_box(f"{name}_LowerBody", (2.0, 4.2, 0.70), (0, 0, 0.55), body_mat, col=col_vehicles)
    lower.parent = root

    # Greenhouse cabin (glossy dark tinted glass)
    cabin = add_box(f"{name}_Cabin", (1.6, 2.3, 0.65), (0, -0.3, 1.15), mat_car_glass, col=col_vehicles)
    cabin.parent = root

    # Roof Cap
    roof = add_box(f"{name}_RoofCap", (1.52, 2.0, 0.08), (0, -0.3, 1.50), body_mat, col=col_vehicles)
    roof.parent = root

    # 4 Sport Alloy Wheels
    wheel_coords = [(-1.05, 1.2, 0.38), (1.05, 1.2, 0.38), (-1.05, -1.2, 0.38), (1.05, -1.2, 0.38)]
    for w_idx, (wx, wy, wz) in enumerate(wheel_coords):
        tire = add_cylinder(f"{name}_Wheel_{w_idx}", 0.38, 0.28, (wx, wy, wz), mat_wheel, vertices=12, rot=(0, math.pi/2, 0), col=col_vehicles)
        tire.parent = root
        rx = wx + (0.02 if wx > 0 else -0.02)
        rim = add_cylinder(f"{name}_Rim_{w_idx}", 0.24, 0.30, (rx, wy, wz), mat_rim, vertices=8, rot=(0, math.pi/2, 0), col=col_vehicles)
        rim.parent = root

    # Bright Front LED Headlights (Front is +Y)
    hl_l = add_box(f"{name}_HL_L", (0.4, 0.1, 0.2), (-0.75, 2.11, 0.60), mat_headlight, col=col_vehicles)
    hl_r = add_box(f"{name}_HL_R", (0.4, 0.1, 0.2), ( 0.75, 2.11, 0.60), mat_headlight, col=col_vehicles)
    hl_l.parent = root
    hl_r.parent = root

    # Bright Red Taillights Bar (Rear is -Y)
    tl = add_box(f"{name}_TL", (1.7, 0.1, 0.2), (0, -2.11, 0.60), mat_taillight, col=col_vehicles)
    tl.parent = root

    return root

# Hero Cars:
# Car_BlueCoupe is our HERO CAR: painted in solid vibrant ORANGE (Apex GT-90)
build_car("Car_BlueCoupe", mat_car_orange, (0, -16.0, 0.05)) # Hero Orange Sports Car!
build_car("Car_RedSedan",  mat_car_white,  (-22.0, 0, 0.05)) # White Sedan
build_car("Car_Taxi",      mat_car_taxi,   (0, 0, 0.05))     # Taxi
build_car("Car_WhiteVan",  mat_car_blue,   (0, 16.0, 0.05))  # Blue Van

print("6. Exporting clean GLB model...")
out_path = "/home/mncuchiinhuttt/city-threejs/public/assets/city.glb"
bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format="GLB",
    use_selection=False,
    export_apply=True,
    export_yup=True
)
print(f"Exported successfully to {out_path}!")
