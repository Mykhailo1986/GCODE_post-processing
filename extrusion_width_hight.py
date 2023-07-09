import sys


# Get the file path from the command line argument
# gcode_file = sys.argv[1]

def number_from_string(string: str) -> int or float:
    """Extracts a number from a string, preserving the decimal point if present."""
    numeric_string = ""
    decimal_found = False

    for char in string:
        if char.isdigit():
            numeric_string += char
        elif char == "." and not decimal_found:
            numeric_string += char
            decimal_found = True

    if decimal_found:
        number = float(numeric_string)
    else:
        number = int(numeric_string)

    return number

def width_hight() ->tuple:

    # Get the file path from the command line argument
    gcode_file : str = sys.argv[1]
    # Open the file in read mode
    with open(gcode_file, "r") as file:
        lines = file.readlines()  # Read all lines of the file
        print(type(lines))
    # Count the occurrences of ";AFTER_LAYER_CHANGE"
    count: int = 0
    for i, line in enumerate(lines):
        if "perimeters extrusion width" in line:
            width : float = number_from_string(line)
        if ";HEIGHT" in line:
            count += 1
            if count == 2:
                height: float = number_from_string(line)
                return width, height

def line_width(gcode_file:str) -> float:
    '''Readin a line width from gcode'''

    # Open the file in read mode
    with open(gcode_file, "r") as file:
        lines:list = file.readlines()  # Read all lines of the file
    # Check the Slyser
        # Check the Slyser
        if "PrusaSlicer" in lines[0]:
            # Count the occurrences of ";AFTER_LAYER_CHANGE"
            for line in lines:
                if "; extrusion_width" in line:
                    width: float = number_from_string(line)
                    return width

        # Return "0"
        return 0



def layer_higth(gcode_file) -> float:
    '''Readin a line higth from gcode'''

    # Open the file in read mode
    with open(gcode_file, "r") as file:
        lines:list = file.readlines()  # Read all lines of the file
    # Check the Slyser
    if "PrusaSlicer" in lines[0]:
        # Count the occurrences
        count: int = 0

        for i, line in enumerate(lines):
            if ";HEIGHT" in line:
                count += 1
                if count == 2:
                    higth: float = number_from_string(line)
                    return higth

    # Return "0"
    return 0



