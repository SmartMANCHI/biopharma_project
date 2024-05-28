def select_skid(max_ac_volume_flowrate):
    skid_options = [
        {"size": "3/8'' o.d.", "flowrate_range": (4, 180), "material": "Unknown"},
        {"size": "1/2'' o.d. SS", "flowrate_range": (15, 600), "material": "Stainless Steel"},
        {"size": "1'' o.d. PP", "flowrate_range": (45, 1800), "material": "Polypropylene"},
        {"size": "1.5'' o.d. SS", "flowrate_range": (200, 5000), "material": "Stainless Steel"},
        {"size": "2.0'' o.d. SS", "flowrate_range": (200, 20000), "material": "Stainless Steel"},
    ]

    selected_skid = {"size": "Custom Skid Required", "material": "Unknown"}

    for skid in skid_options:
        if skid["flowrate_range"][0] <= max_ac_volume_flowrate <= skid["flowrate_range"][1]:
            selected_skid = {"size": skid["size"], "material": skid["material"]}
            break

    return selected_skid
