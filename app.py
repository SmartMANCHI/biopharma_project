from flask import Flask, render_template, request
import math
from centrifuge.calculations import calculate_harvest
from depth_filtration.calculations import calculate_depth_filtration
from affinity_chromatography.calculations import calculate_affinity_chromatography
from affinity_chromatography.skid_selection import select_skid
from vin.calculations import calculate_vin
import pandas as pd

app = Flask(__name__)

def load_filter_library():
    df = pd.read_excel('library/depth_filter_library.xlsx')
    filter_library = {}
    for _, row in df.iterrows():
        filter_library[row['type']] = {'area': row['area'], 'discard_volume': row['discard_volume']}
    return filter_library

filter_library = load_filter_library()

@app.route('/')
def index():
    return render_template('index.html', filter_types=list(filter_library.keys()))

@app.route('/calculate', methods=['POST'])
def calculate():
    # Harvest inputs
    pcv = float(request.form['pcv'])
    centrifuge_flush_volume = float(request.form['centrifuge_flush_volume'])
    centrifuge_yield = float(request.form['centrifuge_yield'])
    brx_titer = float(request.form['brx_titer'])
    brx_volume = float(request.form['brx_volume'])

    # Depth filtration inputs
    filter_type = request.form['filter_type']
    harvest_filter_loading_capacity = float(request.form['harvest_filter_loading_capacity'])
    harvest_depth_filtration_yield = float(request.form['harvest_depth_filtration_yield'])
    harvest_filter_wfi_flux_requirement = float(request.form['harvest_filter_wfi_flux_requirement'])
    harvest_wfi_volume_per_filter = float(request.form['harvest_wfi_volume_per_filter'])
    harvest_equilibration_volume_per_filter = float(request.form['harvest_equilibration_volume_per_filter'])
    harvest_chase_volume_per_filter = float(request.form['harvest_chase_volume_per_filter'])
    harvest_filter_process_flux_requirement = float(request.form['harvest_filter_process_flux_requirement'])

    # Affinity chromatography inputs
    desired_cycle_number = float(request.form['desired_cycle_number'])
    ac_column_bh = float(request.form['ac_column_bh'])
    ac_resin_capacity = float(request.form['ac_resin_capacity'])
    ac_resin_compression_factor = float(request.form['ac_resin_compression_factor'])
    ac_max_linear_flowrate = float(request.form['ac_max_linear_flowrate'])
    ac_cycle_eluate_cv = float(request.form['ac_cycle_eluate_cv'])
    ac_yield = float(request.form['ac_yield'])

    # VIN inputs
    vin_acid_ratio = float(request.form['vin_acid_ratio'])
    vin_base_ratio = float(request.form['vin_base_ratio'])
    vin_yield = float(request.form['vin_yield'])
    process_type = request.form['process_type']

    # Calculate centrifuge outputs
    volume_removed_by_pcv, centrifuge_volume_out, centrifuge_mass_out = calculate_harvest(
        pcv, centrifuge_flush_volume, centrifuge_yield, brx_titer, brx_volume
    )

    # Calculate depth filtration outputs
    depth_filtration_outputs = calculate_depth_filtration(
        centrifuge_mass_out, 
        centrifuge_volume_out, 
        filter_type, 
        filter_library, 
        harvest_filter_loading_capacity, 
        harvest_depth_filtration_yield, 
        harvest_filter_wfi_flux_requirement, 
        harvest_wfi_volume_per_filter, 
        harvest_equilibration_volume_per_filter, 
        harvest_chase_volume_per_filter, 
        harvest_filter_process_flux_requirement
    )

    # Calculate affinity chromatography outputs
    affinity_chromatography_outputs = calculate_affinity_chromatography(
        desired_cycle_number,
        ac_column_bh,
        ac_resin_capacity,
        ac_resin_compression_factor,
        depth_filtration_outputs[2],  # harvest_depth_filtration_mass_out
        depth_filtration_outputs[3],  # harvest_depth_filtration_volume_out
        ac_max_linear_flowrate,
        ac_cycle_eluate_cv,
        ac_yield
    )

    # Select skid
    skid_selection = select_skid(affinity_chromatography_outputs[2])  # max_ac_volume_flowrate

    # Calculate VIN outputs
    vin_outputs = calculate_vin(
        vin_acid_ratio,
        vin_base_ratio,
        affinity_chromatography_outputs[4],  # ac_pool_volume
        affinity_chromatography_outputs[5],  # ac_mass_out
        vin_yield,
        process_type,
        desired_cycle_number
    )

    # Display the results
    results = {
        "volume_removed_by_pcv": round(volume_removed_by_pcv, 2),
        "centrifuge_volume_out": round(centrifuge_volume_out, 2),
        "centrifuge_mass_out": round(centrifuge_mass_out, 2),
        "total_number_harvest_filter_required": round(depth_filtration_outputs[0], 2),
        "total_harvest_filter_area_installed": round(depth_filtration_outputs[1], 2),
        "harvest_depth_filtration_mass_out": round(depth_filtration_outputs[2], 2),
        "harvest_depth_filtration_volume_out": round(depth_filtration_outputs[3], 2),
        "number_harvest_filter_rack_required": round(depth_filtration_outputs[4], 2),
        "number_of_filters_on_eachrack": round(depth_filtration_outputs[5], 2),
        "harvest_depth_filtration_wfi_flowrate": round(depth_filtration_outputs[6], 2),
        "harvest_depth_filtration_process_flowrate": round(depth_filtration_outputs[7], 2),
        "ac_column_diameter": round(affinity_chromatography_outputs[0], 2),
        "ac_column_volume": round(affinity_chromatography_outputs[1], 2),
        "max_ac_volume_flowrate": round(affinity_chromatography_outputs[2], 2),
        "ac_eluate_cycle_volume": round(affinity_chromatography_outputs[3], 2),
        "ac_pool_volume": round(affinity_chromatography_outputs[4], 2),
        "ac_mass_out": round(affinity_chromatography_outputs[5], 2),
        "selected_skid_size": skid_selection['size'],
        "skid_material": skid_selection['material'],
        "total_acid_volume": round(vin_outputs[0], 2),
        "cycle_acid_volume": round(vin_outputs[1], 2),
        "vin_volume_after_acid_addition": round(vin_outputs[2], 2),
        "total_base_volume": round(vin_outputs[3], 2),
        "cycle_base_volume": round(vin_outputs[4], 2),
        "vin_volume_out": round(vin_outputs[5], 2),
        "vin_mass_out": round(vin_outputs[6], 2)
    }

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
