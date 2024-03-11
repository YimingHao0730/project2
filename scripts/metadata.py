import pandas as pd
import os
from scipy.stats import pearsonr
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load the dataframe
metagenomics = pd.read_csv("../../../projects/capstone/finrisk-metadata/FR02_pheno.txt.gz", sep='\t')

output_directory = 'Final_results'

diseases = ['DIAB_T2', 'COPD', 'ASTHMA', 'HDL']

# Select relevant columns
metadata = metagenomics[['Barcode'] + diseases]

# Initialize a dictionary to hold AMP sequence counts for each sample
amp_sequences = {}

# Aggregate AMP sequences from files
folder_path = 'results/'
for filename in os.listdir(folder_path):
    if filename.endswith('.trimmed.txt'):
        sample_name = filename.split('_')[0]  # Extract sample name from the file name
        with open(os.path.join(folder_path, filename), 'r') as file:
            sequences = file.read().splitlines()
            sequence_counts = {}
            for seq in sequences:
                sequence_counts[seq] = sequence_counts.get(seq, 0) + 1
            amp_sequences[sample_name] = sequence_counts

# Convert AMP sequences dictionary to DataFrame and fill missing values with 0
df_amp = pd.DataFrame.from_dict(amp_sequences, orient='index').fillna(0).astype(int)

print(f'{current_time()} - df_amp completed')


metadata = metadata.dropna()

metadata = metadata.set_index("Barcode")

metagenomics = metadata.astype(int)

# Merge DataFrames
df_merged = metagenomics.join(df_amp, how='inner')

empty_col = [col for col in df_merged.columns if df_merged[col].sum() == 0]

df_merged = df_merged.drop(columns=empty_col)



print(f'{current_time()} - merge completed')

correlations = {disease: {} for disease in diseases}


# Iterate over health conditions for correlation analysis
for condition in tqdm(diseases):
    for column in tqdm(df_merged.columns[len(diseases):], desc=f'Condition: {condition}'):  
        correlation, _ = pearsonr(df_merged[column], df_merged[condition])
        correlations[condition][column] = correlation
            

print(f'{current_time()} - correlation completed')
            
# Define the threshold for strong association
threshold = 0.5  # You can adjust this threshold as needed

# Create a dictionary to store sequences with strong association for each condition
strong_associations = {disease: [] for disease in diseases}

# Iterate through the correlations dictionary
for condition, correlations_dict in correlations.items():
    for sequence, correlation in correlations_dict.items():
        # Check if correlation coefficient is above the threshold
        if abs(correlation) >= threshold:
            # Add the sequence to the list of strong associations for the current condition
            strong_associations[condition].append(sequence)
            
print(f'{current_time()} - strong associations completed')



# Convert dictionary to DataFrame for easier manipulation and visualization
df = pd.DataFrame(correlations).T  # Transpose to have diseases as rows and sequences as columns

df.fillna(0, inplace=True)  # Replace NaN with 0s for sequences not present in some diseases

# Since we have a lot of sequences, let's just visualize the data without sequence names
plt.figure(figsize=(20, 10))  # Adjust the size as needed

# Generate a heatmap without annotations and without sequence names
sns.heatmap(df, cmap="viridis", xticklabels=False, yticklabels=True)
plt.title('Correlation between AMP Sequences and Diseases')
plt.ylabel('Disease')
plt.xlabel('AMP Sequence Index')  # Indicating these are indices, not actual names

# Save the plot as an image
plot_path = "Final_results/heatmap_plot.png"  # Specify your desired path
plt.savefig(plot_path)

print(f'{current_time()} - plt completed')

# Prepare the string to write to the file
output_text = "Strong Associations:\n"
for disease, sequences in strong_associations.items():
    output_text += f"\n{disease}:\n"
    if sequences:  # Only if there are associated sequences
        output_text += "\n".join(sequences)
    else:
        output_text += "No strong associations."
    output_text += "\n"  # Add a newline for formatting

# Path where the text file will be saved
output_path = 'Final_results/strong_associations.txt'

# Write the output string to a text file
with open(output_path, 'w') as file:
    file.write(output_text)
    
print(f'{current_time()} - txt completed')
            






