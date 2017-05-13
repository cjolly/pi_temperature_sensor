import os
import sys
import glob
import time
import datetime
import sqlite3
import atexit

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

connection = sqlite3.connect('temp_sensor.db')
connection.row_factory = sqlite3.Row
atexit.register(connection.close)
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS readings (temperature_f NUMERIC, temperature_c NUMERIC, created_at TEXT)')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f

def output():
	cursor.execute("""SELECT round(temperature_f, 2) AS temperature_f FROM readings ORDER BY created_at DESC LIMIT 1""")
	last_reading = cursor.fetchone()

	os.system('clear')	
	print('Last reading: ' + str(last_reading['temperature_f']))

while True:
	temp_c, temp_f = read_temp()
	
	cursor.execute("""INSERT INTO readings (temperature_c, temperature_f, created_at) values((?), (?), datetime('now'))""", (temp_c, temp_f))
	connection.commit()
	output()
	time.sleep(60)

