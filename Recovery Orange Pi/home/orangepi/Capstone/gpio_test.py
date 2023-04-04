import OPi.GPIO as GPIO

GPIO.setmode(GPIO.SUNXI)
GPIO.setup('PL10', GPIO.IN)

if GPIO.input('PL10'):
	print("high")
else:
	print("low")


GPIO.cleanup()

