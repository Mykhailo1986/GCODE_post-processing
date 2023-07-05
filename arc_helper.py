import subprocess
def arc_weider(gcode_file):
    '''Run ArcWeider.exe'''
    program_path = r"ArcWelder\bin\ArcWelder.exe"
    # Get the file path from the command line argument
    subprocess.run([program_path, gcode_file])

def arc_straightener(gcode_file):
    '''Run ArcStraiter.exe'''
    program_path = r"ArcWelder\bin\ArcStraightener.exe"
    # Get the file path from the command line argument
    subprocess.run([program_path, gcode_file])
