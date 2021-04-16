#!/usr/bin/python2.7

import argparse
import csv

def classname_to_filename(classname):
  classname = classname[:classname.find('.java')]
  return classname.replace('/', '.')
def stmt_to_line(stmt):
  classname, lineno = stmt.rsplit('#')
  return '{}#{}'.format(classname_to_filename(classname), lineno)


assert classname_to_filename('org/apache/MyClass.java') == 'org.apache.MyClass'
assert stmt_to_line('org/apache/MyClass.java#123') == 'org.apache.MyClass#123'

parser = argparse.ArgumentParser()
parser.add_argument('--muts-in-line', required=True)
parser.add_argument('--source-code-lines', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

source_code = dict()
with open(args.source_code_lines) as f:
  for line in f:
    line = line.strip()
    entry = line.split(':')
    entry[0]= stmt_to_line(entry[0])
    entry[1]=stmt_to_line(entry[1])
    key = entry[0]
    if key in source_code:
      source_code[key].append(entry[1])
    else:
      source_code[key] = []
      source_code[key].append(entry[1])
f.close()

to_pop=list()

for line in source_code:
  tmp=list()
  for subline in source_code[line]:
    if subline in source_code.keys():
      to_pop.append(subline)
      for sub_subline in source_code[subline]:
        if sub_subline not in source_code[line]:
          tmp.append(sub_subline)
  for subline in tmp:
    source_code[line].append(subline)
for line in to_pop:
  source_code.pop(line)


muts_in_line=dict()

#
# Collect and convert all statements into lines
#
with open(args.muts_in_line) as m2l_file:
  reader = csv.DictReader(m2l_file,delimiter=':')
  for row in reader:
    line = row['Statement']
    susps = row['Mutants']
    muts_in_line[line]=susps.split(',')
m2l_file.close()

muts_in_stmt=dict()
for line in muts_in_line:
  muts_in_stmt[line]=muts_in_line[line]
to_pop=list()

for line in source_code:
  if line in muts_in_line:
    for subline in source_code[line]:
     if subline in muts_in_line:
       for mut in muts_in_line[subline]:
         muts_in_stmt[line].append(mut)
       if subline not in to_pop:
         to_pop.append(subline)
       #muts_in_stmt.pop(subline)
  else:
    for subline in source_code[line]:
      if subline in muts_in_line:
        if line not in muts_in_stmt:
          muts_in_stmt[line]=[]
        for mut in muts_in_line[subline]:
          muts_in_stmt[line].append(mut)
        if subline not in to_pop:
          to_pop.append(subline)
        #muts_in_stmt.pop(subline)
for line in to_pop:
  muts_in_stmt.pop(line)
'''
for line in muts_in_line:
  if line in source_code:
    for subline in source_code[line]:
      if subline in muts_in_stmt.keys():
        muts_in_stmt.pop(subline)
'''

#
# Write the dictionary to the output file
#
with open(args.output, 'w') as f:
  writer = csv.DictWriter(f,['Statement','Mutants'],delimiter=':')
  writer.writeheader()
  for stmt in muts_in_stmt:
    writer.writerow({'Statement':stmt,'Mutants': ','.join(muts_in_stmt[stmt])})
f.close()

# EOF

