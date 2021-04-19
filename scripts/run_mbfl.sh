#!/bin/bash

USAGE="$0 BID"
if ["$#" != 2 ]; then echo ${USAGE} >&2; exit 1; fi

#Setting Defects4j path
GIT_HOME=$(git rev-parse --show-toplevel)
DEFECTS4J_HOME="$(git rev-parse --show-toplevel)/defects4j"
LIB_HOME=$GIT_HOME/lib

echo "defects4j.home=${DEFECTS4J_HOME}" >> default.properties
echo "lib.home=$LIB_HOME" >> default.properties
bid=$1

# Generate MML file
$DEFECTS4J_HOME/framework/util/create_mml.pl -p Chart -b $bid -o . -c $DEFECTS4J_HOME/framework/projects/Chart/loaded_classes/$bid.src
# Generate mutants 
$DEFECTS4J_HOME/major/bin/ant -DmutOp="=$bid.mml.bin" -DexportBool="=true" -DexportPath="=./mutants" clean compile
# Save file that maps mutants to statements
cp mutants.log mut_log_backup
python mutToStmt.py --mutlog_file mutants.log --output_file mut2line
# Lines executed by failing test cases from statements 
./stmt2line --failing-stmts failing_stmts --source-code-lines $LIB_HOME/source-code-lines/Chart-${bid}b.source-code.lines --output failing_lines 
# Remove mutants not generated in the target lines
python truncate_mutants.py --mutToStmt_file mut2line --mutant_dir mutants --targetStmts_file failing_lines --output_file used_mutants
# Run tests on mutants 
./mut_anal.sh ./mutants target_testcases mutant_out
# Combine Timeouts
python3 find_missing_runs.py --used-muts used_mutants --target-tcs target_testcases --mutant-out mutant_out
./mut_anal_permut.sh mutants target_testcases missing_out
cat missing_out >> mutant_out
rm missing_*
mv mut_log_backup mutants.log
