
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--used-muts', required=True)
parser.add_argument('--target-tcs', required=True)
parser.add_argument('--mutant-out', required=True)

args = parser.parse_args()
with open(args.used_muts, 'r', encoding='utf-8') as used_mut_f:
	used_mutants=used_mut_f.read().splitlines()

with open(args.target_tcs, 'r', encoding='utf-8') as tc_f:
	all_tcs = tc_f.read().splitlines()

mutants_out=dict()
with open(args.mutant_out,'r', encoding='utf-8') as mut_out_f:
	for mut_out in mut_out_f:
		tc=mut_out.strip().split(',')[0]
		mut_id = mut_out.strip().split(',')[1]
		if mut_id not in mutants_out.keys():
			mutants_out[mut_id]=[tc]
		else:
		 	mutants_out[mut_id].append(tc)
missing_runs_file = open("missing_runs",'w')
for mut in used_mutants:
	if mut in mutants_out and len(mutants_out[mut])!=len(all_tcs):
		for tc in all_tcs:
			if tc not in mutants_out[mut]:
				missing_runs_file.write(mut+','+tc+'\n')	
		
missing_runs_file.close()
