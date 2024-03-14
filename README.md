# Utilizing Deep Learning to Uncover Antimicrobial Peptides and Investigating their Associations with Diverse Diseases
As pathogens start to become more resistant to our current antibiotics, we
will soon need new antibiotics to fight various forms of bacteria. By 2050,
drug-resistant pathogens are expected to be the leading cause of death in the
world (O’Neill 2016). One way to create new antibiotics is to identify pep-
tides, sequences of amino acids, that have antimicrobial properties. These are
commonly known as antimicrobial peptides(AMP). These AMPs are known to
regulate inflammation, kill certain types of cancer cells, and fight various in-
fections and diseases. In this project, we use an Attention model to classify
peptides as AMPs or non-AMPs. We then run this model on a dataset called
FINRISK, which contains both DNA and health data on a randomly selected
group of Finnish people. Using the output of our model and the health data
in FINRISK, we performed a Pearson correlation test between having a spe-
cific AMP and having a disease listed in the FINRISK health data. We found
an average Pearson correlation coefficient of 0.5456 between having 4 pep-
tides and having COPD. We will be testing these peptides in the wet lab in
the coming weeks.

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
conda install cudatoolkit==11.2.2
conda install cudnn==8.8.0
```

### Building the project stages using `run.py`



* To process the data, from the root directory of the project, run `python run.py pre-process`
  - This script unzips the gz file, converts it to a fasta format, does six-frame-translation and gets the orfs, and get the data into Attention model-ready format.

  - To make sure that you can use multiprocessing to be time efficient, please run the following command:
  ```bash
  srun --mem 32g -N 1 -c 32 --time 14:00:00 --pty bash -l
  ```

  - please make sure that you are on `base` environment for pre-processing

* To gain access to gpu, open up a new terminal and login, then run this command
  ```bash
  srun --mem 100g -N 1 -c 32 --partition gpu --gres=gpu:1 --time 14:00:00 --pty bash -l
  ```
* To do prediction and extract the predicted AMPs, from the project root dir, run `python run.py prediction`
  - This divides the input file into 10 files(If the file is larger than 10GB), and run them separately through the model, it outputs a file which contains all the sequences that has been predicted AMPs.
  
  - Please make sure that you are on `capstone` environment for prediction

* The result will be exported into a txt file in the results folder of the __root directory of the project__

* The processed files are very large (~5TB)

* pre-process takes about `200` minutes

* prediction takes about `180` minutes

* Please notice that all of the finrisk data are protected and you will need certain permission to access, please change the __paths__ in the scripts if you wish to run on your account.

* To run correlation analysis and export the final results, run `python run.py result`, this is export the results in the folder __Final_results__


## Reference

Models and part of the scripts are provided by [Identification of antimicrobial peptides from the human gut microbiome using deep learning](https://www.nature.com/articles/s41587-022-01226-0)
