import csv
import argparse

def ochiai_formula(passed, failed, totalpassed, totalfailed):
	return failed/(totalfailed*(failed+passed)+1)**0.5

def op2_formula(passed, failed, totalpassed,totalfailed):
	return failed-(passed/(totalpassed+1))

def dstar_formula(passed, failed, totalpassed, totalfailed):
	return failed**2/(passed+totalfailed-failed+1)

def tarantula_formula(passed,failed,totalpassed,totalfailed):
	return (failed/(totalfailed+1))/((failed/(totalfailed+1))+(passed/(totalpassed+1))+1)

def barinel_formula(passed,failied,totalpassed,totalfailed):
	return 1-(passed/(passed+failied+1))

def jaccard_formula(passed,failied,totalpassed,totalfailied):
	return failied/(totalfailied+passed+1)

if __name__=='__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('--formula', required=True, choices=['ochiai', 'op2', 'dstar','barinel','tarantula','jaccard'])
	parser.add_argument('--spectra', required=True)
	parser.add_argument('--matrix', required=True)
	parser.add_argument('--output', required=True)

	args=parser.parse_args()

	stmts=[]
	tc_coverage=[]
	tc_result=[]
	susp_score=dict()
	totalfailed=0
	totalpassed=0
	with open(args.spectra, 'r') as spectra_file:
		for line in spectra_file:
			stmts.append(line.strip())
	with open(args.matrix, 'r') as matrix_file:
		for line in matrix_file:
			result=line.strip().split()[-1]
			if result=='+':
				totalpassed+=1
			else:
				totalfailed+=1
			tc_result.append(result)
			tc_coverage.append(line.strip().split()[:-1])
	
	formula_func_dict={'dstar': dstar_formula, 'ochiai': ochiai_formula, 'op2':op2_formula, 'tarantula':tarantula_formula, 'barinel':barinel_formula, 'jaccard':jaccard_formula}
	for i in range(len(stmts)):
		passed=0
		failed=0
		for j in range(len(tc_coverage)):
			if tc_coverage[j][i]=='1':
				if tc_result[j]=='+':
					passed+=1
				else:
					failed+=1
		susp_score[stmts[i]]=formula_func_dict[args.formula](passed, failed, totalpassed, totalfailed)

	with open(args.output, 'w') as out_file:
		writer=csv.DictWriter(out_file, ['Statement', 'Suspiciousness'])
		writer.writeheader()
		for stmt, susp in susp_score.items():
			writer.writerow({'Statement':stmt, 'Suspiciousness':susp})
		
