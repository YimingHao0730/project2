import os
import glob
from datetime import datetime

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def Prediction_Attention(directory_path):
    files = sorted(os.listdir(directory_path))
    for file in files:
        full_path = os.path.join(directory_path, file)
        base_name = os.path.splitext(file)[0]

        print(f"{current_time()} - start splitting {file}")
        os.system(f'split -l $((`wc -l < "{full_path}"`/10)) "{full_path}" chunk/output_{base_name}_')
        os.remove(full_path)  # Delete the original file after splitting
        print(f"{current_time()} - splitting done {file}")

        for output_file in glob.glob(f'chunk/output_{base_name}_*'):
            output_filename = output_file.replace('output', 'processed_data')
            print(f"{current_time()} - start {output_file}")
            command = f"python scripts/prediction_attention.py {output_file} {output_filename}"
            os.system(command)
            print(f"{current_time()} - end {output_file}")
            os.remove(output_file)  # Delete output file after prediction

        print(f"{current_time()} - cat start {file}") 
        os.system(f"cat chunk/processed_data_{base_name}_* > results/probs_{base_name}.txt")
        for processed_file in glob.glob(f'chunk/processed_data_{base_name}_*'):
            os.remove(processed_file)  # Delete processed_data file after concatenation
        print(f"{current_time()} - cat end {file}")

        print(f"{current_time()} - result start {file}") 
        os.system(f"python scripts/chunk.py Data/{base_name}.fa results/probs_{base_name}.txt results/preds_{base_name}.txt")
        os.remove(f"Data/{base_name}.fa")  # Delete Data/{file}.fa
        os.remove(f"results/probs_{base_name}.txt")  # Delete results/probs.txt
        # Optionally delete results/preds_{base_name}.txt if needed
        print(f"{current_time()} - result end {file}")
