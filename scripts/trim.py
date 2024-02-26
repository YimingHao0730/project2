import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Keep the first 10,000 sequences of a FASTA file.')
parser.add_argument('input_file', type=str, help='Input FASTA file path')
parser.add_argument('output_file', type=str, help='Output FASTA file path')

# Parse arguments
args = parser.parse_args()

count = 0
with open(args.input_file, 'r') as infile, open(args.output_file, 'w') as outfile:
    for line in infile:
        if line.startswith('>'):
            count += 1
            if count > 1000000:
                break
        outfile.write(line)
