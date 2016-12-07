#!/usr/bin/env python

import re


#INDI - 0 @P1@ INDI
def parseINDI (linearray, countofarrayvalues):
	if countofarrayvalues == 3: #expectedlength
		previouslinepersonnumber = linepersonnumber
		newlinepersonnumber = linearray[1]
		print(linearray[1])
		if newlinepersonnumber != previouslinepersonnumber:
			linepersonnumber = newlinepersonnumber
			print(linepersonnumber)
	return;


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
for gedcomline in gedcomfile:
	#print(line)
    #Parse the line by Spaces
    linearray = gedcomline.split(" ")
    print(linearray)
    #Determine Length of array
    countofarrayvalues = len(linearray)
    if countofarrayvalues >= 3:
    	#line context
    	#print(linearray[2])
        if linearray[0] == "1":
        	linecontext = linearray[1]
        if linearray[2] == "INDI": #new individual
            parseINDI(linearray,countofarrayvalues)
				
#session.close()
