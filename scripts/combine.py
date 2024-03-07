import os

# Define the directory path
directory_path = "/panfs/dtmcdonald/human-depletion-non-tcga/pangenome-adapter-filter-12142-pese/12142/154499/"

# Get a list of files in the directory sorted alphabetically
files = sorted(os.listdir(directory_path))

# Combine every two consecutive files
for i in range(0, len(files), 2):
    r1_file = files[i]
    r2_file = files[i + 1]
    combined_file = f"{r1_file.split('_R1_')[0]}_{r1_file.split('_R1_')[1]}"
    os.system(f"cat '{os.path.join(directory_path, r1_file)}' '{os.path.join(directory_path, r2_file)}' > /home/y7hao/project2/fasta_sequence_path/'{combined_file}'")
    print(f"Combined {r1_file} and {r2_file} into {combined_file}")

