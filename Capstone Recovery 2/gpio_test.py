import OPi.GPIO as GPIO

GPIO.setmode(GPIO.SUNXI)
GPIO.setup('PD15', GPIO.IN)

if GPIO.input('PD15'):
	print("high")
else:
	print("low")


GPIO.cleanup()
