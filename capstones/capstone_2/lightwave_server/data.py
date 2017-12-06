#data.py

#For waveform data
import numpy as np
import wfdb
from os import path
import os.path

#For webserver
from flask import Flask, Response
from flask import request, current_app
from flask import json
from flask_jsonpify import jsonify


def getData(database, record):
	fileName = path.join('database',database,record)
	
	record = wfdb.rdsamp(fileName, channels=[0], physical=False)
	
	signal = record.d_signals[:,0]
	length = len(signal)
	
	peaks_indexes = wfdb.processing.gqrs_detect(x=signal, frequency=record.fs,
	 				adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
	 				
	hr = wfdb.processing.compute_hr(length=length, peaks_indexes=peaks_indexes, fs=record.fs)
	
	hr = hr.tolist()
	
	for i,r,nan in zip(range(len(hr)),hr,np.isnan(hr)):
		if(nan):
			hr[i] = None
		
	response = {'analysis':
					{'heartrate': hr},
				'success': True
			}
	
	
	return jsonify(response)
	
if(__name__ == '__main__'):
	print(getData())
