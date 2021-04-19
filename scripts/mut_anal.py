import collections
import re
import argparse
import csv
import sys

currentTest=""
test_output = collections.namedtuple('test_output', ('test_case', 'mut_id', 'result', 'stack_trace'))
def parse_pass_output(outLine, mut_id):
  global currentTest
  _, _, test_case, _, _, _= outLine.split()
  return test_output(test_case=currentTest+"#"+test_case, mut_id=mut_id, result="PASS", stack_trace="")

def parse_fail_output(outLine, mut_id):
  global currentTest
  _, _, test_case, _, _, _=outLine[0].split()
  for i in range(3,len(outLine)):
    outLine[i]=outLine[i].strip()
    outLine[i]=outLine[i].replace("[junit]","")
    outLine[i]=outLine[i].replace(",", "")
    outLine[i]=outLine[i].strip()
  stack_trace=' '.join(outLine[3:len(outLine)-1])
  stack_trace=stack_trace.split("Running")[0]
  stack_trace=stack_trace.split("BUILD ")[0].strip()
  return test_output(test_case=currentTest+"#"+test_case, mut_id=mut_id, result="FAILED", stack_trace=stack_trace)

def parse_timeout_output(outLine, mut_id):
  global currentTest
  _,_, test_case, _, _, _=outLine.split()
  return test_output(test_case=currentTest+"#"+test_case, mut_id=mut_id, result="TIMEOUT", stack_trace="")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', required=True)
  parser.add_argument('--target_testcase', required=True)
  parser.add_argument('--result_file', required=True)
  parser.add_argument('--stacktrace_file', required=True)
  parser.add_argument('--isOriginal', required=True, choices=['true', 'false'])
  parser.add_argument('--mut_id', required=True)

  args= parser.parse_args()
  output=[]
  numFailed=0
  target_tcs=[]
  result=""

  with open(args.input_file) as result_file:
    for line in result_file:
      output.append(line)
  with open(args.target_testcase) as tc_file:
    for line in tc_file:
      target_tcs.append(line.strip())

  writeOrAppend='a'
  with open(args.result_file, writeOrAppend) as o_file, open(args.stacktrace_file,writeOrAppend) as st_file:
    writer=csv.DictWriter(o_file, ['Testcase', 'Mut_id', 'Result'], quotechar='', escapechar='\\',quoting=csv.QUOTE_NONE)
    st_writer=csv.DictWriter(st_file, ['Testcase', 'Mut_id', 'Stacktrace'], quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)
    for i in range(len(output)):
      if i+1<len(output):
        failType="fail"
        if ("Testsuite: " in output[i]):
          currentTest=output[i].split()[2]
        if ("Testcase: " in output[i]): #and ("Testcase: " in output[i+1] or "Running " in output[i+1]):# and ("ERROR" not in output[i+1]) and ("FAILED" not in output[i+1] or ("FAILED"in output[i+1] and "TEST" in output[i+1])):
          j=1
          while i+j<len(output) and ("Testcase: " not in output[i+j]) and ("Running" not in output[i+j]):
            j+=1
          for line in output[i:i+j]:
            if ("ERROR" not in line) and ("FAILED" not in line or ("FAILED" in output[i:i+j] and "TEST" in line)):
              result="pass"
            else:
              result="fail"
              break
          if result=="pass":
            parsed_out=parse_pass_output(output[i], args.mut_id)
            #if args.isOriginal=='true':
            if parsed_out.test_case in target_tcs:
              writer.writerow({'Testcase': parsed_out.test_case, 'Mut_id': parsed_out.mut_id, 'Result': parsed_out.result})
            #else:
              #if parsed_out.test_case in target_tcs:
                #writer.writerow({'Testcase': parsed_out.test_case, 'Mut_id': parsed_out.mut_id, 'Result': parsed_out.result})
          elif result=="fail":
            for line in output[i:i+j]:
              if "test timed out" in line or "Timeout" in line:
                failType="timeout"
                break
            if failType=="timeout":
              parsed_out=parse_timeout_output(output[i], args.mut_id)
            else:
              numFailed+=1
              parsed_out=parse_fail_output(output[i:i+j], args.mut_id)
            #if args.isOriginal=='true':
            if parsed_out.test_case in target_tcs:
              writer.writerow({'Testcase': parsed_out.test_case, 'Mut_id': parsed_out.mut_id, 'Result': parsed_out.result})
              if failType=="fail":
                st_writer.writerow({'Testcase':parsed_out.test_case, 'Mut_id': parsed_out.mut_id, 'Stacktrace': parsed_out.stack_trace})
            #else:
              #if parsed_out.test_case in target_tcs:
                #writer.writerow({'Testcase': parsed_out.test_case, 'Mut_id': parsed_out.mut_id, 'Result': parsed_out.result})
                #if failType=="fail":
                  #st_writer.writerow({'Testcase':parsed_out.test_case, 'Mut_id':parsed_out.mut_id, 'Stacktrace': parsed_out.stack_trace})

