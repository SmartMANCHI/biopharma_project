def calculate_vin(vin_acid_ratio, vin_base_ratio, ac_pool_volume, ac_mass_out, vin_yield, process_type, desired_cycle_number):
    # Convert ratios to decimals
    vin_acid_ratio = vin_acid_ratio / 100
    vin_base_ratio = vin_base_ratio / 100
    vin_yield = vin_yield / 100
    
    total_acid_volume = vin_acid_ratio * ac_pool_volume
    vin_volume_after_acid_addition = total_acid_volume + ac_pool_volume
    total_base_volume = vin_base_ratio * vin_volume_after_acid_addition
    vin_volume_out = vin_volume_after_acid_addition + total_base_volume
    vin_mass_out = vin_yield * ac_mass_out

    if process_type == 'separate':
        cycle_acid_volume = total_acid_volume / desired_cycle_number
        cycle_base_volume = vin_volume_after_acid_addition / desired_cycle_number * vin_base_ratio
    elif process_type == 'combined':
        cycle_acid_volume = total_acid_volume
        cycle_base_volume = total_base_volume
    
    return total_acid_volume, cycle_acid_volume, vin_volume_after_acid_addition, total_base_volume, cycle_base_volume, vin_volume_out, vin_mass_out
