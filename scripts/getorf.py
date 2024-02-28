import os
import subprocess
from datetime import datetime

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f'{current_time()} - start getOrf')

in_file = "fasta_sequence_names.txt"

with open(in_file, "r") as file:
    for line in file:
        fastq_name = line.strip()
        fasta_name = f"{fastq_name.replace('.fastq.gz', '')}.fasta"
        decompressed_file = fastq_name.replace('.gz', '')

        if os.path.exists(os.path.join("Data", fasta_name)):
            print(f'{current_time()} - getorf already done')
            continue

        decompression_cmd = f"gzip -d fasta_sequence_path/{fastq_name}"
        subprocess.run(decompression_cmd, shell=True)
        
        print(f'{current_time()} - decompress completed')

        conversion_cmd = f"seqret -sequence fasta_sequence_path/{decompressed_file} -outseq fasta_sequence_path/{fasta_name}"
        subprocess.run(conversion_cmd, shell=True)
        
        print(f'{current_time()} - conversion completed')

        cmd = (
            f"getorf -sequence fasta_sequence_path/{fasta_name} "
            f"-find 0 -table 11 -minsize 15 -maxsize 150 "
            f"-outseq Data/{fasta_name}"
        )
        
        subprocess.run(cmd, shell=True)
        print(f'{current_time()} - getorf completed')

output_dir = "Data"
input_fa_path = os.path.join(output_dir, "input.fa")

cat_cmd = f"cat {output_dir}/*.fasta > {input_fa_path}"
subprocess.run(cat_cmd, shell=True)
print(f'{current_time()} - cat completed')

