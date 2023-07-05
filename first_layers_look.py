def layer_look(gcode_file:str, layer:int, X:int, Y:int):
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
                lines.insert(i + 1, f"G1 X{X} Y{Y} E-0.16761  ; Move for clear look\nM0 Look at layers\nG1 %s %s E-0.16761  "
                                    ";Move Back\n" % (last_x, last_y))
                break  # Stop the loop after the third occurrence
    # Write the modified lines back to the file
    with open(gcode_file, "w") as file:
        file.writelines(lines)


