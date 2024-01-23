import sys
import os

# Function for processing the data
def data_processing():
    # Check if the processed data file exists
    if not os.path.exists('processed_data/processed.txt'):
        # Preprocess the data into txt
        os.system('python preprocess.py input.fastq output.txt')
        # Format the combined data
        os.system('perl scripts/format.pl processed_data/output.txt none > processed_data/processed_data.txt')
    print("Data processing done")

# Function to predict using the Attention model
def Prediction_Attention():
    # Check if the Attention model's result file exists
    if not os.path.exists("results/outcome_Attention.txt"):
        # Run the Attention model prediction script
        os.system('python scripts/prediction_attention.py processed_data/processed_data.txt  results/outcome_Attention.txt')
    print("Prediction with Attention model complete")

# Function to predict using the LSTM model
def Prediction_LSTM():
    # Check if the LSTM model's result file exists
    if not os.path.exists("results/outcome_LSTM.txt"):
        # Run the LSTM model prediction script
        os.system('python scripts/prediction_lstm.py processed_data/processed_data.txt  results/outcome_LSTM.txt')
    print("Prediction with LSTM model complete")

# Function to predict using the Bert model
def Prediction_Bert():
    # Check if the Bert model's result file exists
    if not os.path.exists("results/outcome_Bert.txt"):
        # Run the Bert model prediction script
        os.system('python scripts/prediction_bert.py processed_data/combined.txt  results/outcome_Bert.txt')
    print("Prediction with Bert model complete")

# Function to integrate results from all models
def Result_integration():
    # Combine results from all models and generate a final outcome
    os.system('python scripts/result.py results/outcome_Attention.txt results/outcome_LSTM.txt results/outcome_Bert.txt processed_data/combined.txt results/combined_outcome.csv')
    # Process the final results
    os.system('python scripts/final_results.py')
    print('result integration complete')

# Main execution point of the script
if __name__ == "__main__":
    # Check if the correct number of arguments is passed
    if len(sys.argv) != 2:
        print("Usage: python run.py [data/prediction/all/clean]")
        sys.exit(1)

    argument = sys.argv[1]

    # Process based on the argument
    if argument == "data":
        data_processing()
    elif argument == "prediction":
        # Check if processed data exists before making predictions
        if not os.path.exists("processed_data/processed_data.txt"):
            raise FileNotFoundError("No processed data. Please run 'python run.py data' first.")
        else:
            Prediction_Attention()
            Prediction_LSTM()
            Prediction_Bert()
            Result_integration()
    elif argument == "all":
        # Run all steps: data processing, prediction, and result integration
        data_processing()
        Prediction_Attention()
        Prediction_LSTM()
        Prediction_Bert()
        Result_integration()
    else:
        print("Invalid argument. Please choose 'data', 'prediction', 'all' or 'clean'.")

