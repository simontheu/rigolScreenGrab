import time
import socket
import sys
import struct
import subprocess

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
port = 5555
scope_address = ('192.168.1.65', port)

sock.settimeout(1)
sock.connect(scope_address)

sock.sendall('*IDN?\r'.encode())
out = sock.recv(1000)
print (out)

time_str = time.time()
time_ms = int(time_str)


argc = len(sys.argv)

delay = 0
if argc > 0:
	delay = int(sys.argv[1])
	print ("Will delay " + str(delay) + " second(s) after finishing")


time_ms_bmp = str(time_ms) + ".bmp"
time_ms_png = str(time_ms) + ".png"
print(time_ms)
with open(time_ms_bmp, "wb") as binary_file:
	sock.sendall(':DISP:DATA?\r'.encode())
	ascii_header = sock.recv(2)
	size = sock.recv(ascii_header[1] - 48)

	size_str = size.decode("utf-8")
	print("Size: " + size_str)
	
	print("Receiving...")
	rxd_chars = 0
	
	print("Done")
     
	rxd_bytes = 0
	fragments = []
	
	img = bytearray()
	while rxd_bytes < int(size):
		rx_byte = sock.recv(1)
		img.extend(rx_byte)
		rxd_bytes += 1
	
	binary_file.write(img)
	binary_file.close()

#use image magick to convert from .bmp to png

call = "magick " + time_ms_bmp + " " + time_ms_png
subprocess.call(call, shell=True)
call = "del *.bmp"
subprocess.call(call, shell=True)
sock.close()

#sleep for delay seconds
if delay > 0:
	print("Waiting " + str(delay) + " second(s)..")
	time.sleep(delay)

