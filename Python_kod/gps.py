#!/usr/bin/python
# Filename: text.py
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
	ser.write("AT+BTPOWER=1\r\n")
	ser.write("AT+BTHOST?\r\n")
	data2=""
	print ser.inWaiting()
	while ser.inWaiting() > 0:
		data2 += ser.read(ser.inWaiting())
	print data2	
	ser.write("AT+CGNSPWR=0\r\n")
	ser.write("AT+BTSCAN=1,10\r\n")
	data2 =""
	#szukanie stacji bluetooth przez 30s
	timeout = time.time() + 11
	while True:
		data2 += ser.read(ser.inWaiting())
		szukany_wyraz = "Xperia S"
		if time.time() > timeout:
			break
	print "Wyswietlenie zawrtosci bluetooth"
	print data2
	print "Po bluetooth"
	if szukany_wyraz in data2:
		data2 = data2.split("+BTSCAN: ")
		for j in range(0, len(data2)):
			print data2[j]
		#print len(data2)
		for i in range(len(data2)):
			if szukany_wyraz in data2[i]:
				print "znalazl wyraz w:\n+BTSCAN:" + data2[i] + "\ni ma wartosc = " + str(i)
				data2=""	
				W_buff1 ="AT+BTPAIR=0,"+str(i)+"\r\n"
				print W_buff1
				time.sleep(0.5)
				print "wpisanie polaczenia z urzadzeniem"
				#ser.write("AT+BTPAIR=0,1\r\n")
				#while ser.inWaiting() > 0:
					#data2 += ser.read(ser.inWaiting())
				print "wpsanie polaczenia sparowanie"
				ser.write("AT+BTPAIR=1,1\r\n")
				while ser.inWaiting() > 0:
					data2 += ser.read(ser.inWaiting())
				#timeout = time.time() + 100
				#while True:
					#data2 += ser.read(ser.inWaiting())
				#	if time.time() > timeout:
						#break	
				print data2
	print data2
				
	
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
