#!/usr/bin/env python
"""
Generate json file for sunburst.js from ARA (Allen Reference Atlas) and a list of targets file.

Both input files are in CSV format with Latin-1 encoding.

Input file CSV format:
A reference table with all the possible brain areas listed as “id” (Column 0), described by their full ‘name’ (Column 1), 'acronym' (Column 2), unique ‘red’ (Column 3), ‘green’ (Column 4) and ‘blue’  (Column 5) value combination, 'structure order’ (Column 6), 'parent id' (Column 7) and 'parent acronym’ (Column 8) (see attached 'ARA2_annotation_structure_info.csv’).


The second input file contains a sample dataset with list hits from the reference table along with the ascribed values ‘Count' (Column 9) (see attached ‘List_of_Targets_180830FezfCFA.xlsx’).


The resultant output is in json format presents the structure ontology: http://api.brain-map.org/api/v2/structure_graph_download/1.json
The structure ontology has the following descriptors in common with the attached files: “id”, “parent_structure_id”, “name”, “acronym".  “color_hex_triplet” is a way of describing the unique combinations of red green and blue values.


The following webpage has the code needed to generate the sunburst plot: http://api.brain-map.org/examples/sunburst/index.html
To be specific, the first step will be to import the data using the pipeline in the following link: http://api.brain-map.org/examples/doc/sunburst/import.js.html


Copyright © 2019 Tom Adams. All rights reserved.
"""

import csv
import json
import pprint
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('ARA', type=str, help='Annotated Structure Info ARA formated CSV file')
parser.add_argument('TARGETS', type=str, help='List of targets (counts) ARA formated CSV file')
args = parser.parse_args()

pp = pprint.PrettyPrinter(indent=3)

header = ( "id","name","acronym","red","green","blue","structure_order","parent_id","parent_acronym", "count" )
node = {}
hierarchy = {}
with open(args.ARA, newline='', encoding='Latin-1' ) as f:
    reader = csv.reader(f)
    headers = next(reader,None)
    for row in reader:
        if row[0] in node:
           print("################ NODE EXISTS ALREADY:  {}".format(row[0]))
        color = '%X' % int(row[3]) + '%X' % int(row[4]) + '%X' % int(row[5])
        if row[7] == '':
           row7 = -100
        else:
           row7 = int(row[7])
        row7s = str(row7)
        name = row[1].encode('ascii', errors='ignore').decode()
        node[row[0]] = { 'id': int(row[0]), 'atlas_id': int(row[0]), 'ontology_id': 1, 'acronym': row[2], 'name': name,
                         'color_hex_triplet': color, 'graph_order': int(row[6]), 'st_level': 0, 
                         'hemisphere_id': 3, 'parent_structure_id': row7, 'children': []  }
        if row7s in hierarchy:
            hierarchy[row7s] = hierarchy[row7s] + [row[0]]
        else:
            hierarchy[row7s] = [row[0]]
        #print('{}  ===>>  {}'.format(row7s,hierarchy[row7s]))
        #pp.pprint(node[row[0]])

for key,val in node.items():
  if key in hierarchy:
    for child in hierarchy[key]:
      if child in node:
          node[key]['children'].append(node[child])
      else:
          print('Child not in node')
  #print("{}  x  {}".format(key,val))
  #pp.pprint(val)
    
with open(args.TARGETS, newline='', encoding='Latin-1' ) as f:
    reader = csv.reader(f)
    headers = next(reader,None)
    for row in reader:
        #print(row)
        if row[0] in node:
            node[row[0]]['st_level'] = row[9]
        else:
            print('############# Did not find {} ({}) in nodes but existed in counts.'.format(row[0],row[1]))

if  __name__ == "__main__":
    #pp.pprint(node['997'])
    print(json.dumps(node['997'],sort_keys=True,indent=2, separators=(', ', ': ')))

