import skbio
import os
from skbio import DNA
import time
import cProfile

example_fastq = '/qmounts/qiita_data/per_sample_FASTQ/121153/SAMN08010247.SRR6323500.R2.ebi.fastq.gz'

smallest_AA_size = 4

if not os.path.exists(example_fastq):                                           
    raise ValueError()      

some_fastq_data = skbio.read(example_fastq, format='fastq', phred_offset=33)


#Gets all the 6 frame translations from the first n items in fast_q_data file
#Returns them in a list.
#Removes all items that are smaller than smallest amino acid in training data set.
def get_subset_translations_list(n = 100000):
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

with open('summaryOfSpeeds.txt', 'w') as file:
	pass
start_time = time.time()
results_subset = get_subset_translations_list(100000)
print(f'length of results_100k_list: {len(results_subset)}')
end_time = time.time()
print(f"Execution time for results_subset_list: {end_time-start_time} seconds")
with open('summaryOfSpeeds.txt', 'a') as file:
	file.write(f"Execution time for results_subset_list: {end_time-start_time} seconds\n")

cProfile.run("get_subset_translations_list(1000)", "translations_list.pstats")

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

#start_time = time.time()
#all_results = gets_all_translations()
#print(f'length of all_results: {len(all_results)}')
#end_time = time.time()
#print(f"Execution time for all_results: {end_time-start_time} seconds")

def get_first_n_dna_seq(n=10000):
	all_dna = []
	counter = 0
	for record in some_fastq_data:
		all_dna.append(str(record))
		counter+=1
		if counter==n:
			break
	return all_dna

start_time = time.time()
first100k_dna = get_first_n_dna_seq(100000)
#print(f'length of results_100k_list_print: {len(results_subset)}')
end_time = time.time()
print(f"Execution time for get_first_n_dna_seq: {end_time-start_time} seconds")
with open('summaryOfSpeeds.txt', 'a') as file:
        file.write(f"Execution time for get_first_n_dna_seq: {end_time-start_time} seconds\n")


def get_subset_translations_print(n = 10000):
	all_dna = []
	counter = 0
	for record in some_fastq_data:
		all_dna.append(str(record))
		counter+=1
		if counter==n:
			break

	for record in all_dna[:n]:
		cur_dna = DNA(record)
		for i in range(6):
			cur_translation = str(next(cur_dna.translate_six_frames())).split('*')
			for t in cur_translation:
				if len(t)>=smallest_AA_size:
					print(t)

start_time = time.time()
results_subset = get_subset_translations_print(100000)
#print(f'length of results_100k_list_print: {len(results_subset)}')
end_time = time.time()
print(f"Execution time for results_subset_print: {end_time-start_time} seconds")
with open('summaryOfSpeeds.txt', 'a') as file:
        file.write(f"Execution time for results_subset_print: {end_time-start_time} seconds\n")


def gets_all_translations_txt():
	for record in some_fastq_data:
		cur_dna = DNA(record)
		for i in range(6):
			cur_translation = str(next(cur_dna.translate_six_frames())).split('*')
			for t in cur_translation:
				if len(t)>=smallest_AA_size:
					with open('output1.txt', 'a') as file:
						file.write(t)

