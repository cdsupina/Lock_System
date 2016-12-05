from flask import Flask,request
from twilio import twiml
import time
import RPi.GPIO as GPIO
import random

relay = 12
code = ""

app = Flask(__name__)

@app.route('/sms',methods=['POST'])

def sms():
	number = request.form['From']
	message_body = request.form['Body']

	resp = twiml.Response()

	if message_body == str(code):
		print("changing lock")
		GPIO.output(relay, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(relay, GPIO.LOW)
		resp.message("Activate...")
	else:
		print("unrecognized command")
		resp.message("Unrecognized command sent.")


	return str(resp)

def generateCode(digits = 4):
	result = ""
	i = 0	
	while i < digits:
		result+=str(random.randrange(10))
		i+=1
	return result





if __name__ == '__main__':
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(relay, GPIO.OUT)
	GPIO.output(relay, GPIO.LOW)
	code = generateCode()
	print(code)
	app.run()
