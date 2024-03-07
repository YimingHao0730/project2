import os
import subprocess
from tqdm import tqdm

# Define the directory path
directory_path = "/panfs/dtmcdonald/human-depletion-non-tcga/pangenome-adapter-filter-12142-pese/12142/154499/"
output_directory = "/home/y7hao/project2/fasta_sequence_path/"

# Get a list of files in the directory sorted alphabetically
files = sorted(os.listdir(directory_path))

# Combine every two consecutive files
for i in tqdm(range(0, len(files), 2), desc="Combining files", unit=" pair"):
    r1_file = files[i]
    r2_file = files[i + 1]
    combined_file = f"{r1_file.split('_R1_')[0]}_{r1_file.split('_R1_')[1]}"
    
    # Check if the combined file already exists
    if not os.path.exists(os.path.join(output_directory, combined_file)):
        # Construct the command to combine files using subprocess
        command = f"cat '{os.path.join(directory_path, r1_file)}' '{os.path.join(directory_path, r2_file)}' > '{os.path.join(output_directory, combined_file)}'"
        subprocess.run(command, shell=True, check=True)

# Optionally, add logging statements to track progress
print("Combining files completed.")
