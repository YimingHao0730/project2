import sys
import time

def translate_sequence(in_file, out_file):
    aacode = {
        'A': "1", 'C': "2", 'D': "3", 'E': "4",
        'F': "5", 'G': "6", 'H': "7", 'I': "8",
        'K': "9", 'L': "10", 'M': "11", 'N': "12",
        'P': "13", 'Q': "14", 'R': "15", 'S': "16",
        'T': "17", 'V': "18", 'W': "19", 'Y': "20",
    }

    with open(in_file, 'r') as infile, open(out_file, 'w') as outfile:
        for line in infile:
            line = line.strip().upper()
            if line.startswith('>'):
                b = "0"
            else:
                # Skip invalid amino acids
                if any(x in line for x in ['B', 'J', 'O', 'U', 'X', 'Z']):
                    continue
                else:
                    seq = list(line)
                    b = "0," * (300 - len(seq) - 1) + ",".join([aacode[aa] for aa in seq if aa in aacode])
                    outfile.write(b + "\n")

if __name__ == "__main__":
    start_time = time.time()  # Start time

    # Example usage: python script.py input.txt output.txt
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    translate_sequence(in_file, out_file)

    end_time = time.time()  # End time
    print(f"Done. Execution time: {end_time - start_time:.2f} seconds.")

