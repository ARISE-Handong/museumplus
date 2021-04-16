import csv
import sys
import math
import argparse

f2p=0
p2f=0

def mutant_sum(formula, orig_out, mut_out, orig_st=None, mut_st=None):
	global f2p
	global p2f
	orig_result=dict()
	mut_result=dict()
	for line in orig_out:
		testcase,_, result = line.split(',')
		orig_result[testcase]=result.strip()
	for line in mut_out:
		testcase, mutId, result= line.split(',')
		result=result.strip()
		if formula=='muse' and result=="TIMEOUT":
			result="FAILED"
		if mutId in mut_result:
			mut_result[mutId].append((testcase,result))
		else:
			mut_result[mutId]=list()
			mut_result[mutId].append((testcase,result))
	mutant_info=dict()
	if formula=='muse' or formula=='museum':
		for mutId, testcases in mut_result.items():
			passed=0
			failed=0
			for testcase in testcases:
				if testcase[1]=="PASS" and orig_result[testcase[0]]=="FAILED":
					failed+=1
					f2p+=1
				elif testcase[1]=="FAILED" and orig_result[testcase[0]]=="PASS":
					passed+=1
					p2f+=1
			mutant_info[mutId]=(passed, failed)
	if formula=='metallaxis' or formula=='mutallaxis':
		orig_stack=dict()
		mut_stack=dict()
		for st in orig_st:
			testcase,_,stacktrace= st.split(',')
			orig_stack[testcase]=stacktrace.strip()
		for st in mut_st:
			testcase, mutId, stacktrace=st.split(',')
			stacktrace=stacktrace.strip()
			if mutId in mut_stack:
				mut_stack[mutId][testcase]=stacktrace
			else:
				mut_stack[mutId]=dict()
				mut_stack[mutId][testcase]=stacktrace
		for mutId, testcases in mut_result.items():
			passed=0
			failed=0
			for testcase in testcases:
				if (testcase[1]=="PASS" and orig_result[testcase[0]]!="PASS") or (testcase[1]=="FAILED" and orig_result[testcase[0]]=="FAILED" and mut_stack[mutId][testcase[0]]!=orig_stack[testcase[0]]):
					failed+=1
				elif (testcase[1]=="FAILED" and orig_result[testcase[0]]!="FAILED") or (testcase[1]=="TIMEOUT" and orig_result[testcase[0]]!="TIMEOUT"):
					passed+=1
			mutant_info[mutId]=(passed,failed)
	return mutant_info

def metallaxis_formula(passed,failed,totalpassed,totalfailed):
	return float(failed)/((totalfailed*(failed+passed)+1)**0.5)

def muse_formula(passed,failed, totalpassed,totalfailed):
	global p2f
	global f2p
	return float(failed) -(float(f2p+1)/float(p2f+1) *float(passed))
	#return float(failed)/totalfailed - (float(f2p+1)/totalfailed *float(totalpassed+1)/p2f)*float(passed)/totalpassed

def museum_formula(passed,failed, totalpassed,totalfailed):
	global p2f
	global f2p
	return float(failed)/float(f2p+1) -float(passed)/float(p2f+1)


if __name__=='__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('--formula', required=True, choices=['muse','museum','metallaxis','mutallaxis'])
	parser.add_argument('--original_out', required=True)
	parser.add_argument('--original_st', required=False)
	parser.add_argument('--f2p_mut_cov', required=True)
	parser.add_argument('--mut_out', required=True)
	parser.add_argument('--mut_st', required=False)
	parser.add_argument('--mutsInStmt', required=True)
	parser.add_argument('--target_stmts', required=True)

	args=parser.parse_args()

	totalpassed=0
	totalfailed=0
	if args.formula=='muse' or args.formula=='museum':
		with open(args.original_out,'r') as orig_out, open(args.mut_out, 'r') as mut_out:
			mutant_info=mutant_sum(args.formula, orig_out, mut_out)
	if args.formula=='metallaxis' or args.formula=='mutallaxis':
		with open(args.original_out,'r') as orig_out, open(args.mut_out, 'r') as mut_out, open(args.original_st, 'r') as orig_st, open(args.mut_st,'r') as mut_st:
			mutant_info=mutant_sum(args.formula, orig_out, mut_out, orig_st=orig_st, mut_st=mut_st)
		
	with open(args.original_out,'r') as orig_out:
		for line in orig_out:
			_,_, result=line.split(',')
			result=result.strip()
			if result=="PASS":
				totalpassed+=1
			else:
				totalfailed+=1

	target=list()
	with open(args.target_stmts, 'r') as target_f:
		for line in target_f:
			target.append(line.strip())	
	
	mut_cov=list()
	with open(args.f2p_mut_cov, 'r') as mut_cov_f:
		for line in mut_cov_f:
			hasExecuted=line.strip().split()[:-1]
			mut_cov.append(hasExecuted)

	stmt_uncov=dict()
	for stmt in target:
		stmt_uncov[stmt]=0
		
	all_uncov=0
	for tc_idx in range(len(mut_cov)):
		for stmt_idx, stmt in enumerate(target):
			if int(mut_cov[tc_idx][stmt_idx])==0:
				stmt_uncov[stmt]+=1
				all_uncov+=1

	mutInStmt=dict()
	with open(args.mutsInStmt, 'r') as mutInSt_out:
		mutInSt_out.readline()
		for line in mutInSt_out:
			stmt, mutants = line.split(':')
			mutInStmt[stmt]=mutants.split(',')
			mutInStmt[stmt][-1]=mutInStmt[stmt][-1].strip()


	numMutInStmt=dict()
	for stmt in mutInStmt:
		numMutInStmt[stmt]=len(mutInStmt[stmt])

	stmts_susp=dict()
	if args.formula=='muse' or args.formula=='museum':
		for stmt, mutants in mutInStmt.items():
			stmt_susp=0
			for mutant in mutants:
				if mutant in mutant_info:
					if args.formula=='muse':
						stmt_susp+=muse_formula(mutant_info[mutant][0], mutant_info[mutant][1], totalpassed, totalfailed)
					else:
						stmt_susp+=museum_formula(mutant_info[mutant][0], mutant_info[mutant][1], totalpassed, totalfailed)
			stmt_susp/=(numMutInStmt[stmt])
			if all_uncov==0:
				all_uncov+=1
			if f2p==0:
				f2p+=1
			if stmt in stmt_uncov:
				stmt_susp+=(stmt_uncov[stmt]/float(all_uncov))/f2p
			stmts_susp[stmt]=stmt_susp
	if args.formula=='metallaxis' or args.formula=='mutallaxis':
		for stmt, mutants in mutInStmt.items():
			stmt_susp=0
			mut_susp=[]
			for mutant in mutants:
				if args.formula=='metallaxis':
					if mutant in mutant_info:
						mut_susp.append(metallaxis_formula(mutant_info[mutant][0],mutant_info[mutant][1], totalpassed, totalfailed))
					else: 
						mut_susp.append(0)
				if args.formula=='mutallaxis':
					if mutant in mutant_info:
						stmt_susp+=museum_formula(mutant_info[mutant][0], mutant_info[mutant][1], totalpassed, totalfailed)
			if args.formula=='mutallaxis':
				stmt_susp/=numMutInStmt[stmt]
				stmts_susp[stmt]=stmt_susp			
			elif args.formula=='metallaxis':
				stmts_susp[stmt]=max(mut_susp)

	added=list()
	with open(args.formula+"statement_susp", 'w') as out_file:
		writer=csv.DictWriter(out_file,['Statement', 'Suspiciousness'])
		writer.writeheader()
		for stmt, susp in stmts_susp.items():
			if stmt in target:
				added.append(stmt)
				writer.writerow({'Statement': stmt, 'Suspiciousness':susp})
		for stmt in target:
			if stmt not in added:
				writer.writerow({'Statement':stmt, 'Suspiciousness':'0'})
