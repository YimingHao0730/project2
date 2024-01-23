import sys

def convert_fastq_to_custom_txt(fastq_file, output_file):
    with open(fastq_file, 'r') as f, open(output_file, 'w') as out:
        count = 0  # Starting number for sequences
        while True:
            identifier = f.readline().strip()
            if not identifier: break  # End of file
            sequence = f.readline().strip()
            f.readline()  # Skip '+'
            f.readline()  # Skip quality score line

            out.write(f">{count}\n")
            out.write(f"{sequence}\n")
            count += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python preprocess.py input.fastq output.txt")
        sys.exit(1)

    input_fastq = sys.argv[1]
    output_txt = sys.argv[2]
    
    convert_fastq_to_custom_txt(input_fastq, output_txt)
