import math

def calculate_brx_mass(brx_titer, brx_volume):
    return brx_titer * brx_volume

def calculate_harvest(pcv, centrifuge_flush_volume, centrifuge_yield, brx_titer, brx_volume):
    brx_mass = calculate_brx_mass(brx_titer, brx_volume)
    
    volume_removed_by_pcv = brx_volume * (pcv / 100)
    centrifuge_volume_out = brx_volume - volume_removed_by_pcv + centrifuge_flush_volume
    centrifuge_mass_out = brx_mass * (centrifuge_yield / 100)
    
    return volume_removed_by_pcv, centrifuge_volume_out, centrifuge_mass_out
