import math
from centrifuge.calculations import calculate_harvest
from depth_filtration.calculations import calculate_depth_filtration
from Affinity_Chromatography.calculations import calculate_affinity_chromatography
from Affinity_Chromatography.skid_selection import select_skid

# Example filter library
filter_library = {
    'TypeA': {
        'area': 1.1,  # m²
        'discard_volume': 5.0,  # L/m²
    },
    'TypeB': {
        'area': 1.1,  # m²
        'discard_volume': 5.0,  # L/m²
    },
}

# Harvest inputs
PCV = 30
Centrifuge_Flush_Volume = 50
Centrifuge_Yield = 90
BRX_Titer = 1.5
BRX_Volume = 1000

# Depth filtration inputs
filter_type = 'TypeA'
Harvest_Filter_Loading_Capacity = 100.0
Harvest_Depth_Filtration_Yield = 95
Harvest_Filter_WFI_Flux_Requirement = 30
Harvest_WFI_Volume_Per_Filter = 2.0
Harvest_Equilibration_Volume_Per_Filter = 1.0
Harvest_Chase_Volume_Per_Filter = 1.0
Harvest_Filter_Process_Flux_Requirement = 50.0

# Affinity Chromatography inputs
Desired_Cycle_Number = 3
AC_Column_BH = 20
AC_Resin_Capacity = 40
AC_Resin_Compression_Factor = 1.2
AC_Max_Linear_Flowrate = 300
AC_Cycle_Eluate_CV = 4

# Calculate centrifuge outputs
Volume_removed_by_PCV, Centrifuge_Volume_Out, Centrifuge_Mass_Out = calculate_harvest(PCV, Centrifuge_Flush_Volume, Centrifuge_Yield, BRX_Titer, BRX_Volume)

# Calculate depth filtration outputs
depth_filtration_outputs = calculate_depth_filtration(
    Centrifuge_Mass_Out, 
    Centrifuge_Volume_Out, 
    filter_type, 
    filter_library, 
    Harvest_Filter_Loading_Capacity, 
    Harvest_Depth_Filtration_Yield, 
    Harvest_Filter_WFI_Flux_Requirement, 
    Harvest_WFI_Volume_Per_Filter, 
    Harvest_Equilibration_Volume_Per_Filter, 
    Harvest_Chase_Volume_Per_Filter, 
    Harvest_Filter_Process_Flux_Requirement
)

# Calculate affinity chromatography outputs
AC_Column_Diameter, AC_Column_Volume, Max_AC_Volume_Flowrate, AC_Eluate_Cycle_Volume, AC_Pool_Volume = calculate_affinity_chromatography(
    Desired_Cycle_Number,
    AC_Column_BH,
    AC_Resin_Capacity,
    AC_Resin_Compression_Factor,
    depth_filtration_outputs[2],  # Harvest_Depth_Filtration_Mass_Out
    depth_filtration_outputs[3],  # Harvest_Depth_Filtration_Volume_Out
    AC_Max_Linear_Flowrate,
    AC_Cycle_Eluate_CV
)

# Select skid based on max volume flow rate
selected_skid_size, skid_material = select_skid(Max_AC_Volume_Flowrate)

# Display the results
print("Centrifuge Outputs:")
print(f"Volume Removed by PCV: {Volume_removed_by_PCV:.2f} L")
print(f"Centrifuge Volume Out: {Centrifuge_Volume_Out:.2f} L")
print(f"Centrifuge Mass Out: {Centrifuge_Mass_Out:.2f} g")

print("\nDepth Filtration Outputs:")
print(f"Total Number of Harvest Filters Required: {depth_filtration_outputs[0]}")
print(f"Total Harvest Filter Area Installed: {depth_filtration_outputs[1]:.2f} m²")
print(f"Harvest Depth Filtration Mass Out: {depth_filtration_outputs[2]:.2f} g")
print(f"Harvest Depth Filtration Volume Out: {depth_filtration_outputs[3]:.2f} L")
print(f"Number of Harvest Filter Racks Required: {depth_filtration_outputs[4]}")
print(f"Number of Filters on Each Rack: {depth_filtration_outputs[5]}")
print(f"Harvest Depth Filtration WFI Flowrate: {depth_filtration_outputs[6]:.2f} L/hr")
print(f"Harvest Depth Filtration Process Flowrate: {depth_filtration_outputs[7]:.2f} L/hr")

print("\nAffinity Chromatography Outputs:")
print(f"AC Column Diameter: {AC_Column_Diameter:.2f} cm")
print(f"AC Column Volume: {AC_Column_Volume:.2f} L")
print(f"Max AC Volume Flowrate: {Max_AC_Volume_Flowrate:.2f} L/hr")
print(f"AC Eluate Cycle Volume: {AC_Eluate_Cycle_Volume:.2f} L")
print(f"AC Pool Volume: {AC_Pool_Volume:.2f} L")
print(f"Selected Skid Size: {selected_skid_size}")
print(f"Skid Material: {skid_material}")
