import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

class Lcd:
	def __init__(self, rs, e, *dataPins):
		self.RS = rs
		self.E = e
		self.dataPins = dataPins

		# Define some device constants
		self.LCD_WIDTH = 16    # Maximum characters per line
		self.LCD_CHR = True
		self.LCD_CMD = False
		self.LCD_LINES = [0x80, 0xC0] # LCD RAM address for the lines
		# Timing constants
		self.E_PULSE = 0.0005
		self.E_DELAY = 0.0005
		for pin in [self.E, self.RS, *self.dataPins]:
			GPIO.setup(pin, GPIO.OUT)
		# Initialise display
		self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
		self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
		self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
		self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
		self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
		self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
		time.sleep(self.E_DELAY)

	def lcd_byte(self, bits, mode):
		# Send byte to data pins
		# bits = data
		# mode = True  for character
		#        False for command

		GPIO.output(self.RS, mode) # RS

		# High bits
		for pin in self.dataPins:
			GPIO.output(pin, False)

		if bits&0x10==0x10:
			GPIO.output(self.dataPins[0], True)
		if bits&0x20==0x20:
			GPIO.output(self.dataPins[1], True)
		if bits&0x40==0x40:
			GPIO.output(self.dataPins[2], True)
		if bits&0x80==0x80:
			GPIO.output(self.dataPins[3], True)

		# Toggle 'Enable' pin
		self.lcd_toggle_enable()

		# Low bits
		for pin in self.dataPins:
			GPIO.output(pin, False)
			
		if bits&0x01==0x01:
			GPIO.output(self.dataPins[0], True)
		if bits&0x02==0x02:
			GPIO.output(self.dataPins[1], True)
		if bits&0x04==0x04:
			GPIO.output(self.dataPins[2], True)
		if bits&0x08==0x08:
			GPIO.output(self.dataPins[3], True)

		# Toggle 'Enable' pin
		self.lcd_toggle_enable()

	def lcd_toggle_enable(self):
		# Toggle enable
		time.sleep(self.E_DELAY)
		GPIO.output(self.E, True)
		time.sleep(self.E_PULSE)
		GPIO.output(self.E, False)
		time.sleep(self.E_DELAY)
        
	def print(self, message,line):
		# Send string to display

		message = message.ljust(self.LCD_WIDTH," ")

		self.lcd_byte(self.LCD_LINES[line - 1], self.LCD_CMD)

		for ch in message:
			self.lcd_byte(ord(ch), self.LCD_CHR)

	def clear(self):
		self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
