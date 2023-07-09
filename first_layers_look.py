import sys
from extrusion_width_hight import number_from_string

def pause_after_brim(gcode_file:str, X:int=220, Y:int=220, brim_layer_count:int=0):
    '''Adds stops in printing after last brim to give possibility to look at the specific layer'''
    # Open the file in read mode
    with open(gcode_file, "r") as file:
        lines: list[str] = file.readlines()  # Read all lines of the file

    # search for quantity of brim layer
    if brim_layer_count == 0:
        for line in reversed(lines):
            if "; wipe_tower_brim_width" in line:
                brim_layer_count=number_from_string(line)
                break
    # if didn't find any return
    if brim_layer_count == 0:
        print("Isn't any brim/skirt in the file")
        return

    for i, line in enumerate(lines):
        if ";TYPE:Skirt/Brim" in line:
            brim_layer_count -= 1
        if brim_layer_count == 0 and len(line) >= 5 and line[3] == "X":
            words: list[str] = line.split()
            # Store the last X and Y positions
            last_x: str = words[1]
            last_y: str = words[2]
        if brim_layer_count == 0 and ";WIPE_END" in line:
            if "Move for clear look" in lines[i + 1]:
                print("The brim layer already have the stop")
                return
            lines.insert(i + 1, f"G1 X{X} Y{Y} E-0.16761  ; Move for clear look\nM0 Look at layers\nG1 %s %s E-0.16761  "
                                ";Move Back\n" % (last_x, last_y))
            break  # Stop the loop after the third occurrence
        # Write the modified lines back to the file
    with open(gcode_file, "w") as file:
        file.writelines(lines)
    print(f"In {gcode_file} added stop on brim/skirt layer at the position X{X} and Y{Y}")

def layer_look(gcode_file:str, layer:int=2, X:int=220, Y:int=220):
    '''Adds stops in printing to give possibility to loock at the specific layer'''
    # Open the file in read mode
    with open(gcode_file, "r") as file:
        lines: list[str] = file.readlines()  # Read all lines of the file
    # Count the occurrences of ";AFTER_LAYER_CHANGE"
    count: int = -1
    for i, line in enumerate(lines):
        if len(line) >= 5 and line[3] == "X":
            words: list[str] = line.split()
            # Store the last X and Y positions
            last_x: str = words[1]
            last_y: str = words[2]
        if ";AFTER_LAYER_CHANGE" in line:
            count += 1

            # Check if the count is 3
            if count == layer:
                if "Move for clear look" in lines[i + 1]:
                    print(f"The {layer} layer already have the stop")
                    return
                lines.insert(i + 1, f"G1 X{X} Y{Y} E-0.16761  ; Move for clear look\nM0 Look at layers\nG1 %s %s E-0.16761  "
                                    ";Move Back\n" % (last_x, last_y))
                break  # Stop the loop after the third occurrence
    # Write the modified lines back to the file
    with open(gcode_file, "w") as file:
        file.writelines(lines)
    print(f"In {gcode_file} added stop on {layer} layer at the position X{X} and Y{Y}")



if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'h' or sys.argv[1] == 'help':
            print("Add '-l' to set the first layer look.\nExample: first_layers_look.py <example.gcode> -l2")
        if len(sys.argv) > 2:
            if "-l" in sys.argv[2]:
                layer_look(gcode_file=sys.argv[1],
                           layer = number_from_string(sys.argv[2]))
            if "-b" in sys.argv[2]:
                pause_after_brim(gcode_file=sys.argv[1],
                                 brim_layer_count=number_from_string(sys.argv[2]))
        else:
            layer_look(gcode_file=sys.argv[1])
    else:
        print("Example: first_layers_look.py <example.gcode>")



