import sys
from Bio.Seq import Seq

def convert_fastq_to_custom_txt(fastq_file, output_file):
    with open(fastq_file, 'r') as f, open(output_file, 'w') as out:
        count = 0
        while True:
            identifier = f.readline().strip()
            if not identifier: break
            sequence = f.readline().strip()
            f.readline()  # Skip '+'
            f.readline()  # Skip quality score line

            # Ensure the sequence length is a multiple of three by trimming or padding
            remainder = len(sequence) % 3
            if remainder != 0:
                sequence = sequence[:-remainder]  # Trim the sequence

            # Translate the nucleotide sequence to amino acid sequence
            amino_acid_sequence = Seq(sequence).translate()

            # Remove asterisks representing stop codons
            amino_acid_sequence = amino_acid_sequence.replace("*", "")

            out.write(f"<{count}>\n")
            out.write(f"{amino_acid_sequence}\n")
            count += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python preprocess.py input.fastq output.txt")
        sys.exit(1)

    input_fastq = sys.argv[1]
    output_txt = sys.argv[2]
    
    convert_fastq_to_custom_txt(input_fastq, output_txt)


