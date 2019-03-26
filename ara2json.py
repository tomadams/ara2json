#!/usr/bin/env python

# Copyright © 2019 Tom Adams. All rights reserved.
#
# ara2json.py - Generate json file for sunburst.js from ARA (Allen Reference Atlas) and a list of targets file.
#
# Both input files are in CSV format with Latin-1 encoding.

import csv
import json
import pprint
import argparse

parser = argparse.ArgumentParser(description='Optional app description')
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

