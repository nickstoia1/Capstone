import wave, struct, math, random

# !/usr/bin/python

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
	adc = spi.xfer2([1, (8 + channel) << 4, 0])
	data = ((adc[1] & 3) << 8) + adc[2]
	return data


# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data, places):
	volts = (data * 3.3) / float(1023)
	volts = round(volts, places)
	return volts


# TODO
def get_time():
	return 'sound'


# TODO
def read_squelch():
	return 1


def main():
	# Define sensor channels
	audio_pos_channel = 0
	audio_neg_channel = 1

	filename = get_time() + ".wav"

	datalist_pos = []
	sample_rate = 200000.0  # hertz
	obj = wave.open(filename, 'w')
	obj.setnchannels(1)  # mono
	obj.setsampwidth(2)
	obj.setframerate(sample_rate)

	squelch = 1
	while squelch:
		# read until squelch is unbroken
		for i in range(2000000):
			audio_pos = ReadChannel(audio_pos_channel)
			datalist_pos.append(audio_pos)

		squelch = 0

	for number in datalist_pos:
		data = struct.pack('<h', number)
		obj.writeframesraw(data)

	obj.close()

	print(filename + ' is made and saved!')

