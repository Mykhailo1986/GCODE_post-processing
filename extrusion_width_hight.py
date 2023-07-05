import sys

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
    file_path = sys.argv[1]
    # Open the file in read mode
    with open(file_path, "r") as file:
        lines = file.readlines()  # Read all lines of the file
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


