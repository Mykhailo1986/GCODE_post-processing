import sys
from extrusion_width_hight import number_from_string

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
            if count == FAN_FROM and FAN_FROM != 0:
                lines.insert(i + 1, f"M106 S{FAN_POWER}   ; Turn on the fan at set speed\n")
                print(f"Tutn on the fun at {FAN_FROM} layer with {FAN_POWER} power.")
                if FAN_TILL == 0:
                    break
            if count == FAN_TILL :
                lines.insert(i + 1, "M106 S0   ; Turn off the fan \n")
                print(f"Tutn off the fun at {FAN_FROM} layer.")
                break  # Stop the loop after the occurrence
    # Write the modified lines back to the file
    with open(gcode_file, "w") as file:
        file.writelines(lines)

def error():
    print("Erorr\nExample: fan_layers_control.py <example.gcode> -f15 -p255 -s18")
    sys.exit()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        error()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'h' or sys.argv[1] == 'help':
            print("Add '-f' to set the fan layer begin.\n"
                  "Add '-p' to set the fan pawer(0-255).\n"
                  "Add '-s' to set the fan layer off.")
        if not ".gcode" in sys.argv[1]:
            error()

        FAN_FROM:int = 0
        FAN_POWER:int = 255,
        FAN_TILL:int = 0

        for argv in sys.argv:
            if "-f" in argv:
                FAN_FROM = number_from_string(argv)
            if "-s" in argv:
                FAN_TILL = number_from_string(argv)
            if "-p" in argv:
                FAN_POWER = number_from_string(argv)

        fan_on_off(gcode_file=sys.argv[1],
                   FAN_FROM=FAN_FROM,
                   FAN_POWER=FAN_POWER,
                   FAN_TILL=FAN_TILL)
    else:
        error()



