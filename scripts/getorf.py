import os
import subprocess

# Input file containing the names of the FASTA files
in_file = "fasta_sequence_names.txt"

# Open the input file and read each line
with open(in_file, "r") as file:
    for line in file:
        # Clean up the line to remove newline characters
        fasta_name = line.strip()

        # Construct the output file name
        out_name = f"{fasta_name}.fa"

        # Decompress the FASTA file
        decompressed_file = fasta_name.replace('.gz', '')

        decompression_cmd = f"gzip -d fasta_sequence_path/{fasta_name}"
        subprocess.run(decompression_cmd, shell=True)

        # Construct the command to run getorf
        cmd = (
            f"getorf -sequence fasta_sequence_path/{decompressed_file} "
            f"-find 0 -table 11 -minsize 15 -maxsize 150 "
            f"-outseq ../Data/{out_name}"
        )

        # Execute the command
        subprocess.run(cmd, shell=True)
        # Uncomment the line below to print the command instead of executing
        # print(cmd)

# Concatenate all the .fa files into one file called input.fa
output_dir = "../Data"
input_fa_path = os.path.join(output_dir, "input.fa")

cat_cmd = f"cat {output_dir}/*.fa > {input_fa_path}"
subprocess.run(cat_cmd, shell=True)
