import os
import sys
import uuid
import hashlib
import zipfile
import datetime

import mariqt.variables as miqtv


def assertExists(path):
	""" Asserts that a file/folder exists and otherwise terminates the program"""
	if not os.path.exists(path):
		raise NameError("Could not find: " + path)


def assertSlash(path):
	""" Asserts that a path string to a directory ends with a slash"""
	#if not os.path.isdir(path):
	#	return path
	if not path[-1] == "/":
		return path + "/"
	else:
		return path


def humanReadable(val):
	""" Turns a number > 0 (int/float) into a shorter, human-readable string with a size character (k,M,G,...)"""

	sign = 1
	if val < 0:
		sign = -1
		val *= -1

	if val < 1:
		suffixes = ['m','µ','n','p','a','f']
		idx = -1
		while val < 0.001:
			val *= 1000
			idx += 1
		if idx >= 0:
			return str(sign*round(val))+suffixes[idx]
		else:
			return str(sign*val)
	else:
		suffixes=['k','M','G','T','P','E']
		idx = -1
		while val > 1000:
			val /= 1000
			idx += 1
		if idx >= 0:
			return str(sign*round(val))+suffixes[idx]
		else:
			return str(sign*val)

def uuid4():
	""" Returns a random UUID (i.e. a UUID version 4)"""
	return uuid.uuid4()


def is_valid_uuid(value):
	""" Retruns whether value is a valid UUIV version 4"""
	try:
		uuid.UUID(str(value), version=4)
		return True
	except ValueError:
		return False


def sha256HashFile(path):
	""" Returns the SHA256 hash of the file at path"""
	sha256_hash = hashlib.sha256()
	with open(path,"rb") as f:
		for byte_block in iter(lambda: f.read(4096),b""):
			sha256_hash.update(byte_block)
		return sha256_hash.hexdigest()

def md5HashFile(path):
	""" Returns the MD5 hash of the file at path"""
	md5_hash = hashlib.md5()
	with open(path, "rb") as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			md5_hash.update(byte_block)
	return md5_hash.hexdigest()


def rgb2hex(r,g,b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def parseFileDateTimeAsUTC(fileName:str):
	""" Parses date time from from file name according to file naming convention <event>_<sensor>_<date>_<time>.<ext>
	with date fromat yyyymmdd and time format HHMMSS[.f] with [] being optional"""

	split = fileName.split("_")
	try:
		pos = split[-1].rfind(".")
		dt_str = split[-2]+"_"+split[-1][0:pos] + "+0000"
	except:
		raise Exception("can not parse time from file name " + fileName)
	
	try:
		dt = datetime.datetime.strptime(dt_str,miqtv.date_formats['mariqt_files']+".%f%z")
	except:
		try:
			dt = datetime.datetime.strptime(dt_str,miqtv.date_formats['mariqt_files']+"%z")
		except:
			raise Exception("can not parse time from file name " + fileName)
	return dt


def recursivelyUpdateDicts(oldDict:dict, newDict:dict, mutuallyExclusives:list=[]):
	""" Recursively updates oldDict with newDict """
	log = []
	for newItem in newDict:
		if (not newItem in oldDict) or (not isinstance(newDict[newItem],dict) or (not isinstance(oldDict[newItem],dict))):
			oldDict[newItem] = newDict[newItem]
			log += checkMutuallyExclusive(mutuallyExclusives,oldDict,newDict,newItem)
		else:
			log += recursivelyUpdateDicts(oldDict[newItem],newDict[newItem],mutuallyExclusives)
	return log

def checkMutuallyExclusive(mutuallyExclusives:list,oldDict:dict,newDict:dict,newItem:str):
	""" expects a list of lists with mutually exclusive field names """
	log = []
	for mutuallyExclusive in mutuallyExclusives:
		if len(mutuallyExclusive) != 0:
			if newItem in mutuallyExclusive and newDict[newItem] != "":
				toExclude = [e for e in mutuallyExclusive if e != newItem]
				for exclude in toExclude:
					if exclude in oldDict:
						oldDict[exclude] = ""
						log.append("Removed field " + exclude + " since mutually exclusive to added field " + newItem)
	return log

def recursivelyRemoveEmptyFields(oldDict:dict):
	""" Return a dict in which all fields in all levels of oldDict that have empty string values are removed """
	newDict =  {k: v for k, v in oldDict.items() if v != ""}
	for item in newDict:
		if isinstance(newDict[item],dict):
			newDict[item] = recursivelyRemoveEmptyFields(newDict[item])
	return newDict