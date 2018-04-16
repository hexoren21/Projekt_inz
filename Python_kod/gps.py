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
	x = x.split(".")
	x1 = float("0." + str(int(x[1]) * 60)) * 100
	temp = x[0] # odzielanie stopni od minut
	x[1] = temp[len(temp)-2:len(temp)]
	if temp[0] == "0":
		x[0] = temp[1:len(temp)-2]
	else:
		x[0] = temp[0:len(temp)-2]
	temp = str(float(x[1])/60 + float(x1)/3600) #zamiana minut na stopnie dziesietne
	temp = temp[1:len(temp)] #usuwanie zera z przodu
	dd = x[0] + temp
	return dd
def send_GPRS_to_serwer(latitude, longitude):
	W_buff = ["AT+CSTT=\"internet\"\r\n", "AT+CIICR\r\n", "AT+CIFSR\r\n", "AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",\"80\"\r\n"]
	data_send = ("GET /update?key=49TE04U3HL5ZKO8B&field1=" + latitude + "&field2=" + longitude + "\r\n")
	data_len = ("AT+CIPSEND=" + str(len(data_send)) + "\r\n")
	data=""
	ser.write(W_buff[0])
	data += ser.read(ser.inWaiting())
	time.sleep(3)
	ser.write(W_buff[1])
	data += ser.read(ser.inWaiting())
	time.sleep(3)
	ser.write(W_buff[2])
	data += ser.read(ser.inWaiting())
	time.sleep(3)
	ser.write(W_buff[3])
	data += ser.read(ser.inWaiting())
	time.sleep(3)
	ser.write(data_len)
	time.sleep(3)
	data += ser.read(ser.inWaiting())
	ser.write(data_send)
	time.sleep(1)
	while ser.inWaiting() > 0:
		data += ser.read(ser.inWaiting())
	print data
	time.sleep(3)

def send_bluetooth_to_phone(latitude, longitude):

	addr = "18:00:2D:7C:5B:E6"


# search for the SampleServer service
	uuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"
	service_matches = find_service( uuid = uuid, address = addr )

	if len(service_matches) == 0:	
		print("couldn't find the SampleServer service")
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
	time.sleep(15)
	
while True:
		print ser.inWaiting()
		while ser.inWaiting() > 0:
			data += ser.read(ser.inWaiting())
		if data != "":
			print data
			if num == 4:
				data1 = data
				data1 = data1.split(",")
				if len(data1) > 3:
					print data1[1]
					print data1[2]
					print data1[4]
					if '.' in data1[2] and data1[2].replace('.','',1).isdigit() : #usuwa 1 przecinek, jesli beda dwa zwroci false oraz liczba musi byc z przecinkiem
						if '.' in data1[4] and data1[4].replace('.','',1).isdigit():
							latitude = changeDMStoDD(data1[2])
							longitude = changeDMStoDD(data1[4])
							print "Szerokosc geograficzna: " + latitude
							print "Dlugosc geograficzna: " + longitude
							ser.write("AT+CGNSPWR=0\r\n")
							data=""
							ser.write("AT+CSQ\r\n")
							time.sleep(3)
							print ser.inWaiting()
							while ser.inWaiting() > 0:
								data += ser.read(ser.inWaiting())
							print "data przed rozdzieleniem"
							print data
							quaility_of_signal = data.split("+CSQ: ")
							quaility_of_signal_1 = quaility_of_signal[1]
							quaility_of_signal_1 = quaility_of_signal_1[0:2]
							time.sleep(1)
							print "quality of signal"
							print quaility_of_signal_1
							if quaility_of_signal_1 != 0:
								print "wysylanie danych przez GPRS" 
								send_GPRS_to_serwer(latitude, longitude)
							else:
								print "wysylanie danych przez Bluetooth"
								send_bluetooth_to_phone(latitude, longitude)
							ser.write("AT+CGNSPWR=1\r\n")
						else:
							print "Blad odczytu (Dlugosc zla)"
					
					else:
						print "Blad odczytu (Szerokosc zla)"
			if  num < 4:	# the string have ok
				print num 
				time.sleep(0.5)
				ser.write(W_buff[num+1])
				num = num + 1
			if num == 4:
				time.sleep(0.5)
				ser.write(W_buff[4])
			data = ""
			#print "kasowanie daty"

