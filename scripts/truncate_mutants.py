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
with open(args.mutToStmt_file, 'r') as stmt_muts_f, open(args.output_file, 'w')as out_f:
	stmt_muts_f.readline()
	for line in stmt_muts_f:
		fileName, muts= line.split(':')
		if fileName in target_stmts:
			muts=muts.split(',')
			for mut in muts:
				all_muts.append(mut.strip())
	for mut in all_muts:
		out_f.write(mut+'\n')
	for filename in os.listdir(args.mutant_dir):
		if filename not in all_muts:
			shutil.rmtree(args.mutant_dir+'/'+filename)
