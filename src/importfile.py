#!/usr/bin/env python
#need to look for suffix varioations
#need to look for commas
#is parsing the name really needed when we have person and family@ values
import re
linepersonnumber = ""
linefamilynumber = ""
linehusbpersonnumber = ""
linewifepersonnumber = ""
linechilpersonnumber = ""


#Cleanup and parse the GEDCOM line
def formatGEDCOMLINE (gedcomline):
	gedcomline = gedcomline.replace("\n","")
	linearray = gedcomline.split(" ")
	return linearray;

#INDI - 0 @P1@ INDI
def parseINDI (linearray):
	if countofarrayvalues == 3: #expectedlength
		linepersonnumber = linearray[1]
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
		
	#nonsurname
	positionfirstslash = 0
	lengthoflinearray = len(linearray) - 1
	for num, namepart in enumerate(linearray[2:], start=2):
		#name suffix doesnt have a lsash and is last element and surname is not blank
		if ((num == lengthoflinearray) & (namepart.find("/") == -1) & (surname <> "")): namesuffix = namepart
		if ((num < lengthoflinearray) & (namepart.find("/") == -1)): nonsurname = nonsurname + namepart + " "
	print linepersonnumber
	print gedcomline
	return;
	
#FAM
#0 @F1@ FAM
#1 HUSB @P1@
#1 WIFE @P4@
#1 CHIL @P5@
def parseFAM (linearray):
	if countofarrayvalues == 3: #expectedlength
		linefamilynumber = linearray[1]
		#print linefamilynumber
	return linefamilynumber;

def parseHUSB (linefamilynumber, linearray):
	if countofarrayvalues == 3: #expectedlength
		linehusbpersonnumber = linearray[2]
	print linehusbpersonnumber + " is the husband in family " + linefamilynumber
	return;

def parseWIFE (linefamilynumber, linearray):
	if countofarrayvalues == 3: #expectedlength
		linewifepersonnumber = linearray[2]
	print linewifepersonnumber + " is the wife in family " + linefamilynumber
	return;
	
def parseCHIL (linefamilynumber, linearray):
	if countofarrayvalues == 3: #expectedlength
		linechilpersonnumber = linearray[2]
	print linechilpersonnumber + " is the child in family " + linefamilynumber
	return;


#Begin reading GEDCOM file
gedcomfile = open("stonepark-tree.ged", "r")
for gedcomline in gedcomfile:
	linearray = formatGEDCOMLINE(gedcomline)
	countofarrayvalues = len(linearray)
	if countofarrayvalues >= 3:
		if (linearray[0] == "1"): linecontext = linearray[1]
		if (linearray[2] == "INDI"): linepersonnumber = parseINDI(linearray)
		if ((linearray[1] == "NAME") & (linearray[0] == "1")): parseNAME(gedcomline, linepersonnumber, linearray)
		#if (linearray[1] == "FAMS"):
		#if (linearray[1] == "FAMC"):
		if (linearray[2] == "FAM"): linefamilynumber = parseFAM(linearray)
		if (linearray[1] == "HUSB"): parseHUSB(linefamilynumber, linearray)
		if (linearray[1] == "WIFE"): parseWIFE(linefamilynumber, linearray)
		if (linearray[1] == "CHIL"): parseCHIL(linefamilynumber, linearray)
		#if (linearray[1] == "SEX"):
		#if (linearray[1] == "BIRT"):	