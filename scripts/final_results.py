import pandas as pd
from sklearn.metrics import precision_score, recall_score, confusion_matrix, precision_recall_curve, auc

# Read the CSV file
df = pd.read_csv('results/combined_outcome.csv', sep='\t')

# Add the 'actual' column
df['actual'] = [1 if i < 1085 else 0 for i in range(len(df))]

# Define models with their respective prediction and probability columns
models = {
    'Attention+LSTM+Bert': ('prediction', 'probability'),
    'Attention': ('att_prediction', 'att_prob'),
    'LSTM': ('lstm_prediction', 'lstm_prob'),
    'Bert': ('bert_prediction', 'bert_prob')
}

# Start HTML table
html = """
<html>
<head><title>Sequences ≤ 50 AAs</title></head>
<body>
    <table border="1">
        <tr>
            <th>Models</th>
            <th>TP</th>
            <th>FP</th>
            <th>TN</th>
            <th>FN</th>
            <th>AUPRC</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>FNR</th>
        </tr>
"""

# Loop through each model and calculate metrics
for model, (prediction_col, prob_col) in models.items():
    # Calculate TP, FP, TN, FN
    tp = sum((df[prediction_col] == 1) & (df['actual'] == 1))
    fp = sum((df[prediction_col] == 1) & (df['actual'] == 0))
    tn = sum((df[prediction_col] == 0) & (df['actual'] == 0))
    fn = sum((df[prediction_col] == 0) & (df['actual'] == 1))

    # Calculate AUPRC, Precision, Recall, FNR
    precision = precision_score(df['actual'], df[prediction_col])
    recall = recall_score(df['actual'], df[prediction_col])
    fnr = fn / (fn + tp)
    precision_curve, recall_curve, _ = precision_recall_curve(df['actual'], df[prob_col])
    auprc = auc(recall_curve, precision_curve)

    # Append to HTML
    html += f"""
        <tr>
            <td>{model}</td>
            <td>{tp}</td>
            <td>{fp}</td>
            <td>{tn}</td>
            <td>{fn}</td>
            <td>{auprc:.4f}</td>
            <td>{precision:.4f}</td>
            <td>{recall:.4f}</td>
            <td>{fnr:.4f}</td>
        </tr>
    """

# Close HTML table
html += """
    </table>
</body>
</html>
"""

# Write to HTML file
with open('final_results.html', 'w') as file:
    file.write(html)
