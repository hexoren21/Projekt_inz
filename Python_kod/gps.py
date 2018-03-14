#!/usr/bin/python
# Filename: text.py
from bluetooth import *
import sys
import serial
import time
ser = serial.Serial("/dev/ttyS0",115200)
W_buff = ["AT+CGNSPWR=1\r\n", "AT+CGNSSEQ=\"RMC\"\r\n", "AT+CGNSINF\r\n", "AT+CGNSURC=2\r\n","AT+CGNSTST=1\r\n"]

ser.write(W_buff[0])
ser.flushInput()
data = ""
latitude = 0
longitude = 0
num = 0

def changeDMStoDD(x):
	#print x
	x = x.split(".")
	x1 = float("0." + str(int(x[1]) * 60)) * 100
	temp = x[0] # odzielanie stopni od minut
	x[1] = temp[len(temp)-2:len(temp)]
	if temp[0] == "0":
		x[0] = temp[1:len(temp)-2]
	else:
		x[0] = temp[0:len(temp)-2]
	#print x[0]
	#print x[1]
	#print x1
	temp = str(float(x[1])/60 + float(x1)/3600) #zamiana minut na stopnie dziesietne
	temp = temp[1:len(temp)] #usuwanie zera z przodu
	#print temp
	dd = x[0] + temp
	return dd

def Bluetooth(latitude, longitude):
	if sys.version < '3':

		addr = "18:00:2D:7C:5B:E6"


# search for the SampleServer service
	uuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"
	service_matches = find_service( uuid = uuid, address = addr )

	if len(service_matches) == 0:	
		print("couldn't find the SampleServer service =(")
		sys.exit(0)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print("connecting to \"%s\" on %s" % (name, host))

	# Create the client socket
	sock=BluetoothSocket( RFCOMM )
	sock.connect((host, port))

	print("connected.  type stuff")
	while True:
		data = latitude + ',' + longitude
		sock.send(data)
		break
	sock.close()
	time.sleep(10)
	return 0
#try:
while True:
		print ser.inWaiting()
		print "ser.inWaiting"
		while ser.inWaiting() > 0:
			data += ser.read(ser.inWaiting())
		if data != "":
			#print "data przed"
			print data
			if num == 4:
				data1 = data
				data1 = data1.split(",")
				if len(data1) > 3:
					print data1[1]
					print data1[2]
					print data1[4]
					if data1[2].replace('.','',1).isdigit(): #usuwa 1 przecinek, jesli beda dwa zwroci false
						if data1[4].replace('.','',1).isdigit():
							latitude = changeDMStoDD(data1[2])
							longitude = changeDMStoDD(data1[4])
							print "Szerokosc geograficzna: " + latitude
							print "Dlugosc geograficzna: " + longitude
							Bluetooth(latitude, longitude)
							break;
						else:
							print "blad odczytu (Dlugosc zla)"
					
					else:
						print "Blad odczytu (Szerokosc zla)"
			#plik_tekstowy = open('suchy_kod.txt', 'w+')
			#plik_tekstowy.write(data)
			#plik_tekstowy.close
			#print "data"
			if  num < 4:	# the string have ok
				print num 
				#print "numer"
				time.sleep(0.5)
				ser.write(W_buff[num+1])
				num = num +1
			if num == 4:
				time.sleep(0.5)
				ser.write(W_buff[4])
				#break
				#ser.close
			data = ""
			#print "kasowanie daty"
#except keyboardInterrupt:
#	if ser != None:
#		ser.close()
