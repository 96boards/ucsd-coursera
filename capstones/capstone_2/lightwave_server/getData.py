#getData.py
#For waveform data
import numpy as np
import wfdb
from os import path
import os.path

global dataJ
dataJ = 0
def getData():
	global dataJ
	t0 = 0
	tf = 10000
	fileName = 'database/ecgiddb/Person_01/rec_1'
	sig, fields = wfdb.srdsamp(fileName, sampfrom=t0, sampto=tf, channels=[0])
	#print(sig)
	record = wfdb.rdsamp(fileName, sampfrom=t0, sampto=tf, channels=[0], physical=False)
	peaks_indexes = wfdb.processing.gqrs_detect(x=record.d_signals[:,0], frequency=fields['fs'],
	 				adcgain=record.adcgain[0], adczero=record.adczero[0], threshold=1.0)
	#print(peaks_indexes)
	hr = wfdb.processing.compute_hr(length=tf-t0, peaks_indexes=peaks_indexes, fs=fields['fs'])
	
	hr = hr.tolist()
	
	#print type(hr[0])
	#print np.isnan(hr)
	for i,r,nan in zip(range(len(hr)),hr,np.isnan(hr)):
		if(nan):
			hr[i] = None
	
	#print(hr)
	print(dataJ)
	if(dataJ>=len(hr)):
		dataJ = 0
	while(hr[dataJ] == None):
		dataJ += 100
		
	heartrate = hr[dataJ]
	response = {'analysis':
					{'heartrate': heartrate}
			}
	dataJ+=100
	print response
	
	return response
	

getData()

while True:
	getData()
	

