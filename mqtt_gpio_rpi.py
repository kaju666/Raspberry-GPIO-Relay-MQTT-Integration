#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import urllib
from time import sleep
import RPi.GPIO as GPIO


#Conf GPIO Number for relays
out_1 = 18
out_2 = 23

#Conf MQTT broker
broker_ip = "192.168.8.120"
broker_port = 1883
broker_timeout = 60
topic_sub = "gBridge/u000/relay/#"
topic_out1 = "gBridge/u000/relay/led"
topic_out2 = "gBridge/u000/relay/printer"

GPIO.setmode(GPIO.BCM)
GPIO.setup(out_1, GPIO.OUT)
GPIO.output(out_1, GPIO.HIGH)
GPIO.setup(out_2, GPIO.OUT)
GPIO.output(out_2, GPIO.HIGH)

def main():
   def on_connect(client, userdata, flags, rc):
	client.subscribe(topic_sub)
   def on_message(client, userdata, msg):
	if msg.topic == topic_out1 :
		if msg.payload == "1" :
			GPIO.output(out_1, GPIO.LOW)
			sleep(.1)
			#print "OUT 1 ON"
		if msg.payload == "0" :
			GPIO.output(out_1, GPIO.HIGH)
			sleep(.1)
			#print "OUT 1 OFF"
	if msg.topic == topic_out2 :
		if msg.payload == "1" :
			GPIO.output(out_2, GPIO.LOW)
			sleep(.1)
			#print "OUT 2 ON"
		if msg.payload == "0" :
			GPIO.output(out_2, GPIO.HIGH)
			sleep(.1)
			#print "OUT 2 OFF"
	
   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message

   client.connect(broker_ip, broker_port, broker_timeout)

   client.loop_forever()

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      GPIO.cleanup()
