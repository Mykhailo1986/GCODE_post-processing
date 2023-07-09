import sys
import extrusion_width_hight

def check_LA_in_gcode(gcode_file:str)->bool:
    '''return True if Line Advance is already in file'''
    with open(gcode_file, "r") as file:
        lines:list = file.readlines()  # Read all lines of the file
        for line in lines:
            if ";LINEARADVANCEPROCESSED" in line:
                return True
        return False
def add_LA(gcode_file:str,line_width: float, layer_height : float  , linear_advance_factor: float=0.8, material_diameter: float=1.75 ):
    '''Insert Linaer Avance lines in gcodefile'''

    if check_LA_in_gcode(gcode_file):
        return
    # Open the file in read mode
    with open(gcode_file, "r") as file:
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
    with open(gcode_file, "w") as file:
        file.writelines(lines)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == 'h' or sys.argv[1] == 'help':
            print("Add '-k' to set the linear advance factor.\nExample: linear_advance_add.py <example.gcode> -k0.8")
        if sys.argv[2] and "-k" in sys.argv[2]:
            add_LA(
                gcode_file=sys.argv[1],
                line_width=extrusion_width_hight.line_width(gcode_file=sys.argv[1]),
                layer_height=extrusion_width_hight.layer_higth(gcode_file=sys.argv[1]),
                linear_advance_factor=extrusion_width_hight.number_from_string(sys.argv[2])
            )
        else:
            add_LA(
                gcode_file=sys.argv[1],
                line_width=extrusion_width_hight.line_width(gcode_file=sys.argv[1]),
                layer_height=extrusion_width_hight.layer_higth(gcode_file=sys.argv[1]))
    else:
        print("nExample: linear_advance_add.py <example.gcode> -k0.8")


