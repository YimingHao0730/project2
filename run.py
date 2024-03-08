import sys
import os
from datetime import datetime
import string
import glob
from tqdm import tqdm

# Function to get current time as a string
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def data_processing():
    os.system('python scripts/combine.py')
    os.system('python scripts/getorf.py')
    os.system('python scripts/format.py')
    print(f"{current_time()} - Data processing done")

# Function to predict using the Attention model
def Prediction_Attention():
    files = sorted(os.listdir("../../../panfs/y7hao/processed_data/"))
    for file in tqdm(files, desc="Processing files"):  # Wrap files with tqdm for a progress bar
        full_path = os.path.join("../../../panfs/y7hao/processed_data/", file)
        base_name = os.path.splitext(file)[0]
        file_size = os.path.getsize(full_path)
        
        if os.path.isfile(f'results/{base_name}.txt'):
            print(f"{current_time()} - Prediction Already done")
            continue

        elif file_size < 10240 * 1024 * 1024:  # File size less than 500MB
            print(f"{current_time()} - start direct prediction {file}")
            output_filename = f"../../../panfs/y7hao/results/probs_{base_name}.txt"
            command = f"python scripts/prediction_attention.py {full_path} {output_filename}"
            os.system(command)
            print(f"{current_time()} - end direct prediction {file}")
            # Process results regardless of whether the file was split.
            print(f"{current_time()} - result start {file}")
            os.system(f"python scripts/chunk.py ../../../panfs/y7hao/Data/{base_name}.fasta ../../../panfs/y7hao/results/probs_{base_name}.txt results/{base_name}.txt")
            # Deleting intermediate files and the original Data file.
            os.remove(f"../../../panfs/y7hao/results/probs_{base_name}.txt")  # Delete intermediate results file
            # Optionally delete results/preds_{base_name}.txt if it's considered intermediate
            print(f"{current_time()} - result end {file}")
        else:
            print(f"{current_time()} - File too large")
            continue
        
# Main execution point of the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{current_time()} - Usage: python run.py [pre-process/prediction/trimmed]")
        sys.exit(1)

    argument = sys.argv[1]
    if argument == "pre-process":
        data_processing()
    elif argument == "prediction":
        Prediction_Attention()
    else:
        print(f"{current_time()} - Invalid argument. Please choose 'pre-process' or 'prediction'.")


