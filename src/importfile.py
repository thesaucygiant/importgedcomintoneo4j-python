#!/usr/bin/env python

import re



#Cleanup and parse the GEDCOM line
def formatGEDCOMLINE (gedcomline):
	gedcomline = gedcomline.replace("\n","")
	linearray = gedcomline.split(" ")
	return linearray;

#INDI - 0 @P1@ INDI
def parseINDI (linearray):
	if countofarrayvalues == 3: #expectedlength
		linepersonnumber = linearray[1]
		print(linepersonnumber)
	return;
	
def parseNAME (linearray):
	#Detemine how many names
	namecount = len(linearray) - 2
	for num, namepart in enumerate(linearray, start=2):
		indexofforwardslashes = namepart.find("/") #Surname has slashes
		if (indexofforwardslashes == 0): #this is a surname field
			print(namepart)
	return;

#Begin reading GEDCOM file
gedcomfile = open("stonepark-tree.ged", "r")
for gedcomline in gedcomfile:
	linearray = formatGEDCOMLINE(gedcomline)
	countofarrayvalues = len(linearray)
	if countofarrayvalues >= 3:
		if (linearray[0] == "1"): linecontext = linearray[1]
		if (linearray[2] == "INDI"): parseINDI(linearray)
		if (linearray[1] == "NAME"): parseNAME(linearray)
		#if (linearray[1] == "FAMS"):
		#if (linearray[1] == "FAMC"):
		#if (linearray[1] == "FAM"):
		#if (linearray[1] == "HUSB"):
		#if (linearray[1] == "WIFE"):
		#if (linearray[1] == "CHIL"):
		#if (linearray[1] == "SEX"):
		#if (linearray[1] == "BIRT"):	