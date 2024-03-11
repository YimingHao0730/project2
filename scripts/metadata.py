import pandas as pd
import os
from scipy.stats import pearsonr
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load the dataframe
metagenomics = pd.read_csv("../../../projects/capstone/finrisk-metadata/FR02_pheno.txt.gz", sep='\t')

output_directory = 'Final_results'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

diseases = ['DIAB_T2', 'COPD', 'ASTHMA', 'HDL']

# Select relevant columns
metadata = metagenomics[['Barcode'] + diseases].dropna()

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

metadata = metadata.set_index("Barcode")
metadata = metadata.astype(int)

# Merge DataFrames
df_merged = metadata.join(df_amp, how='inner')
df_merged.drop(columns=[col for col in df_merged.columns if df_merged[col].sum() == 0], inplace=True)

correlations = {disease: {} for disease in diseases}

# Iterate over health conditions for correlation analysis
for condition in diseases:
    for column in df_merged.columns[len(diseases):]:  
        correlation, p_value = pearsonr(df_merged[column], df_merged[condition])
        correlations[condition][column] = {'correlation': correlation, 'p_value': p_value}

# Define the threshold for strong association
threshold = 0.5  # Adjust this threshold as needed

# Create a dictionary to store sequences with strong association for each condition
strong_associations = {disease: [] for disease in diseases}

# Iterate through the correlations dictionary
for condition, seq_data in correlations.items():
    for sequence, data in seq_data.items():
        if abs(data['correlation']) >= threshold:
            strong_associations[condition].append(sequence)

# Create a list of dictionaries for DataFrame creation
data_for_df = []
for disease, seq_data in correlations.items():
    for sequence, data in seq_data.items():
        row = {'Disease': disease, 'Sequence': sequence, 'Correlation': data['correlation'], 'P-Value': data['p_value']}
        data_for_df.append(row)

# Create DataFrame and set index
df_correlations = pd.DataFrame(data_for_df)
df_correlations.set_index(['Disease', 'Sequence'], inplace=True)

# Prepare the string to write to the file including correlation coefficients and p-values
output_text = "Associations (Correlation and P-Values):\n"
for disease, sequences in strong_associations.items():
    output_text += f"\n{disease}:\n"
    for sequence in sequences:
        correlation = correlations[disease][sequence]['correlation']
        p_value = correlations[disease][sequence]['p_value']
        output_text += f"{sequence}: Correlation = {correlation:.4f}, P-value = {p_value:.4g}\n"

# Write the output string to a text file
output_path = os.path.join(output_directory, 'strong_associations_with_p_values.txt')
with open(output_path, 'w') as file:
    file.write(output_text)

# Print completion message
print(f'{current_time()} - Analysis completed. Results saved to {output_path}')

            






