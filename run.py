import sys
import os
from datetime import datetime
import string

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
    print(f"{current_time()} - start spliting")
    os.system('split -l $((`wc -l < processed_data/processed_data.txt`/10)) processed_data/processed_data.txt chunk/output_')
    print(f"{current_time()} - spliting done")

    # Loop through each letter from 'aa' to 'aj'
    for letter1 in ['a']:  # First letter is always 'a' in this case
        for letter2 in string.ascii_lowercase[:10]:  # Loop through the first 10 letters of the alphabet
            input_filename = f"chunk/output_{letter1}{letter2}"
            output_filename = f"chunk/processed_data_{letter1}{letter2}"
            print(f"{current_time()} - start {input_filename}")
            command = f"python scripts/prediction_attention.py {input_filename} {output_filename}"
            os.system(command)
            print(f"{current_time()} - end {input_filename}")
            
        
    print(f"{current_time()} - cat start") 
    os.system("cat chunk/processed_data_aa chunk/processed_data_ab chunk/processed_data_ac chunk/processed_data_ad chunk/processed_data_ae chunk/processed_data_af chunk/processed_data_ag chunk/processed_data_ah chunk/processed_data_ai chunk/processed_data_aj > results/probs.txt")
    print(f"{current_time()} - cat end")

    print(f"{current_time()} - result start") 
    os.system("python scripts/chunk.py Data/input.fa results/probs.txt results/preds.txt")
    print(f"{current_time()} - result end")
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
        print(f"{current_time()} - Invalid argument. Please choose 'pre-process' or 'prediction' or 'trimmed'.")


