#!/usr/bin/python

import os
import random
import sys
import re
from vtktools import VTUWriter
from collections import OrderedDict


usage = "%s input-file output-file" %(sys.argv[0])

if len(sys.argv) < 3:
    print "Please provide an input and output files"
    print usage
    exit(1)

# opening and parsing input file
input_file = sys.argv[1]
f = open(input_file,'r+')
input_lines = f.readlines()
node_regex = re.compile("node\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*")
vertex_regex = re.compile("element quad (\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*")
nodes = {}
connectivity = []

hasFoundConnectivity = False

for line in input_lines:
    result_node = node_regex.match(line)
    if result_node != None:
        nodeId = result_node.group(1)
        nodeX = result_node.group(2)
        nodeY = result_node.group(3)
        #print '%s : (%s,%s)' %(nodeId,nodeX,nodeY)
        if not hasFoundConnectivity:
            nodes[int(nodeId)] = (float(nodeX),float(nodeY),0.0)
        continue

    result_vertex = vertex_regex.match(line)
    if result_vertex == None:
        continue
    else:
        hasFoundConnectivity = True
        members = [int(result_vertex.group(2))-1,int(result_vertex.group(3))-1,int(result_vertex.group(4))-1,int(result_vertex.group(5))-1]
        #print members
        connectivity.append(members)

nodes_sorted_by_value = OrderedDict(sorted(nodes.items(), key=lambda x: x[0]))

writer = VTUWriter()

fakeVel = [[random.random(),random.random(),1.0] for i in range(len(nodes.keys()))]

writer.snapshot("test.vtu",nodes_sorted_by_value.keys(),connectivity,nodes_sorted_by_value.values(),[],[],[])


# opening and parsing output file








