import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

class Keypad:
	def __init__(self, keys, rowPins, colPins, Lcd):
		self.ROW = rowPins
		self.COL  = colPins
		self.keys = keys
		self.Lcd = Lcd
		self.key = set()
		for j in range(4):
			GPIO.setup(self.COL[j], GPIO.OUT)
			GPIO.output(self.COL[j], 1)

		for i in range(4):
			GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def getKey(self):
		for i in range(4):
			GPIO.output(self.COL[i], 0)
			for j in range(4):
				if GPIO.input(self.ROW[j]) == 0:
					self.key.clear()
					self.key.add(self.keys[j][i])
					end = time.time() + 1
					while GPIO.input(self.ROW[j]) == 0 and time.time() < end:
						pass
			GPIO.output(self.COL[i], 1)
		if self.key:
			return self.key.pop()

