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
    os.system('perl scripts/format1.pl --input Data/input2.fa')
    print(f'{current_time()} - format1 complete')
    os.system('perl scripts/format.pl Data/input2.fa none > processed_data/processed_data.txt')
    print(f"{current_time()} - Data processing done")

def data_processing():
    os.system('python scripts/getorf.py')
    os.system('perl scripts/format1.pl --input Data/input.fa')
    print(f'{current_time()} - format1 complete')
    os.system('perl scripts/format.pl Data/input.fa none > processed_data/processed_data.txt')
    print(f"{current_time()} - Data processing done")

# Function to predict using the Attention model
def Prediction_Attention():
    os.system('python scripts/prediction_attention.py processed_data/processed_data.txt  results/outcome_Attention.txt')
    print(f"{current_time()} - Prediction with Attention model complete")

# Main execution point of the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{current_time()} - Usage: python run.py [full/trimmed]")
        sys.exit(1)

    argument = sys.argv[1]

    if argument == "full":
        data_processing()
        Prediction_Attention()
    elif argument == "trimmed":
        trimming()
        Prediction_Attention()
    else:
        print(f"{current_time()} - Invalid argument. Please choose 'trimmed' or 'full'.")


