import sys
import time

def translate_sequence(in_file, out_file):
    aacode = {
        'A': "1", 'C': "2", 'D': "3", 'E': "4",
        'F': "5", 'G': "6", 'H': "7", 'I': "8",
        'K': "9", 'L': "10", 'M': "11", 'N': "12",
        'P': "13", 'Q': "14", 'R': "15", 'S': "16",
        'T': "17", 'V': "18", 'W':"19", 'Y':"20" 
    }

    with open(in_file, 'r') as infile, open(out_file, 'w') as outfile:
        for line in infile:
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

    # Example usage: python script.py input.txt output.txt
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    translate_sequence(in_file, out_file)

    end_time = time.time()  # End time
    print(f"Done. Execution time: {end_time - start_time:.2f} seconds.")