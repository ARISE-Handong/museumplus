import sys
import csv
import argparse
import os
import shutil

parser=argparse.ArgumentParser()
parser.add_argument('--mutToStmt_file', required=True)
parser.add_argument('--mutant_dir', required=True)
parser.add_argument('--targetStmts_file', required=True)
parser.add_argument('--output_file', required=True)

args=parser.parse_args()

target_stmts=list()
with open(args.targetStmts_file, 'r') as failing_stmts_f:
	for line in failing_stmts_f:
		target_stmts.append(line.strip())

mutsInStmt=dict()
all_muts=list()

used_mutants=list()
with open('used_mutants', 'r') as used_f:
	for line in used_f:
		line=line.strip()
		used_mutants.append(line)

with open(args.mutToStmt_file, 'r') as stmt_muts_f, open(args.output_file, 'w')as out_f:
	stmt_muts_f.readline()
	for line in stmt_muts_f:
		fileName, muts= line.split(':')
		if fileName in target_stmts:
			muts=muts.split(',')
			for mut in muts:
				if mut.strip() not in used_mutants:
					all_muts.append(mut.strip())
	if "24" in used_mutants and "24" in all_muts:
		print ("hi")
	print(len(all_muts))
	for mut in all_muts:
		out_f.write(mut+'\n')
	for filename in os.listdir(args.mutant_dir):
		if filename not in all_muts:
			print("deleting " +str(filename))
			shutil.rmtree(args.mutant_dir+'/'+filename)
