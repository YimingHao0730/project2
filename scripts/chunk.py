import sys

# Check if the correct number of arguments is provided (4 arguments: script name, sequences file path, floats file path, output file path)
if len(sys.argv) != 4:
    print("Usage: script.py sequences_file_path floats_file_path output_file_path")
    sys.exit(1)

# Assign command-line arguments to variables
sequences_file_path = sys.argv[1]
floats_file_path = sys.argv[2]
output_file_path = sys.argv[3]

# Process files and write to the specified output file
with open(sequences_file_path, 'r') as sequences_file, open(floats_file_path, 'r') as floats_file, open(output_file_path, 'w') as output_file:
    while True:
        metadata_line = sequences_file.readline()  # Read metadata line but don't use it
        sequence_line = sequences_file.readline()  # Read sequence line
        float_line = floats_file.readline()  # Read float line

        if not sequence_line or not float_line:  # Break the loop if either file ends
            break

        if float(float_line.strip()) > 0.999999:
            output_file.write(sequence_line)  # Write only sequence line


