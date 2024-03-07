import os
import time
from tqdm import tqdm

def translate_sequence(in_file, out_file):
    aacode = {
        'A': "1", 'C': "2", 'D': "3", 'E': "4",
        'F': "5", 'G': "6", 'H': "7", 'I': "8",
        'K': "9", 'L': "10", 'M': "11", 'N': "12",
        'P': "13", 'Q': "14", 'R': "15", 'S': "16",
        'T': "17", 'V': "18", 'W':"19", 'Y':"20" 
    }

    with open(in_file, 'r') as infile, open(out_file, 'w') as outfile:
        for line in tqdm(infile, desc="Translating", unit=" line"):
            line = line.strip().upper()
            if line.startswith('>'):
                continue  # Skip further processing for header lines
            else:
                # Generate sequence encoding
                encoded_seq = ",".join([aacode[aa] for aa in line if aa in aacode])
                # Calculate how much padding is needed
                padding_needed = 300 - len(encoded_seq.split(','))
                # Prepend the padding
                b = "0," * padding_needed + encoded_seq
                # Write the padded sequence to the outfile
                outfile.write(b + "\n")

if __name__ == "__main__":
    start_time = time.time()  # Start time

    input_dir = "Data"
    output_dir = "processed_data"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over every file in the Data directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".fasta"):
            in_file = os.path.join(input_dir, filename)
            out_file = os.path.join(output_dir, filename)
            translate_sequence(in_file, out_file)

    end_time = time.time()  # End time
    print(f"Done. Execution time: {end_time - start_time:.2f} seconds.")

