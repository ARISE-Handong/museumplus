import csv
import sys
import argparse


if __name__=='__main__':
	parser= argparse.ArgumentParser()
	parser.add_argument('--mutlog_file', required=True)
	parser.add_argument('--output_file', required=True)

	args=parser.parse_args()

	mutInStmt=dict()
	with open(args.mutlog_file, 'r') as log_file:
		for line in log_file:
			line= line.split(':')
			if '@' in line[4]:
				fileName,_=line[4].split('@')
			else:
				fileName=line[4]
			if fileName+"#"+line[5] in mutInStmt:
				mutInStmt[fileName+"#"+line[5]].append(line[0])
			else:
				mutInStmt[fileName+"#"+line[5]]=[line[0]]
	
	with open(args.output_file, 'w') as out_file:
		writer=csv.DictWriter(out_file, ['Statement', 'Mutants'], delimiter=':')
		writer.writeheader()
		for stmt, mutants in mutInStmt.items():
			mutants=','.join(mutants)
			writer.writerow({'Statement': stmt, 'Mutants':mutants})

