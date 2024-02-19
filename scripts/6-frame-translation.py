import skbio
import os
from skbio import DNA

example_fastq = '/qmounts/qiita_data/per_sample_FASTQ/121153/SAMN08010247.SRR6323500.R2.ebi.fastq.gz'

smallest_AA_size = 4

if not os.path.exists(example_fastq):
    raise ValueError()

some_fastq_data = skbio.read(example_fastq, format='fastq', phred_offset=33)


#Gets all the 6 frame translations from the first n items in fast_q_data file
#Returns them in a list.
#Removes all items that are smaller than smallest amino acid in training data set.
def get_subset_translations(n = 100000):
        all_dna = []
        counter = 0
        for record in some_fastq_data:
                all_dna.append(str(record))
                counter+=1
                if counter==n:
                        break

        results = []
        for record in all_dna[:n]:
                cur_dna = DNA(record)
                for i in range(6):
                        cur_translation = str(next(cur_dna.translate_six_frames())).split('*')
                        for t in cur_translation:
                                if len(t)>=smallest_AA_size:
                                        results.append(t)
        return results

results_1k = get_subset_translations(1000)
#print(f'length of results_100k: {len(results_100k)}')
with open('results_1k.txt', 'w') as file:
	file.write('\n'.join(results_1k))


#Gets all the 6 frame translations from all the DNA sequences in the fast_q_data file
#Returns them in a list.
#Removes all items that are smaller than smallest amino acid in training data set.
#hasn't been tested yet
def gets_all_translations():
        all_results = []
        for record in some_fastq_data:
                cur_dna = DNA(record)
                for i in range(6):
                        cur_translation = str(next(cur_dna.translate_six_frames())).split('*')
                        for t in cur_translation:
                                if len(t)>=smallest_AA_size:
                                        all_results.append(t)
        return all_results

all_results = gets_all_translations()
with open('all_results.txt', 'w') as file:
        file.write('\n'.join(all_results))
