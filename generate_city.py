import bpy
import math
import random

# Clear existing objects and data
bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, base_color, roughness=0.5, metallic=0.0, emission_color=(0,0,0,1), emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

# --- Materials Palette ---
mat_road = create_material("MAT_Road", (0.13, 0.14, 0.16, 1.0), roughness=0.85)
mat_mountain_road = create_material("MAT_MountainRoad", (0.18, 0.17, 0.16, 1.0), roughness=0.9)
mat_sidewalk = create_material("MAT_Sidewalk", (0.70, 0.72, 0.74, 1.0), roughness=0.7)
mat_marking = create_material("MAT_RoadMarking", (0.95, 0.95, 0.95, 1.0), roughness=0.6)
mat_marking_yellow = create_material("MAT_MarkingYellow", (0.95, 0.80, 0.10, 1.0), roughness=0.6)
mat_grass = create_material("MAT_Grass", (0.28, 0.52, 0.24, 1.0), roughness=0.85)
mat_mountain_rock = create_material("MAT_MountainRock", (0.42, 0.40, 0.38, 1.0), roughness=0.9)
mat_mountain_snow = create_material("MAT_MountainSnow", (0.92, 0.94, 0.96, 1.0), roughness=0.6)
mat_guardrail = create_material("MAT_Guardrail", (0.85, 0.25, 0.25, 1.0), roughness=0.4, metallic=0.6)

# Building materials
mat_wall_concrete = create_material("MAT_WallConcrete", (0.82, 0.83, 0.85, 1.0), roughness=0.6)
mat_wall_terracotta = create_material("MAT_WallTerracotta", (0.75, 0.38, 0.28, 1.0), roughness=0.6)
mat_wall_blue = create_material("MAT_WallBlue", (0.22, 0.35, 0.50, 1.0), roughness=0.5)
mat_wall_dark = create_material("MAT_WallDark", (0.18, 0.20, 0.23, 1.0), roughness=0.4)
mat_wall_yellow = create_material("MAT_WallYellow", (0.85, 0.72, 0.35, 1.0), roughness=0.6)
mat_roof = create_material("MAT_Roof", (0.16, 0.17, 0.20, 1.0), roughness=0.9)

# Windows (Emissive for night glow)
mat_window = create_material("MAT_Window", (0.98, 0.88, 0.50, 1.0), roughness=0.2, metallic=0.1,
                             emission_color=(1.0, 0.85, 0.40, 1.0), emission_strength=2.2)
mat_window_cyan = create_material("MAT_WindowCyan", (0.5, 0.9, 1.0, 1.0), roughness=0.2, metallic=0.1,
                                  emission_color=(0.1, 0.8, 1.0, 1.0), emission_strength=2.2)
mat_neon_pink = create_material("MAT_NeonPink", (1.0, 0.1, 0.6, 1.0), roughness=0.2,
                                emission_color=(1.0, 0.1, 0.6, 1.0), emission_strength=3.5)
mat_neon_cyan = create_material("MAT_NeonCyan", (0.0, 0.95, 1.0, 1.0), roughness=0.2,
                                emission_color=(0.0, 0.95, 1.0, 1.0), emission_strength=3.5)

# Props
mat_metal = create_material("MAT_Metal", (0.45, 0.47, 0.50, 1.0), roughness=0.3, metallic=0.8)
mat_wood = create_material("MAT_Wood", (0.42, 0.26, 0.16, 1.0), roughness=0.75)
mat_foliage = create_material("MAT_Foliage", (0.16, 0.45, 0.20, 1.0), roughness=0.8)
mat_foliage_light = create_material("MAT_FoliageLight", (0.32, 0.60, 0.26, 1.0), roughness=0.8)
mat_pine = create_material("MAT_Pine", (0.12, 0.35, 0.18, 1.0), roughness=0.85)
mat_trunk = create_material("MAT_Trunk", (0.30, 0.20, 0.14, 1.0), roughness=0.85)
mat_streetlamp_glow = create_material("MAT_StreetlampGlow", (1.0, 0.95, 0.8, 1.0), roughness=0.1,
                                      emission_color=(1.0, 0.92, 0.70, 1.0), emission_strength=4.5)

# Vehicles
mat_car_red = create_material("MAT_CarRed", (0.88, 0.10, 0.15, 1.0), roughness=0.2, metallic=0.6)
mat_car_taxi = create_material("MAT_CarTaxi", (0.96, 0.76, 0.04, 1.0), roughness=0.25, metallic=0.4)
mat_car_blue = create_material("MAT_CarBlue", (0.08, 0.45, 0.90, 1.0), roughness=0.2, metallic=0.7)
mat_car_white = create_material("MAT_CarWhite", (0.92, 0.92, 0.94, 1.0), roughness=0.3, metallic=0.2)
mat_car_glass = create_material("MAT_CarGlass", (0.12, 0.18, 0.24, 1.0), roughness=0.1, metallic=0.8)
mat_headlight = create_material("MAT_Headlight", (1.0, 1.0, 0.9, 1.0), roughness=0.1,
                                emission_color=(1.0, 1.0, 0.85, 1.0), emission_strength=5.0)
mat_taillight = create_material("MAT_Taillight", (1.0, 0.05, 0.05, 1.0), roughness=0.1,
                                emission_color=(1.0, 0.05, 0.05, 1.0), emission_strength=4.0)
mat_wheel = create_material("MAT_Wheel", (0.08, 0.08, 0.09, 1.0), roughness=0.8)
mat_rim = create_material("MAT_Rim", (0.75, 0.76, 0.78, 1.0), roughness=0.25, metallic=0.85)

# --- Collections ---
def get_or_create_col(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

col_roads = get_or_create_col("COL_Roads")
col_buildings = get_or_create_col("COL_Buildings")
col_mountains = get_or_create_col("COL_Mountains")
col_props = get_or_create_col("COL_Props")
col_vehicles = get_or_create_col("COL_Vehicles")

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

def add_cylinder(name, radius, depth, loc, mat, vertices=10, rot=(0,0,0), col=col_props):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj

def add_cone(name, radius, depth, loc, mat, vertices=7, rot=(0,0,0), col=col_props):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=0.0, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj

print("Generating City & Mountain Pass World...")

# 1. DOWNTOWN CITY GROUND & BLOCKS
add_box("Ground_City_Asphalt", (40.0, 40.0, 0.4), (0, 0, -0.2), mat_road, col=col_roads)

# Sidewalk Blocks
block_centers = [(-10.0, -10.0), (10.0, -10.0), (-10.0, 10.0), (10.0, 10.0)]
for b_idx, (bx, by) in enumerate(block_centers):
    add_box(f"Sidewalk_Block_{b_idx}", (13.0, 13.0, 0.25), (bx, by, 0.125), mat_sidewalk, col=col_roads)

# Road markings
for y in range(-16, 17, 3):
    if -3.5 < y < 3.5: continue
    add_box(f"Marking_Y_{y}", (0.16, 1.4, 0.02), (0, y, 0.02), mat_marking, col=col_roads)
for x in range(-16, 17, 3):
    if -3.5 < x < 3.5: continue
    add_box(f"Marking_X_{x}", (1.4, 0.16, 0.02), (x, 0, 0.02), mat_marking, col=col_roads)

# Crosswalk stripes
for d_val in [-2.5, 2.5]:
    for i in range(-5, 6):
        add_box(f"Crosswalk_NS_{d_val}_{i}", (0.32, 0.9, 0.02), (i * 0.55, d_val * 1.5, 0.02), mat_marking, col=col_roads)
        add_box(f"Crosswalk_EW_{d_val}_{i}", (0.9, 0.32, 0.02), (d_val * 1.5, i * 0.55, 0.02), mat_marking, col_roads)

# 2. SKYSCRAPERS & SHOPS
def build_skyscraper(name, loc, size, wall_mat):
    w, d, h = size
    bx, by, bz = loc
    add_box(f"{name}_Main", (w, d, h), (bx, by, bz + h/2), wall_mat, col=col_buildings)
    floors = int(h / 1.0) - 1
    cols_x = max(1, int(w / 1.1))
    cols_y = max(1, int(d / 1.1))
    for fl in range(1, floors):
        z_pos = bz + fl * 1.0 + 0.3
        for cx in range(cols_x):
            xp = bx - w/2 + (cx + 0.5) * (w / cols_x)
            add_box(f"{name}_W_N_{fl}_{cx}", (0.45, 0.06, 0.45), (xp, by + d/2 + 0.01, z_pos), mat_window, col=col_buildings)
            add_box(f"{name}_W_S_{fl}_{cx}", (0.45, 0.06, 0.45), (xp, by - d/2 - 0.01, z_pos), mat_window, col=col_buildings)
        for cy in range(cols_y):
            yp = by - d/2 + (cy + 0.5) * (d / cols_y)
            add_box(f"{name}_W_E_{fl}_{cy}", (0.06, 0.45, 0.45), (bx + w/2 + 0.01, yp, z_pos), mat_window, col=col_buildings)
            add_box(f"{name}_W_W_{fl}_{cy}", (0.06, 0.45, 0.45), (bx - w/2 - 0.01, yp, z_pos), mat_window, col=col_buildings)
    # Roof details
    add_box(f"{name}_RoofTier", (w*0.75, d*0.75, 1.2), (bx, by, bz + h + 0.6), mat_roof, col=col_buildings)
    if h > 8.0:
        add_cylinder(f"{name}_Antenna", 0.05, 3.0, (bx, by, bz + h + 2.7), mat_metal, vertices=6, col=col_buildings)
        add_cylinder(f"{name}_AntennaLight", 0.1, 0.15, (bx, by, bz + h + 4.2), mat_taillight, vertices=6, col=col_buildings)

def build_commercial_shop(name, loc, size, wall_mat, canopy_mat):
    w, d, h = size
    bx, by, bz = loc
    add_box(f"{name}_Base", (w, d, h), (bx, by, bz + h/2), wall_mat, col=col_buildings)
    add_box(f"{name}_Glass", (w*0.75, 0.08, h*0.45), (bx, by - d/2 - 0.02, bz + h*0.28), mat_window_cyan, col=col_buildings)
    add_box(f"{name}_Canopy", (w*0.85, 0.9, 0.15), (bx, by - d/2 - 0.45, bz + h*0.55), canopy_mat, col=col_buildings)
    add_box(f"{name}_Neon", (w*0.6, 0.1, 0.4), (bx, by - d/2 - 0.05, bz + h*0.8), mat_neon_pink, col=col_buildings)

# Place City Buildings
build_skyscraper("Tower_SW_A", (-12.0, -12.0, 0.25), (4.5, 4.5, 13.0), mat_wall_blue)
build_skyscraper("Tower_SW_B", (-7.0, -12.0, 0.25), (3.6, 3.6, 8.5), mat_wall_concrete)
build_commercial_shop("Shop_SW_C", (-9.5, -6.0, 0.25), (5.0, 4.0, 4.0), mat_wall_terracotta, mat_neon_pink)

build_skyscraper("Tower_SE_A", (12.0, -12.0, 0.25), (4.8, 4.8, 15.0), mat_wall_dark)
build_skyscraper("Tower_SE_B", (7.0, -12.0, 0.25), (3.6, 4.0, 9.0), mat_wall_concrete)
build_commercial_shop("Shop_SE_C", (9.5, -6.0, 0.25), (5.5, 4.0, 3.8), mat_wall_yellow, mat_neon_cyan)

build_skyscraper("Apt_NW_A", (-11.5, 11.5, 0.25), (4.2, 5.0, 8.0), mat_wall_terracotta)
build_skyscraper("Apt_NW_B", (-6.0, 11.5, 0.25), (4.0, 4.0, 6.0), mat_wall_yellow)

build_skyscraper("Office_NE_A", (11.5, 11.5, 0.25), (4.5, 4.5, 11.0), mat_wall_concrete)
build_commercial_shop("Cafe_NE_B", (6.0, 10.5, 0.25), (4.2, 4.0, 3.5), mat_wall_blue, mat_neon_pink)

# 3. SCENIC MOUNTAIN PASS & ROCKY PEAKS (CUNG ĐƯỜNG NÚI)
# Positioned at East / North-East perimeter (X from 20 to 55, Y from -25 to 35)
print("Building Mountain Pass & Peaks...")

# Large Mountain Base Mass
mountain_peaks = [
    # (name, radius, height, location, vertices)
    ("Peak_Alpha", 18.0, 24.0, (38.0, 12.0, 0), 7),
    ("Peak_Beta",  15.0, 20.0, (42.0, -10.0, 0), 6),
    ("Peak_Gamma", 14.0, 18.0, (28.0, 26.0, 0), 8),
    ("Peak_Delta", 12.0, 15.0, (32.0, -22.0, 0), 6),
    ("Ridge_East", 20.0, 16.0, (48.0, 5.0, 0), 7),
]

for name, rad, h, loc, verts in mountain_peaks:
    # Mountain Body
    add_cone(f"{name}_Rock", rad, h, (loc[0], loc[1], h/2), mat_mountain_rock, vertices=verts, col=col_mountains)
    # Snowcap at top (upper 25%)
    snow_h = h * 0.3
    add_cone(f"{name}_Snow", rad * 0.35, snow_h, (loc[0], loc[1], h - snow_h/2), mat_mountain_snow, vertices=verts, col=col_mountains)

# Mountain Ground Slope
add_box("Mountain_Slope_Base", (30.0, 60.0, 1.2), (32.0, 5.0, 0.4), mat_mountain_rock, col=col_mountains)

# Elevated Mountain Pass Road (Cung đường đèo uốn lượn trên núi)
# Road segments climbing up the mountain slope
mountain_road_segments = [
    # (loc, size, rot_z, rot_y)
    ((20.0, -16.0, 0.5), (6.0, 3.5, 0.3), 0.1, 0.05),
    ((23.0, -12.0, 1.2), (6.0, 3.5, 0.3), 0.3, 0.08),
    ((26.0, -6.0, 2.2),  (6.5, 3.5, 0.3), 0.4, 0.10),
    ((28.5, 0.0, 3.4),   (6.5, 3.5, 0.3), 0.2, 0.12),
    ((30.0, 6.0, 4.6),   (6.5, 3.5, 0.3), -0.1, 0.08),
    ((29.0, 13.0, 5.5),  (6.5, 3.5, 0.3), -0.3, 0.05), # Highest scenic overlook
    ((26.0, 19.0, 4.2),  (6.5, 3.5, 0.3), -0.4, -0.08),
    ((22.5, 24.0, 2.6),  (6.0, 3.5, 0.3), -0.2, -0.10),
    ((19.0, 27.0, 1.0),  (6.0, 3.5, 0.3), -0.1, -0.06),
]

for idx, (loc, sz, rz, ry) in enumerate(mountain_road_segments):
    # Road slab
    add_box(f"Mtn_Road_{idx}", sz, loc, mat_mountain_road, rot=(0, ry, rz), col=col_roads)
    # Red-white guardrails on the outer cliffside
    gx = loc[0] + 1.8 * math.cos(rz + math.pi/2)
    gy = loc[1] + 1.8 * math.sin(rz + math.pi/2)
    add_box(f"Guardrail_{idx}", (sz[0], 0.15, 0.5), (gx, gy, loc[2] + 0.35), mat_guardrail, rot=(0, ry, rz), col=col_props)

# Scenic Overlook Platform at top of mountain road
add_box("Scenic_Overlook_Deck", (8.0, 5.0, 0.5), (32.0, 12.0, 5.3), mat_wood, col=col_mountains)
# Overlook observation lights
add_cylinder("Overlook_Lantern", 0.15, 2.0, (32.0, 14.0, 6.3), mat_metal, col=col_props)
add_cylinder("Overlook_Lantern_Bulb", 0.22, 0.3, (32.0, 14.0, 7.3), mat_streetlamp_glow, col=col_props)

# Alpine Pine Trees on the mountain slopes
pine_coords = [
    (24.0, -18.0, 0.5, 1.3),
    (28.0, -14.0, 1.8, 1.5),
    (31.0, -8.0, 2.8, 1.4),
    (33.0, -2.0, 3.8, 1.6),
    (34.0, 4.0, 4.8, 1.7),
    (35.0, 10.0, 5.8, 1.5),
    (33.0, 18.0, 5.0, 1.8),
    (28.0, 22.0, 3.5, 1.4),
    (24.0, 28.0, 1.8, 1.3),
    (36.0, -16.0, 2.5, 2.0),
    (40.0, 0.0, 6.0, 2.2),
    (38.0, 20.0, 7.0, 2.0),
]

for idx, (px, py, pz, psc) in enumerate(pine_coords):
    # Pine Trunk
    add_cylinder(f"Pine_Trunk_{idx}", 0.18*psc, 1.5*psc, (px, py, pz + 0.75*psc), mat_trunk, vertices=6, col=col_props)
    # Tiered Pine Foliage (3 stacked sharp cones)
    add_cone(f"Pine_F1_{idx}", 1.4*psc, 1.6*psc, (px, py, pz + 1.8*psc), mat_pine, vertices=7, col=col_props)
    add_cone(f"Pine_F2_{idx}", 1.1*psc, 1.4*psc, (px, py, pz + 2.6*psc), mat_pine, vertices=6, col=col_props)
    add_cone(f"Pine_F3_{idx}", 0.7*psc, 1.2*psc, (px, py, pz + 3.4*psc), mat_foliage_light, vertices=5, col=col_props)

# 4. STREET PROPS & LIGHTS
def add_streetlight(name, loc):
    x, y, z = loc
    add_cylinder(f"{name}_Pole", 0.08, 3.2, (x, y, z + 1.6), mat_metal, vertices=6, col=col_props)
    add_box(f"{name}_Arm", (0.1, 0.7, 0.1), (x, y + 0.3, z + 3.15), mat_metal, col=col_props)
    add_box(f"{name}_Head", (0.25, 0.35, 0.12), (x, y + 0.6, z + 3.05), mat_metal, col=col_props)
    add_box(f"{name}_Bulb", (0.18, 0.25, 0.04), (x, y + 0.6, z + 2.97), mat_streetlamp_glow, col=col_props)

lamp_coords = [
    ("Lamp_SW_1", (-3.8, -3.8, 0.25)),
    ("Lamp_SE_1", ( 3.8, -3.8, 0.25)),
    ("Lamp_NW_1", (-3.8,  3.8, 0.25)),
    ("Lamp_NE_1", ( 3.8,  3.8, 0.25)),
    ("Lamp_W_Far", (-3.8, -17.0, 0.25)),
    ("Lamp_E_Far", ( 3.8, -17.0, 0.25)),
    ("Lamp_N_Far", (-17.0, 3.8, 0.25)),
    ("Lamp_S_Far", ( 17.0, -3.8, 0.25)),
]
for name, coord in lamp_coords:
    add_streetlight(name, coord)

# 5. CAR VEHICLES
def create_car(name, body_mat, loc=(0,0,0), is_taxi=False):
    car_empty = bpy.data.objects.new(name, None)
    car_empty.location = loc
    col_vehicles.objects.link(car_empty)

    lower = add_box(f"{name}_LowerBody", (1.6, 3.4, 0.6), (0, 0, 0.45), body_mat, col=col_vehicles)
    lower.parent = car_empty

    cabin = add_box(f"{name}_Cabin", (1.3, 1.8, 0.55), (0, -0.2, 0.95), mat_car_glass, col=col_vehicles)
    cabin.parent = car_empty

    roof = add_box(f"{name}_RoofCap", (1.28, 1.6, 0.08), (0, -0.2, 1.25), body_mat, col=col_vehicles)
    roof.parent = car_empty

    wheel_positions = [(-0.82, 1.0, 0.3), (0.82, 1.0, 0.3), (-0.82, -1.0, 0.3), (0.82, -1.0, 0.3)]
    for w_idx, (wx, wy, wz) in enumerate(wheel_positions):
        w_obj = add_cylinder(f"{name}_Wheel_{w_idx}", 0.32, 0.22, (wx, wy, wz), mat_wheel, vertices=10, rot=(0, math.pi/2, 0), col=col_vehicles)
        w_obj.parent = car_empty
        rim_x = wx + (0.02 if wx > 0 else -0.02)
        r_obj = add_cylinder(f"{name}_Rim_{w_idx}", 0.18, 0.24, (rim_x, wy, wz), mat_rim, vertices=8, rot=(0, math.pi/2, 0), col=col_vehicles)
        r_obj.parent = car_empty

    hl_l = add_box(f"{name}_Headlight_L", (0.3, 0.08, 0.16), (-0.55, 1.71, 0.5), mat_headlight, col=col_vehicles)
    hl_r = add_box(f"{name}_Headlight_R", (0.3, 0.08, 0.16), ( 0.55, 1.71, 0.5), mat_headlight, col=col_vehicles)
    hl_l.parent = car_empty
    hl_r.parent = car_empty

    tl_l = add_box(f"{name}_Taillight_L", (0.3, 0.08, 0.16), (-0.55, -1.71, 0.5), mat_taillight, col=col_vehicles)
    tl_r = add_box(f"{name}_Taillight_R", (0.3, 0.08, 0.16), ( 0.55, -1.71, 0.5), mat_taillight, col=col_vehicles)
    tl_l.parent = car_empty
    tl_r.parent = car_empty

    if is_taxi:
        tsign = add_box(f"{name}_TaxiSign", (0.55, 0.25, 0.2), (0, -0.2, 1.38), mat_window, col=col_vehicles)
        tsign.parent = car_empty

    return car_empty

create_car("Car_Taxi", mat_car_taxi, (1.6, -8.0, 0), is_taxi=True)
create_car("Car_RedSedan", mat_car_red, (-1.6, 8.0, 0))
create_car("Car_BlueCoupe", mat_car_blue, (8.0, 1.6, 0))
create_car("Car_WhiteVan", mat_car_white, (-8.0, -1.6, 0))

print("City & Mountain assembly complete! Exporting GLB...")

output_path = "/home/mncuchiinhuttt/city-threejs/public/assets/city.glb"
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format="GLB",
    use_selection=False,
    export_apply=True,
    export_yup=True
)

print(f"Exported updated City & Mountain Pass model to {output_path}")
