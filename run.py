import sys
import os
from datetime import datetime

# Function to get current time as a string
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function for processing the data
def trimming():
    os.system('python scripts/getorf.py')
    os.system('python scripts/trim.py Data/input.fa Data/input2.fa')
    os.system('python scripts/format.py Data/input2.fa processed_data/processed_data.txt')
    print(f"{current_time()} - Data processing done")

def data_processing():
    os.system('python scripts/getorf.py')
    os.system('python scripts/format.py Data/input.fa processed_data/processed_data.txt')
    print(f"{current_time()} - Data processing done")

# Function to predict using the Attention model
def Prediction_Attention():
    os.system('python scripts/prediction_attention.py processed_data/processed_data.txt  results/outcome_Attention.txt')
    print(f"{current_time()} - Prediction with Attention model complete")

# Main execution point of the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{current_time()} - Usage: python run.py [pre-process/prediction/trimmed]")
        sys.exit(1)

    argument = sys.argv[1]
    if argument == "pre-process":
        data_processing()
    elif argument == "trimmed":
        trimming()
    elif argument == "prediction":
        Prediction_Attention()
    else:
        print(f"{current_time()} - Invalid argument. Please choose 'pre-process' or 'prediction' or 'trimmed'.")


