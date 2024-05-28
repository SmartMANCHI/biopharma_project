import math

def calculate_affinity_chromatography(desired_cycle_number, ac_column_bh, ac_resin_capacity, ac_resin_compression_factor, harvest_depth_filtration_mass_out, harvest_depth_filtration_volume_out, ac_max_linear_flowrate, ac_cycle_eluate_cv, ac_yield):
    # Calculate the required column volume
    required_volume = harvest_depth_filtration_mass_out / (desired_cycle_number * ac_resin_capacity)
    compressed_volume = required_volume * ac_resin_compression_factor

    # Calculate column diameter
    ac_column_diameter = math.sqrt((4 * compressed_volume * 1000) / (math.pi * ac_column_bh))

    # Select the closest available column diameter
    available_diameters = [20, 40, 60, 80, 120, 160]  # in cm
    ac_column_diameter = min(available_diameters, key=lambda x: abs(x - ac_column_diameter))

    # Calculate column volume in liters
    ac_column_volume = (1 / 4) * math.pi * (ac_column_diameter ** 2) * ac_column_bh * 0.001

    # Calculate maximum volume flow rate
    max_ac_volume_flowrate = ac_max_linear_flowrate * (1 / 4) * math.pi * (ac_column_diameter ** 2) * 0.001

    # Calculate eluate cycle volume
    ac_eluate_cycle_volume = ac_cycle_eluate_cv * ac_column_volume

    # Calculate pool volume
    ac_pool_volume = ac_eluate_cycle_volume * desired_cycle_number

    # Calculate mass out
    ac_mass_out = (ac_yield / 100) * harvest_depth_filtration_mass_out

    return ac_column_diameter, ac_column_volume, max_ac_volume_flowrate, ac_eluate_cycle_volume, ac_pool_volume, ac_mass_out
