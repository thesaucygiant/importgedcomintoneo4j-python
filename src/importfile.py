#!/usr/bin/env python

import re

#from neo4j.v1 import GraphDatabase, basic_auth
#driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "CIAshit2016h"))
#session = driver.session()
 #session.run("CREATE (a:Person {name:'Bob'})")
		#result = session.run("MATCH (a:Person) RETURN a.name AS name")
		#for record in result:
   		#print(record["name"])
		#if firstslashposition:
        #	secondslashposition = line.index('/',firstslashposition+1)
        #	print firstslashposition + ' ' + secondslashposition + ' ' + line


gedcomfile = open("stonepark-tree.ged", "r")
for line in gedcomfile:
    #print line
	if re.match("(.*)NAME(.*)", line):
    	#print line
		if line.find("/") <> -1:
		####
			firstslashposition = 0
			#firstslashposition = line.find('/')
			print "Found a Forward Slash"
			print firstslashposition
			print line
		#else:
    		#print "Found 'is' in the string."
    		#########

#session.close()
