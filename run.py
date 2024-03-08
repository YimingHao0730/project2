import sys
import os
from datetime import datetime
import string
import glob

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
    for file in files:
        full_path = os.path.join("../../../panfs/y7hao/processed_data/", file)
        base_name = os.path.splitext(file)[0]
        file_size = os.path.getsize(full_path)

        if file_size < 10240 * 1024 * 1024:  # File size less than 500MB
            print(f"{current_time()} - start direct prediction {file}")
            output_filename = f"../../../panfs/y7hao/results/probs_{base_name}.txt"
            command = f"python scripts/prediction_attention.py {full_path} {output_filename}"
            os.system(command)
            print(f"{current_time()} - end direct prediction {file}")
        else:
            print(f"{current_time()} - start splitting {file}")
            os.system(f'split -l $((`wc -l < "{full_path}"`/10)) "{full_path}" ../../../panfs/y7hao/chunk/output_{base_name}_')
            print(f"{current_time()} - splitting done {file}")
            

            for output_file in glob.glob(f'../../../panfs/y7hao/chunk/output_{base_name}_*'):
                output_filename = output_file.replace('output', 'processed_data')
                print(f"{current_time()} - start {output_file}")
                command = f"python scripts/prediction_attention.py {output_file} {output_filename}"
                os.system(command)
                print(f"{current_time()} - end {output_file}")
                os.remove(output_file)  # Delete output file after prediction

            print(f"{current_time()} - cat start {file}")
            os.system(f"cat ../../../panfs/y7hao/chunk/processed_data_{base_name}_* > ../../../panfs/y7hao/results/probs_{base_name}.txt")
            for processed_file in glob.glob(f'panfs/y7hao/chunk/processed_data_{base_name}_*'):
                os.remove(processed_file)  # Delete processed_data file after concatenation
            print(f"{current_time()} - cat end {file}")

        # Process results regardless of whether the file was split.
        print(f"{current_time()} - result start {file}")
        os.system(f"python scripts/chunk.py ../../../panfs/y7hao/Data/{base_name}.fasta ../../../panfs/y7hao/results/probs_{base_name}.txt results/{base_name}.txt")
        # Deleting intermediate files and the original Data file.
        os.remove(f"../../../panfs/y7hao/results/probs_{base_name}.txt")  # Delete intermediate results file
        # Optionally delete results/preds_{base_name}.txt if it's considered intermediate
        print(f"{current_time()} - result end {file}")
        
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


