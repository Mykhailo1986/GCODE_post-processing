import sys
import subprocess

file_path = sys.argv[1]

def arc_weider():
    program_path = r"ArcWelder\bin\ArcWelder.exe"
    # Get the file path from the command line argument
    subprocess.run([program_path, file_path])

def arc_straightener():
    program_path = r"ArcWelder\bin\ArcStraightener.exe"
    # Get the file path from the command line argument
    subprocess.run([program_path, file_path])
