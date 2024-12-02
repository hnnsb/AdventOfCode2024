import sys 

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][:2] + ".in") as file:
    data = file.readlines()