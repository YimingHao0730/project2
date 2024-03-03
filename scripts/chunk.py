import sys

# Check if the correct number of arguments is provided (4 arguments: script name, sequences file path, floats file path, output file path)
if len(sys.argv) != 4:
    print("Usage: script.py sequences_file_path floats_file_path output_file_path")
    sys.exit(1)

# Assign command-line arguments to variables
sequences_file_path = sys.argv[1]
floats_file_path = sys.argv[2]
output_file_path = sys.argv[3]  # The output file path is now provided as an argument

# Process files and write to the specified output file
with open(sequences_file_path, 'r') as sequences_file, open(floats_file_path, 'r') as floats_file, open(output_file_path, 'w') as output_file:
    for sequence_line, float_line in zip(sequences_file, floats_file):
        if float(float_line.strip()) > 0.999999:
            output_file.write(sequence_line)

