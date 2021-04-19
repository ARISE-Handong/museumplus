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


for filename in $MUT_DIR/*; do
	pushd "$filename/" > /dev/null
	mut_src=`find $filename -name "*.java"` 
	mut_src=${mut_src#${filename}}
	mut_src=${mut_src#'/'}
	IFS='/' read -ra count <<<"$filename"
	count=${count[-1]}
	echo "Executing ${count}th mutant"
	popd > /dev/null
	mv "source/$mut_src" "original_code"
	cp "$filename/$mut_src" "source/$mut_src"
	ant clean compile-tests
	ant test > "mut${count}_out"
	python mut_anal.py --input_file="mut${count}_out" --target_testcase="target_testcases" --result_file="$OUTPUT_FILE" --stacktrace_file="${OUTPUT_FILE}_st" --isOriginal="false" --mut_id="$count"
	mv "mut${count}_out" "$MUT_DIR/$count"
	mv "original_code" "source/$mut_src"
#	count+=1
done
