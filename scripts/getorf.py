import os
import subprocess
from datetime import datetime
from tqdm import tqdm

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f'{current_time()} - start getOrf')

fasta_sequence_path = "fasta_sequence_path"
output_dir = "Data"

# Get the list of files in the fasta_sequence_path folder
files = os.listdir(fasta_sequence_path)

# Iterate over every file in the fasta_sequence_path folder
for filename in tqdm(files, desc="Processing files", unit=" file"):
    if filename.endswith(".fastq.gz"):
        fastq_name = filename
        fasta_name = f"{fastq_name.replace('.fastq.gz', '')}.fasta"
        decompressed_file = fastq_name.replace('.gz', '')

        decompression_cmd = f"gzip -d {os.path.join(fasta_sequence_path, fastq_name)}"
        subprocess.run(decompression_cmd, shell=True)

        conversion_cmd = f"seqret -sequence {os.path.join(fasta_sequence_path, decompressed_file)} -outseq {os.path.join(fasta_sequence_path, fasta_name)}"
        subprocess.run(conversion_cmd, shell=True)

        cmd = (
            f"getorf -sequence {os.path.join(fasta_sequence_path, fasta_name)} "
            f"-find 0 -table 11 -minsize 15 -maxsize 150 "
            f"-outseq {os.path.join(output_dir, fasta_name)}"
        )

        subprocess.run(cmd, shell=True)

print(f'{current_time()} - getOrf completed')

