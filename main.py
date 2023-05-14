import sys
from parser import parser

if len(sys.argv) < 2:
    print("Error")
    sys.exit(1)

filename = sys.argv[1]
#open file
try:
    with open(filename, "r") as file:
        for line in file:
            # delete blank
            line = line.strip()
            if line:
                result = parser.parse(line)
                if result:
                    # print information about money
                    if 'value' in result:
                        print(f"{result['value']} {result['unit']}")
                        if 'original_unit' in result and result['original_unit'] != result['unit']:
                            print(f"Converted from {result['original_unit']} to {result['unit']}")
                    else:
                        print("Error: Invalid expression")
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
