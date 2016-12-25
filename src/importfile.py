#!/usr/bin/env python

import re
linepersonnumber = ""
linefamilynumber = ""
linehusbpersonnumber = ""
linewifepersonnumber = ""
linechilpersonnumber = ""
linesexpersonnumber = ""
currentcontext = ""

#create connection to NEO4j
from neo4j.v1 import GraphDatabase, basic_auth
driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "CIAshit2016h"))
session = driver.session()

#delete
session.run("MATCH h=()-[r:Husband]->() Delete r")
session.run("MATCH w=()-[r:Wife]->() Delete r")
session.run("MATCH c=()-[r:Child]->() Delete r")
session.run("MATCH c=()-[r:Born]->() Delete r")
session.run("MATCH c=()-[r:BornIn]->() Delete r")
session.run("MATCH c=()-[r:MarriedAt]->() Delete r")
session.run("MATCH c=()-[r:Married]->() Delete r")
session.run("MATCH c=()-[r:Graduated]->() Delete r")
session.run("MATCH c=()-[r:Born]->() Delete r")
session.run("MATCH c=()-[r:Resided]->() Delete r")
session.run("MATCH c=()-[r:Died]->() Delete r")
session.run("MATCH (n) DELETE n")

#Cleanup and parse the GEDCOM line
def formatGEDCOMLINE (gedcomline):
	gedcomline = gedcomline.replace("\n","")
	linearray = gedcomline.split(" ")
	return linearray;

#INDI - 0 @P1@ INDI
def parseINDI (linearray):
	if countofarrayvalues == 3: #expectedlength
		linepersonnumber = linearray[1]
		cypher = "CREATE (a:PERSON {personid:'" + linepersonnumber + "'})"
		session.run(cypher)
	return linepersonnumber;

#NAME	
def parseNAME (gedcomline, linepersonnumber, linearray):
		namecount = len(linearray) - 2
		surname = ""
		nonsurname = ""
		namesuffix = ""
		#pull surname from between two slashes then ignore array values with slashes
		positionfirstslash = 0
		positionlastslash = 0
		positionfirstslash = gedcomline.find("/",1)
		if positionfirstslash > 0: positionlastslash = gedcomline.find("/", positionfirstslash+1)
		if ((positionfirstslash > 0) & (positionlastslash > positionfirstslash)):
			surname = gedcomline[positionfirstslash+1:positionlastslash]
			surname = surname.replace("'"," ")
			surname = surname.strip()
			existingpersonidcypher = "MATCH (a:PERSON) WHERE a.personid = '" + linepersonnumber + "' RETURN a.personid"
			result = session.run(existingpersonidcypher)
			if result:
				updatesurnamecypher = "MATCH (a:PERSON) WHERE a.personid = '" + linepersonnumber + "' SET a.surname = '" + surname + "'"
				session.run(updatesurnamecypher)
			else:
				cypher = "CREATE (a:PERSON {personid:'" + linepersonnumber + "', nonsurname:'" + nonsurname + "', surname:'" + surname + "'})"
				session.run(cypher)
				print "insert surname"	
		#nonsurname
		positionfirstslash = 0
		lengthoflinearray = len(linearray) - 1
		for num, namepart in enumerate(linearray[2:], start=2):
			#name suffix doesnt have a lsash and is last element and surname is not blank
			if ((num == lengthoflinearray) & (namepart.find("/") == -1) & (surname <> "")): namesuffix = namepart
			if ((num < lengthoflinearray) & (namepart.find("/") == -1)): nonsurname = nonsurname + namepart + " "
		nonsurname = nonsurname.strip()
		updatenonsurnamecypher = "MATCH (a:PERSON) WHERE a.personid = '" + linepersonnumber + "' SET a.nonsurname = '" + nonsurname + "'"
		session.run(updatenonsurnamecypher)
		return;

def parseFAM (linearray):
	if countofarrayvalues == 3: #expectedlength
		linefamilynumber = linearray[1]
		#NEO 4j
		cypher = "CREATE (f:FAMILY {familyid:'" + linefamilynumber + "'})"
		#print(cypher)
		session.run(cypher)	
	return linefamilynumber;

def parseHUSB (linefamilynumber, linearray):
	if countofarrayvalues == 3: #expectedlength
		linehusbpersonnumber = linearray[2]
		#NEO 4j
		husbcypher = "MATCH (i:PERSON) where i.personid = '" + linehusbpersonnumber + "' match (f:FAMILY) where f.familyid = '" + linefamilynumber + "' CREATE (i)-[r:Husband]->(f)" 
		#print(husbcypher)
		session.run(husbcypher)	
	return;

def parseWIFE (linefamilynumber, linearray):
	if countofarrayvalues == 3: #expectedlength
		linewifepersonnumber = linearray[2]
		wifecypher = "MATCH (i:PERSON) where i.personid = '" + linewifepersonnumber + "' match (f:FAMILY) where f.familyid = '" + linefamilynumber + "' CREATE (i)-[r:Wife]->(f)" 
		session.run(wifecypher)
		
	return;
	
def parseCHIL (linefamilynumber, linearray):
	if countofarrayvalues == 3: #expectedlength
		linechilpersonnumber = linearray[2]
		childcypher = "MATCH (i:PERSON) where i.personid = '" + linechilpersonnumber + "' match (f:FAMILY) where f.familyid = '" + linefamilynumber + "' CREATE (i)-[r:Child]->(f)" 
		session.run(childcypher)	
	return;

def parseSEX(linepersonnumber, linearray):
	if countofarrayvalues == 3: #expectedlength
		linesexpersonnumber = linearray[2]
		updatenonsexcypher = "MATCH (a:PERSON) WHERE a.personid = '" + linepersonnumber + "' SET a.sex = '" + linesexpersonnumber + "'"
		session.run(updatenonsexcypher)
	return

def parseBIRT(linepersonnumber, gedcomline):
	linebirtdescription = gedcomline[6:]
	linebirtdescription = linebirtdescription.replace("'"," ")
	linebirtdescription = linebirtdescription.strip()
	updatenonbirtdesccypher = "MATCH (a:PERSON) WHERE a.personid = '" + linepersonnumber + "' SET a.birthdescription = '" + linebirtdescription + "'"
	session.run(updatenonbirtdesccypher)
	return
	
def parseMARR(linepersonnumber, gedcomline):
	linemarrdescription = gedcomline[6:]
	linemarrdescription = linemarrdescription.replace("'"," ")
	linemarrdescription = linemarrdescription.strip()
	updatemarrcypher = "MATCH (f:FAMILY) WHERE f.familyid = '" + linefamilynumber + "' SET f.marriagedescription = '" + linemarrdescription + "'"
	session.run(updatemarrcypher)
	return

def parseDATE(linepersonnumber, gedcomline):
	adddatecypher = ""
	linedate = gedcomline[6:]
	linedate = linedate.replace("'"," ")
	linedate = linedate.strip()
	#if linecontext == "BIRT": adddatecypher = "MATCH (a:PERSON) WHERE a.personid = '" + linepersonnumber + "' SET a.birthdate = '" + linedate + "'"
	#if linecontext == "MARR": adddatecypher = "MATCH (f:FAMILY) WHERE f.familyid = '" + linefamilynumber + "' SET f.marriagedate = '" + linedate + "'"
	#if len(adddatecypher) > 0: session.run(adddatecypher)
	return linedate

def parsePLAC(linecontext,linedate, linepersonnumber, gedcomline):
	addplacecypher = ""
	lineplace = gedcomline[6:]
	lineplace = lineplace.replace("'"," ")
	lineplace = lineplace.strip()
	existingplacecypher = "MATCH (p:PLACE) WHERE p.location = '" + lineplace + "' RETURN p.place"
	placeresult = session.run(existingplacecypher)
	for record in placeresult:
		if linecontext == "BIRT": addplacecypher = "MATCH (i:PERSON) where i.personid = '" + linepersonnumber + "' match (p:PLACE) where p.location = '" + lineplace + "' CREATE (i)-[r:Born{date:'" + linedate + "'}]->(p)"
		if linecontext == "MARR": addplacecypher = "MATCH (i:PERSON) where i.personid = '" + linepersonnumber + "' match (p:PLACE) where p.location = '" + lineplace + "' CREATE (i)-[r:Married{date:'" + linedate + "'}]->(p)"
		if linecontext == "GRAD": addplacecypher = "MATCH (i:PERSON) where i.personid = '" + linepersonnumber + "' match (p:PLACE) where p.location = '" + lineplace + "' CREATE (i)-[r:Graduated{date:'" + linedate + "'}]->(p)"
		if linecontext == "RESI": addplacecypher = "MATCH (i:PERSON) where i.personid = '" + linepersonnumber + "' match (p:PLACE) where p.location = '" + lineplace + "' CREATE (i)-[r:Resided{date:'" + linedate + "'}]->(p)"
		if linecontext == "DEAT": addplacecypher = "MATCH (i:PERSON) where i.personid = '" + linepersonnumber + "' match (p:PLACE) where p.location = '" + lineplace + "' CREATE (i)-[r:Died{date:'" + linedate + "'}]->(p)"
		if len(addplacecypher) > 0: session.run(addplacecypher)
		break
	else:
		createplacecypher = "CREATE (p:PLACE {location:'" + lineplace + "'})"
		session.run(createplacecypher)
		#raise ValueError("No acceptable value in {!r:100}".format(data))
	return


prevlinepersonnumber = "@P0@"
#Begin reading GEDCOM file
gedcomfile = open("stonepark-tree.ged", "r")
for gedcomline in gedcomfile:
	linearray = formatGEDCOMLINE(gedcomline)
	countofarrayvalues = len(linearray)
	if countofarrayvalues >= 3:
		if (linearray[0] == "1"): linecontext = linearray[1]
		if (linearray[2] == "INDI"): linepersonnumber = parseINDI(linearray)
		if ((linearray[1] == "NAME") & (linearray[0] == "1") & (linepersonnumber <> prevlinepersonnumber)): 
			prevlinepersonnumber = linepersonnumber
			parseNAME(gedcomline, linepersonnumber, linearray)
		if (linearray[2] == "FAM"): linefamilynumber = parseFAM(linearray)
		if (linearray[1] == "HUSB"): parseHUSB(linefamilynumber, linearray)
		if (linearray[1] == "WIFE"): parseWIFE(linefamilynumber, linearray)
		if (linearray[1] == "CHIL"): parseCHIL(linefamilynumber, linearray)
		if (linearray[1] == "SEX"): parseSEX(linepersonnumber, linearray)
		if (linearray[1] == "BIRT"): parseBIRT(linepersonnumber, gedcomline)
		if (linearray[1] == "DATE"): linedate = parseDATE(linepersonnumber, gedcomline)
		if (linearray[1] == "PLAC"): parsePLAC(linecontext,linedate, linepersonnumber, gedcomline)
		if (linearray[1] == "MARR"): parseMARR(linepersonnumber, gedcomline)

session.close()
print("Im Done!")