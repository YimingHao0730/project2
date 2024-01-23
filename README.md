# AMPs-prediction

__Identification of antimicrobial peptides from the human gut microbiome using deep learning__

Welcome to our project focused on identifying Antimicrobial Peptides (AMPs) from the human gut microbiome using state-of-the-art deep learning techniques. In the wake of increasing antibiotic resistance, our aim is to accelerate the discovery of new AMP candidates by applying an ensemble of advanced NLP models — LSTM, BERT, and Attention —, and also its combinations to analyze metagenomic and metaproteomic data. This approach represents a significant advancement over traditional methods, enabling us to explore a high-dimensional space of peptide sequences and uncover potential AMPs that were previously undetectable. Our dataset comprises both known AMPs and non-AMPs.[Dataset](https://github.com/mayuefine/c_AMPs-prediction/tree/master/Data), providing a robust foundation for training our models. Join us in this innovative venture to develop more effective strategies against antibiotic-resistant pathogens.

# DSMLP Workflow

## Retrieving the Bert Model locally:

(1) download the Bert Model from https://www.dropbox.com/sh/o58xdznyi6ulyc6/AABLckEnxP54j2X7BrGybhyea?dl=0\

(2) put bert.bin in the __Models__ folder

## Running the project

### Initlize environment
The required python version is 3.9, so please make sure you have __python3.9__ before proceeding.

To create the environment, run the following command from the `root directory of the project`.
```bash
python -m venv amp_prediction
source amp_prediction/bin/activate
```

Right now you should have a folder called __amp_prediction__ in your root directory of the project

### Installation of dependencies
To install dependencies, run the following command from the same terminal
```bash
pip install -r requirements.txt
```
### Installation bert_sklearn

copy the __bert_sklearn__ folder to __amp_prediction/lib/python3.9/site-packages__ folder, and then run the following command from the same terminal
```bash
cd amp_prediction/lib/python3.9/site-packages/bert_sklearn
pip install .
cd ../../../..
```

### Building the project stages using `run.py`

* To process the data, from the same terminal, run `python run.py data`
  - This combines the amp and non-amp data and saves the processed data in processed_data folder.
* To do prediction and evaluate the performance of the models, from the project root dir, run `python run.py prediction`
  - This loads the processed data into three individual models (Attention, LSTM and Bert) and completes the prediction. Save the results and integrates them, and outputs the model's performance statistic as a html page in the project root dir.
* Use `python run.py all` to complete all steps above

*The result will be exported into a html file in the __root directory of the project__

* This step takes `10-15` minutes

* Whenever you want to open a __new terminal__ and run the project, make sure to activate the environment by running the follow command from __root directory of the project__:
```bash
source amp_prediction/bin/activate
```
## Reference

Models, bert-sklearn and part of the scripts are provided by [Identification of antimicrobial peptides from the human gut microbiome using deep learning](https://www.nature.com/articles/s41587-022-01226-0)
