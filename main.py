
# !/usr/bin/python
import OPi.GPIO as GPIO
import wave, struct, math
import spidev
import time
import os
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()


# Open SPI bus
spi = spidev.SpiDev()
spi.open(1, 0)
spi.max_speed_hz = 10000000
# Define sensor channels
audio_pos_channel = 0
# Setup GPIO Pins
GPIO.setmode(GPIO.SUNXI)
GPIO.setup('PL10', GPIO.IN)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def read_channel(channel):
	adc = spi.xfer2([1, (8 + channel) << 4, 0])
	data = ((adc[1] & 3) << 8) + adc[2]
	return data

# Gets the current time and adds it to mnt path as string
def get_time():
	# datetime object containing current date and time
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")
	return '/mnt/' + dt_string


def main():
	while True:
		# Wait until Squelch Breaks
		if GPIO.input('PL10'):
			# get the file name which is the time and date
			filename = get_time() + ".wav"
			# setup for data reading
			datalist_audio = []
			sample_rate = 20000.0  # hertz
			obj = wave.open(filename, 'w')
			obj.setnchannels(1)  # mono
			obj.setsampwidth(2)
			obj.setframerate(sample_rate)

			# read until squelch is unbroken
			while GPIO.input('PL10'):
				audio_pos = read_channel(audio_pos_channel) * 10
				datalist_audio.append(audio_pos)

			# write data to wave file
			for number in datalist_audio:
				data = struct.pack('<h', number)
				obj.writeframesraw(data)

			obj.close()

			print(filename + ' is made and saved!')


if __name__ == "__main__":
	main()

