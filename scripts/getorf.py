import os
import subprocess
from datetime import datetime
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def process_file(filename):
    if filename.endswith(".fastq.gz"):
        fastq_name = filename
        fasta_name = f"{fastq_name.replace('.fastq.gz', '')}.fasta"
        decompressed_file = fastq_name.replace('.gz', '')

        decompression_cmd = f"gzip -d {os.path.join(fasta_sequence_path, fastq_name)}"
        subprocess.run(decompression_cmd, shell=True)
        print(f'{current_time()} - decompression completed')

        conversion_cmd = f"seqret -sequence {os.path.join(fasta_sequence_path, decompressed_file)} -outseq {os.path.join(fasta_sequence_path, fasta_name)}"
        subprocess.run(conversion_cmd, shell=True)
        print(f'{current_time()} - conversion completed')

        # Delete the original file after seqret
        os.remove(os.path.join(fasta_sequence_path, decompressed_file))
        print(f'{current_time()} - original file deleted after seqret')

        cmd = (
            f"getorf -sequence {os.path.join(fasta_sequence_path, fasta_name)} "
            f"-find 0 -table 11 -minsize 15 -maxsize 150 "
            f"-outseq {os.path.join(output_dir, fasta_name)}"
        )

        subprocess.run(cmd, shell=True)
        print(f'{current_time()} - getorf completed')

        # Delete the fasta file after getorf
        os.remove(os.path.join(fasta_sequence_path, fasta_name))
        print(f'{current_time()} - fasta file deleted after getorf')

if __name__ == "__main__":
    print(f'{current_time()} - start getOrf')

    fasta_sequence_path = "fasta_sequence_path"
    output_dir = "Data"
    files = os.listdir(fasta_sequence_path)

    # Create a multiprocessing Pool with the number of available CPU cores
    num_processes = min(cpu_count(), len(files))
    with Pool(num_processes) as pool:
        # Map the processing function to each file in parallel
        list(tqdm(pool.imap_unordered(process_file, files), total=len(files), desc="Processing files", unit=" file"))

    print(f'{current_time()} - getOrf completed')



