import sys


def add_LA(line_width: float, layer_height : float  , linear_advance_factor: float, material_diameter: float ):


    # Get the file path from the command line argument
    file_path = sys.argv[1]

    # Open the file in read mode
    with open(file_path, "r") as file:
        lines = file.readlines()  # Read all lines of the file
        lines.insert(10, ";LINEARADVANCEPROCESSED\n")
        lines.append(r';SETTING_3 {"global_quality": "[values]\\nline_width = 0.3\\nmaterial_linear_adv'+'\n')
        lines.append(r';SETTING_3 ance_factor = 0.8\\narcwelder_allow_dynamic_precision = True\\narcwel'+'\n')
        lines.append(r';SETTING_3 der_allow_travel_arcs = True\\n\\n", "extruder_quality": ["[general]'+'\n')
        lines.append(r';SETTING_3 \\nversion = 4\\nmaterial_linear_advance_enable = True\\n\\n"]}')

    # Count the occurrences of ";AFTER_LAYER_CHANGE"
    count: int = 0
    for i, line in enumerate(lines):
        if "home all axis" in line and count !=1:
            lines.insert(i , f"M900 K{linear_advance_factor}\n")
            lines.insert(i +1, f"M900 W{line_width} H{layer_height} D{material_diameter}\n")
            count += 1
        if "M107" in line:
            lines.insert(i , "M900 K{:.5f}0 T0 ;added by LinearAdvanceSettingPlugin\n".format(linear_advance_factor))
            break  # Stop the loop after the occurrence
    # Write the modified lines back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)

