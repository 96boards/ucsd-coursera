#lightwave.py
import numpy as np
import wfdb
from os import path

#For webserver
from flask import Flask, Response
from flask import request, current_app
from flask import json
from flask_jsonpify import jsonify

#Constants
VERSION = "0.64"
DATABASE_DIR="database/"
verbose = False

def writeResponse(func):
	"""Prints response objects returned by functions.
	
	Args:
		func: Function whose output will be printed to screen.
		
	Returns:
		What the function given returns.
	"""
	
	def inner(*args, **kwargs):
		response = func(*args, **kwargs)
		if(verbose):
			print response.data
		return response
	return inner

@writeResponse
def readDatabase():
	"""Reads the database list file.
	
	Returns:
		flask.Response: List of databases as JSON.
	
	"""
	
	database_list = []									#Initilializes empty list of database
														#dictionaries.
	database_path = path.join(DATABASE_DIR, "DBS")

	with open(database_path) as database_file:
		for line in database_file:						#Reads each line of the file.
			words = line.split("\t")
			name = words[0]
			description = None
			for word in words:							#Finds second string that is not empty
				if(word != ""):
					description = word.replace("\n", "")
			database_dict = {
							"name": name,				#Creates a dict to hold data.
							"desc": description
							}
			database_list.append(database_dict)			#Add dict to the database list.
	
	response = {"database": database_list,				#Create a response dict that will become JSON.
				"version": VERSION,
				"success": True
				}
	database_response = jsonify(response)
		
	return database_response

@writeResponse			
def readAnnotators(database):
	"""Reads the annotators file.
	
	Returns:
		flask.Response: Info within ANNOTATORS file as JSON.
	
	"""
	
	annotator_list = []									#Initilializes empty list of annotator
														#dictionaries.
	annotator_path = path.join(DATABASE_DIR, database, 
							"ANNOTATORS")
	
	with open(annotator_path) as annotation_file:
		 for line in annotation_file:					#Reads each line of the file.
			words = line.split("\t")
			name = words[0]
			description = words[1]
			annotator_dict = {
							"name": name,				#Creates a dict to hold data.
							"desc": description
							}
			annotator_list.append(annotator_dict)		#Add dict to the annotator list.
	
	response = {
				"annotator": annotator_list,			#Create a response dict that will become JSON.
				"version": VERSION,
				"success": True
				}

	annotator_response = jsonify(response)
	
	return annotator_response

@writeResponse
def readRecords(database):
	"""Reads the records file.
	
	Returns:
		flask.Response: Info within RECORDS file as JSON.
	
	"""
	
	record_list = []									#Initilializes empty list of record strings.
	record_path = path.join(DATABASE_DIR,database,"RECORDS")
	
	with open(record_path) as record_file:
		 for record in record_file:						#Reads each line of the file.
			record = record.replace("\n", "")
			record_list.append(record)					#Add dict to the record list.
	
	response = {
				"record": record_list,					#Create a response dict that will become JSON.
				"success": True
				}

	record_response = jsonify(response)

	return record_response

@writeResponse
def fetchAnnotations(db, record, annotator, dt):
	"""Fetchs annotations from the annotation file *.annotator.
	
	Args:
		record (str): Record from annotations are fetched.
		annotator (str): Chooses whcih annotator to interpret the annotations.
		dt (int): Duration of the annotations.
		
	Returns:
		flask.Response: Annotations as JSON.
	"""
	dt = int(dt)
	
	annotation_path = path.join(DATABASE_DIR, db, record)
	
	annotation = wfdb.rdann(annotation_path, annotator, sampfrom=dt)
	
	annsamp = annotation.annsamp	#The annotation location in samples relative to the beginning of 
									#the record.
	anntype = annotation.anntype	#The annotation type according the the standard WFDB codes.
	subtype = annotation.subtype	#The marked class/category of the annotation.
	chan  = annotation.chan			#The signal channel associated with the annotations.
	num = annotation.num			#The labelled annotation number.
	aux = annotation.aux			#The auxiliary information string for the annotation.
	
	annotation_list = []
	
	print
	for t,a,s,c,n,x in zip(annsamp, anntype, subtype, chan, num, aux):
		if(x == ''):
			x = None
		annotation = {
						"t": t,
						"a": a,
						"s": s,
						"c": c,
						"n": n,
						"x": x }
		annotation_list.append(annotation)
	
		
	response = {
				"fetch":
					{"annotator":
						[
							{"name": annotator,
							"annotation": annotation_list
							}
						]
					}
				}
				
	
	annotation_response = jsonify(response)
	
	return annotation_response

@writeResponse
def readInfo(database, record):
	"""Reads the header file of the given record.
	
	Args:
		db (str): Name of the database.
		record (str): Name of the record.
	
	Returns:
		flask.Response: Info of the record in JSON.
	"""
	
	#Get path of signal.
	signal_path = annotation_path = path.join(DATABASE_DIR, database, record)
	
	record_samples = wfdb.rdsamp(signal_path, physical=False)

	
	note_list = []										#Initilializes empty list of note strings.
	info_path = path.join(DATABASE_DIR,database,
						record + ".hea")
	
	response = {										#Create a response dict that will become JSON.
				"info": {"db": database,
						"record": record,
						"start": None,
						"end": None,
						"signal": [
									{
									"tps": 1,
       								"units": None
									},
									{
									"tps": 1,
       								"units": None
									}
								]
						},					
				"success": True
				}
	
	with open(info_path) as info_file:
		i=0
		for line in info_file:								#Reads each line of the file.
		 	if(line == '\n'):
		 		continue
		 	if(i == 0):
		 		words = line.split(" ")
		 		record_name = words[0]
		 		num_signals = int(words[1])
		 		samp_freq = float(words[2])
		 		num_samples = float(words[3].replace('\n',''))
		 		seconds = num_samples / samp_freq
		 		m, s = divmod(seconds, 60.0)
				h, m = divmod(m, 60)
		 		duration = "%02d:%02.3f" % (m, s)
		 		
		 		info = response["info"]
		 		info["tfreq"] = samp_freq
		 		info["duration"] = duration
		 		
		 	elif(line[0] != '#'):
		 		words = line.split(" ")
		 		sample_file = words[0]
		 		signal_format = int(words[1])
		 		gain = int(words[2])
		 		adcres = int(words[3])
		 		adczero = int(words[4])
		 		baseline = int(words[7])
		 		description = " ".join(words[8::]).replace("\n","")
		 		
		 		signal = response["info"]["signal"][i-1]
		 		signal["name"] = description.replace('\r', '')
		 		signal["gain"] = gain
		 		signal["adcres"] = adcres
		 		signal["adczero"] = adczero
		 		signal["baseline"] = baseline
			elif(line[0] == '#'):
				note = line[1::].replace('\n', '').replace('\r', '')
				note_list.append(note)
		 	i+=1
		 
	response["info"]["notes"] = note_list
	
	names = record_samples.signame
	units_list = record_samples.units
	gains = record_samples.adcgain
	baselines = record_samples.baseline
	adcres_list = record_samples.adcres
	adczero_list = record_samples.adczero
	
	#Writes all remaining attributes of record
	write = False
	if(write):
		r = record_samples
		attrs = vars(r)
		print(', '.join("%s: %s" % item for item in attrs.items()))
		
	
	for signal,name,units,gain,base,adcres,adczero in zip(
				response["info"]["signal"], names, units_list, gains, baselines, adcres_list,
					adczero_list):
		signal["name"] = name
		signal["units"] = units
		signal["gain"] = gain
		signal["baseline"] = base
		signal["adcres"] = adcres
		signal["adczero"] = adczero


	info_response = jsonify(response)

	return info_response

@writeResponse	
def fetchSignals(database, record, t0, dt):
	"""Fetch signal samples.
	
	Args:
	
	Return:
		flask.Response: Signal samples in JSON.
	"""
	
	#Get path of signal.
	signal_path = annotation_path = path.join(DATABASE_DIR, database, record)

	#Get the sampling frequency of the signal (samples/sec).
	signals, fields = wfdb.srdsamp(signal_path)
	samp_freq = fields["fs"]
	
	#Calculates start and end sample position.
	end = int((t0+dt) * samp_freq)
	start = int(t0 * samp_freq)
	

	
	record_samples = None
	try:
		record_samples = wfdb.rdsamp(signal_path, sampfrom=start, sampto=end, physical=False)
	except ValueError:
		record_samples = wfdb.rdsamp(signal_path, sampfrom=start, physical=False)
	
	digital_samp = record_samples.d_signals
	
	digital_samp_list = []
	for i in range(len(digital_samp[0])):
		samples = digital_samp[:,i]
		samples_differenced = differenceSignal(samples)
		digital_samp_list.append(samples_differenced)
	

		
	response = { 
			"fetch":
				{ 
				"signal":
				    [
						{ 
						"tps": 1,
						"scale": 1
						},
						{
						"tps": 1,
						"scale": 1
						}
					]
				}
	}
	
	names = record_samples.signame
	units_list = record_samples.units
	gains = record_samples.adcgain
	baselines = record_samples.baseline
	
	for signal,name,units,gain,base,samp in zip(
				response["fetch"]["signal"], names, units_list, gains, baselines, digital_samp_list):
		signal["name"] = name
		signal["units"] = units
		signal["t0"] = start
		signal["tf"] = end
		signal["gain"] = gain
		signal["base"] = base
		signal["samp"] = samp

	signal_response = jsonify(response)

	return signal_response

def differenceSignal(record):
	recordData = []
	for sample in record:
		recordData.append(int(sample))
	
	for i in reversed(range(len(recordData))):
		if(i == 0):
			continue
		else:
			recordData[i] = recordData[i] - recordData[i-1]
	return recordData

@writeResponse
def errorHandler(error):
	response = {
				"success": False,
				"error": error
	}
	
	return jsonify(response)


