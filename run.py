import sys
import os

# Function for processing the data

def trimming():
    # Trim the input file
    os.system('python scripts/trim.py Data/input.fa Data/input2.fa')
    # Preprocess the data into txt
    os.system('perl scripts/format1.pl --input Data/input2.fa')
    # Format the combined data
    os.system('perl scripts/format.pl Data/input2.fa none > processed_data/processed_data.txt')
    print("Data processing done")
def data_processing():
    # Preprocess the data into txt
    os.system('perl scripts/format1.pl --input Data/input.fa')
    # Format the combined data
    os.system('perl scripts/format.pl Data/input.fa none > processed_data/processed_data.txt')
    print("Data processing done")

# Function to predict using the Attention model
def Prediction_Attention():
    os.system('python scripts/prediction_attention.py processed_data/processed_data.txt  results/outcome_Attention.txt')
    print("Prediction with Attention model complete")


# Main execution point of the script
if __name__ == "__main__":
    # Check if the correct number of arguments is passed
    if len(sys.argv) != 2:
        print("Usage: python run.py [full/trimmed]")
        sys.exit(1)

    argument = sys.argv[1]

    # Process based on the argument
    if argument == "full":
        data_processing()
        Prediction_Attention()
    elif argument == "trimmed":
        trimming()
        Prediction_Attention()
    else:
        print("Invalid argument. Please choose 'data', 'prediction', 'all' or 'clean'.")

