import os
import subprocess
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# Define the directory path
directory_path = "/panfs/dtmcdonald/human-depletion-non-tcga/pangenome-adapter-filter-12142-pese/12142/154499/"
output_directory = "/home/y7hao/project2/fasta_sequence_path/"

# Get a list of files in the directory sorted alphabetically
files = sorted(os.listdir(directory_path))

# Function to combine files
def combine_files(file_pair):
    r1_file, r2_file = file_pair
    combined_file = f"{r1_file.split('_R1_')[0]}_{r1_file.split('_R1_')[1]}"
    combined_file_path = os.path.join(output_directory, combined_file)
    
    # Check if the combined file already exists
    if not os.path.exists(combined_file_path):
        # Construct the command to combine files using subprocess
        command = f"cat '{os.path.join(directory_path, r1_file)}' '{os.path.join(directory_path, r2_file)}' > '{combined_file_path}'"
        subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    # Create a multiprocessing Pool with the number of available CPU cores
    num_processes = min(cpu_count(), len(files))
    with Pool(num_processes) as pool:
        # Map the combine_files function to each file pair in parallel
        list(tqdm(pool.imap_unordered(combine_files, zip(files[::2], files[1::2])), total=len(files)//2, desc="Combining files", unit=" pair"))

    print("Combining files completed.")

