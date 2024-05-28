import math

def calculate_depth_filtration(
        centrifuge_mass_out, centrifuge_volume_out, filter_type, filter_library, 
        harvest_filter_loading_capacity, harvest_depth_filtration_yield, 
        harvest_filter_wfi_flux_requirement, harvest_wfi_volume_per_filter, 
        harvest_equilibration_volume_per_filter, harvest_chase_volume_per_filter, 
        harvest_filter_process_flux_requirement):
    
    filter_properties = filter_library[filter_type]
    harvest_filter_area = filter_properties['area']
    harvest_filter_discard_volume = filter_properties['discard_volume']
    
    total_number_harvest_filter_required = math.ceil(centrifuge_volume_out / harvest_filter_loading_capacity / harvest_filter_area)
    total_harvest_filter_area_installed = total_number_harvest_filter_required * harvest_filter_area
    harvest_depth_filtration_mass_out = centrifuge_mass_out * (harvest_depth_filtration_yield / 100)
    harvest_depth_filtration_volume_out = centrifuge_volume_out - (harvest_filter_discard_volume * total_harvest_filter_area_installed) + (harvest_chase_volume_per_filter * total_harvest_filter_area_installed)
    number_harvest_filter_rack_required = math.ceil(total_number_harvest_filter_required / 10)
    number_of_filters_on_eachrack = math.ceil(total_number_harvest_filter_required / number_harvest_filter_rack_required)
    harvest_depth_filtration_wfi_flowrate = (number_of_filters_on_eachrack * harvest_filter_wfi_flux_requirement * harvest_filter_area)
    harvest_depth_filtration_process_flowrate =  (total_harvest_filter_area_installed * harvest_filter_process_flux_requirement)
    
    return (
        total_number_harvest_filter_required, total_harvest_filter_area_installed, 
        harvest_depth_filtration_mass_out, harvest_depth_filtration_volume_out, 
        number_harvest_filter_rack_required, number_of_filters_on_eachrack, 
        harvest_depth_filtration_wfi_flowrate, harvest_depth_filtration_process_flowrate
    )
