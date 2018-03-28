#!/usr/bin/python
# Filename: text.py
from firebase import firebase
import time
firebase = firebase.FirebaseApplication('https://lokalizacja-gps.firebaseio.com/Users58de49ab6bb5a502', None)


#result = firebase.post('/RaspberryPi',data={"18-03-2018 at 14:32":"wspolrzedne"})
data = time.strftime("%Y-%m-%d at ", time.localtime())
print data
czas = time.strftime("%H:%M", time.localtime())
czas = czas.split(':')
if int(czas[0]) >= 22: 
	czas[0] = int(czas[0]) + 2 - 24
else:
	czas[0] = int(czas[0]) + 2
data_calosc = "{0}{1}:{2}".format(data,czas[0],czas[1])
print data_calosc
result = firebase.post('/RaspberryPi',data={data_calosc:"wspolrzedne"})