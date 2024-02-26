import os
import subprocess

print('start getOrf')
# Input file containing the names of the FASTQ files
in_file = "fasta_sequence_names.txt"

# Open the input file and read each line
with open(in_file, "r") as file:
    for line in file:
        # Clean up the line to remove newline characters
        fastq_name = line.strip()

        # Construct the output file name
        fasta_name = f"{fastq_name.replace('.fastq.gz', '')}.fasta"
        
        decompressed_file = fastq_name.replace('.gz', '')

        # Decompress the FASTQ file
        decompression_cmd = f"gzip -d fasta_sequence_path/{fastq_name}"
        subprocess.run(decompression_cmd, shell=True)
        
        print('decompress completed')

        # Convert FASTQ to FASTA using EMBOSS
        conversion_cmd = f"seqret -sequence fasta_sequence_path/{decompressed_file} -outseq fasta_sequence_path/{fasta_name}"
        subprocess.run(conversion_cmd, shell=True)
        
        print('conversion completed')

        # Construct the command to run getorf
        cmd = (
            f"getorf -sequence fasta_sequence_path/{fasta_name} "
            f"-find 0 -table 11 -minsize 15 -maxsize 150 "
            f"-outseq Data/{fasta_name}"
        )
        

        # Execute the command
        subprocess.run(cmd, shell=True)
        print('getorf completed')
        # Uncomment the line below to print the command instead of executing
        # print(cmd)

# Concatenate all the .fasta files into one file called input.fa
output_dir = "../Data"
input_fa_path = os.path.join(output_dir, "input.fa")

cat_cmd = f"cat {output_dir}/*.fasta > {input_fa_path}"
subprocess.run(cat_cmd, shell=True)
print('cat completed')

