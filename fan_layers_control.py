def fan_on_off(gcode_file:str, FAN_FROM: int, FAN_POWER : int  , FAN_TILL: int):
    '''Changes the gcode, adds the starts and stops of fan'''

    # Open the file in read mode
    with open(gcode_file, "r") as file:
        lines = file.readlines()  # Read all lines of the file
    # Count the occurrences of ";AFTER_LAYER_CHANGE"
    count: int = 0
    for i, line in enumerate(lines):
        if ";AFTER_LAYER_CHANGE" in line:
            count += 1

            # Check if the count is bigger of equal FAN_FROM and less  than FAN_TIL
            # if FAN_FROM <= count < FAN_TILL:
            if count == FAN_FROM:
                lines.insert(i + 1, f"M106 S{FAN_POWER}   ; Turn on the fan at set speed\n")

            if count == FAN_TILL:
                lines.insert(i + 1, "M106 S0   ; Turn off the fan \n")
                break  # Stop the loop after the occurrence
    # Write the modified lines back to the file
    with open(gcode_file, "w") as file:
        file.writelines(lines)



