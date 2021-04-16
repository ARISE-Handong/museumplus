#!/bin/bash

USAGE="$0 bid"
if [ "$#" != 1 ]; then echo ${USAGE} >&2; exit 1; fi

num=$1

./integrate_muts_in_stmt.py --muts-in-line ../Chart-$num/raw_data/MBFL/mut2line --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/raw_data/MBFL/mut2stmt


python3 mbfl_susp_score.py --formula muse  --original_out ../Chart-$num/raw_data/MBFL/original_out --mut_out ../Chart-$num/raw_data/MBFL/mutant_out --mutsInStmt ../Chart-$num/raw_data/MBFL/mut2stmt --target_stmts ../Chart-$num/raw_data/SBFL/failing_stmts
mv musestatement* muse_susp_score
python3 mbfl_susp_score_mut_cov.py --formula museum  --original_out ../Chart-$num/raw_data/MBFL/original_out --f2p_mut_cov ../Chart-$num/raw_data/omission/mut_gzoltar --mut_out ../Chart-$num/raw_data/MBFL/mutant_out --mutsInStmt ../Chart-$num/raw_data/MBFL/mut2stmt --target_stmts ../Chart-$num/raw_data/SBFL/failing_stmts
mv museumstatement* museum_susp_score
python3 mbfl_susp_score.py --original_out ../Chart-$num/raw_data/MBFL/original_out --original_st ../Chart-$num/raw_data/MBFL/original_out_st --mut_out ../Chart-$num/raw_data/MBFL/mutant_out --mut_st ../Chart-$num/raw_data/MBFL/mutant_out_st --mutsInStmt ../Chart-$num/raw_data/MBFL/mut2stmt --target_stmts ../Chart-$num/raw_data/SBFL/failing_stmts --formula metallaxis
mv metalla* met_susp_score
python3 mbfl_susp_score.py --original_out ../Chart-$num/raw_data/MBFL/original_out --original_st ../Chart-$num/raw_data/MBFL/original_out_st --mut_out ../Chart-$num/raw_data/MBFL/mutant_out --mut_st ../Chart-$num/raw_data/MBFL/mutant_out_st --mutsInStmt ../Chart-$num/raw_data/MBFL/mut2stmt --target_stmts ../Chart-$num/raw_data/SBFL/failing_stmts --formula mutallaxis
mv mutallaxisstatement* mutallaxis_susp_score

python3 sbfl_susp_score.py --spectra ../Chart-$num/raw_data/SBFL/failing_stmts --matrix ../Chart-$num/raw_data/SBFL/gzoltar_matrix --formula barinel --output barinel_susp_score
python3 sbfl_susp_score.py --spectra ../Chart-$num/raw_data/SBFL/failing_stmts --matrix ../Chart-$num/raw_data/SBFL/gzoltar_matrix --formula tarantula --output tarantula_susp_score
python3 sbfl_susp_score.py --spectra ../Chart-$num/raw_data/SBFL/failing_stmts --matrix ../Chart-$num/raw_data/SBFL/gzoltar_matrix --formula jaccard --output jaccard_susp_score
python3 sbfl_susp_score.py --spectra ../Chart-$num/raw_data/SBFL/failing_stmts --matrix ../Chart-$num/raw_data/SBFL/gzoltar_matrix --formula ochiai --output ochiai_susp_score
python3 sbfl_susp_score.py --spectra ../Chart-$num/raw_data/SBFL/failing_stmts --matrix ../Chart-$num/raw_data/SBFL/gzoltar_matrix --formula op2 --output op2_susp_score
python3 sbfl_susp_score.py --spectra ../Chart-$num/raw_data/SBFL/failing_stmts --matrix ../Chart-$num/raw_data/SBFL/gzoltar_matrix --formula dstar --output dstar_susp_score

mkdir ../Chart-$num/susp_score
mv *susp_score ../Chart-$num/susp_score


./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/muse_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/muse_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/museum_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/museum_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/met_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/met_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/mutallaxis_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/mutallaxis_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/op2_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/op2_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/ochiai_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/ochiai_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/dstar_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/dstar_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/barinel_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/barinel_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/jaccard_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/jaccard_line_susp
./stmt-susps-to-line-susps --stmt-susps ../Chart-$num/susp_score/tarantula_susp* --source-code-lines ../../chart/source-code-lines/Chart-${num}b.source-code.lines --output ../Chart-$num/susp_score/tarantula_line_susp

#./score-ranking --project Chart --bug $num --line-susps ../Chart-$num/susp_score/${form}_line_susp --scoring-scheme first --sloc-csv ../../chart/buggy-lines/sloc.csv --buggy-lines ../Chart-$num/raw_data/Chart-$num.buggy.lines -output t


