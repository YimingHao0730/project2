
# Barnacle2 Workflow

## Setting up conda environment:
### Only required if you do not have a conda environment set up already.

(1) After signing in to Barnacle2, run these commands:
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

(2)
run
```bash
vi ~/.bash_profile
```
then press i to enter insert mode, and paste the following code
```bash
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```
hit esc, type":wq" to save and exit file

(3) finally, run
```bash
source ~/.bash_profile
```
### Now you have a working conda environment on barnacle2.

## Input file

(1) This workflow is designed to process one file at a time, once you decided which file you want to use as input, move it to _~\project2\fasta_sequence_path_, __for example__:
```bash
cp '/qmounts/qiita_data/per_sample_FASTQ/121153/SAMN08010247.SRR6323500.R2.ebi.fastq.gz' /home/y7hao/project2/fasta_sequence_path/
```
replace the file name with your desired file and the path with your project2 folder path.

(2) run
```bash
vi fasta_sequence_names.txt
```
press i and enter the input file name, for example, "SAMN08010247.SRR6323500.R2.ebi.fastq.gz"

press esc and type ":wq" to save and exit file


## Running the project

### Initlize environment

To create the environment, run the following command from the `root directory of the project`.
```bash
conda -m venv capstone python==3.8
conda activate capstone
```

### Installation of dependencies
To install dependencies, run the following command from the same terminal
```bash
pip install -r requirements.txt
```
(Have to use conda to install cudatoolkit)

### Building the project stages using `run.py`

* To gain access to gpu, run this command
```bash
srun --mem 100g -N 1 -c 1 --partition gpu --gres=gpu:1 --time 5:00:00 --pty bash -l
```

* To process the data, from the root directory of the project, run `python run.py pre-process`
  - This script unzips the gz file, converts it to a fasta format, does six-frame-translation and gets the orfs, and get the data into Attention model-ready format.

  - please make sure that you are on `base` environment for pre-processing
* To do prediction and extract the predicted AMPs, from the project root dir, run `python run.py prediction`
  - This divides the input file into 10 files, and run them separately through the model, it outputs a file which contains all the sequences that has been predicted AMPs.
  
  - Please make sure that you are on `capstone` environment for prediction

*The result will be exported into a txt file in the results folder of the __root directory of the project__

* pre-process takes about `30` minutes

* prediction takes about `120` minutes

## Reference

Models and part of the scripts are provided by [Identification of antimicrobial peptides from the human gut microbiome using deep learning](https://www.nature.com/articles/s41587-022-01226-0)
