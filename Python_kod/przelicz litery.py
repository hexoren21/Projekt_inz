import serial
import time
ser = serial.Serial("/dev/ttyS0",115200)
W_buff = ["AT+CSTT=\"internet\"\r\n", "AT+CIICR\r\n", "AT+CIFSR\r\n", "AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",\"80\"\r\n","AT+CIPSEND=58\r\n"]
wartosc = "GET /update?key=49TE04U3HL5ZKO8B&field1=0.30&field2=0.40\r\n"
ser.write("AT+CGNSPWR=0\r\n")
ser.write(W_buff[0])
ser.flushInput()
data=""
print ser.inWaiting()
data += ser.read(ser.inWaiting())
time.sleep(3)
ser.write(W_buff[1])
print ser.inWaiting()
data += ser.read(ser.inWaiting())
time.sleep(3)
ser.write(W_buff[2])
print ser.inWaiting()
data += ser.read(ser.inWaiting())
time.sleep(3)
ser.write(W_buff[3])
print ser.inWaiting()
data += ser.read(ser.inWaiting())
time.sleep(3)
ser.write(W_buff[4])
print ser.inWaiting()
time.sleep(3)
data += ser.read(ser.inWaiting())
ser.write(wartosc)
while ser.inWaiting() > 0:
	data += ser.read(ser.inWaiting())
print data
time.sleep(3)