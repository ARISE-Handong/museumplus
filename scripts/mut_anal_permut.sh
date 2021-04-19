#!/bin/bash

#cache original src code

HOME_DIR=$(dirname ${BASH_SOURCE[0]})
declare -i mutId=0

USAGE="$0 MUT_DIR TARGET_TESTCASES OUTPUT_FILE"

die(){
	echo "$@" >&2
	exit 1
}

ensure-dir-exists(){
	if [ ! -d "$1" ]; then
		die "'$1' is not a directory" >$2
	fi
}

if [ "$#" != 3 ]; then echo ${USAGE} >&2; exit 1; fi
MUT_DIR=$(readlink --canonicalize "$1"); ensure-dir-exists "$MUT_DIR"
TARGET_TESTCASES=$2
OUTPUT_FILE=$3

prev_run=-1

while read run; do
	echo "Executing ${run}"
	IFS="," read -ra run_info <<< "$run"
	pushd "$MUT_DIR/${run_info[0]}/" > /dev/null
	mut_src=`find . -name "*.java"`
	popd > /dev/null
	mv "source/$mut_src" "original_code"
	cp "$MUT_DIR/${run_info[0]}/$mut_src" "source/$mut_src"
	if [ $prev_run != ${run_info[0]} ]; then
		ant clean compile-tests
		prev_run=${run_info[0]}
	fi
	IFS='#' read -ra class_tc <<< "${run_info[1]}"
	echo "test.entry=${class_tc[0]}" >> default.properties
	echo "test.testcase=${class_tc[1]}" >> default.properties
	ant test > "mut${run_info[0]}_out"
	python mut_anal.py --input_file="mut${run_info[0]}_out" --target_testcase="target_testcases" --result_file="$OUTPUT_FILE" --stacktrace_file="${OUTPUT_FILE}_st" --isOriginal="false" --mut_id="${run_info[0]}"
	sed -i '$ d' default.properties
	sed -i '$ d' default.properties
	rm "mut${run_info[0]}_out"
	mv "original_code" "source/$mut_src"
done < missing_runs
