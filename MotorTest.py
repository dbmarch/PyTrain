#!/usr/bin/python

import paho.mqtt.client as mqtt


from netifaces import interfaces, ifaddresses, AF_INET

from grovepi import *
import grove_i2c_motor_driver 
import grove_128_64_oled as oled
import socket
import time


def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	print("message retain flag=",message.retain)


def on_log(client, userdata, level, buf):
	print("log: ",buf)



brightness = 255

#Start and initialize the OLED

oled.sendCommand(0x8D)
oled.sendCommand(0x14)

oled.init()
oled.clearDisplay()
oled.setNormalDisplay()

oled.deactivateScroll()
#oled.sendCommand(0xa0)
oled.sendCommand(0xc8)

oled.sendCommand(0xa1)
#oled.sendCommand(0xC0)

#oled.setInverseDisplay();
#oled.setPageMode();
oled.setHorizontalMode();
oled.setBrightness(brightness);


try:

    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        print '%s: %s' % (ifaceName, ', '.join(addresses))
        myIP= '.'.join(addresses)
        oled.setTextXY(0,1)
        oled.putString (ifaceName)
        oled.setTextXY(0,3)
        oled.putString (myIP)
        time.sleep(2)
        oled.clearDisplay()
    

except (IOError, TypeError) as e:
   print ("Error");

time.sleep(.1)


try:
	# You can initialize with a different address too: grove_i2c_motor_driver.motor_driver(address=0x0a)
	m= grove_i2c_motor_driver.motor_driver()

	#FORWARD
	print("Forward")
	oled.PutString ("Forward")
	m.MotorSpeedSetAB(100,100)	#defines the speed of motor 1 and motor 2;
	m.MotorDirectionSet(0b1010)	#"0b1010" defines the output polarity, "10" means the M+ is "positive" while the M- is "negtive"
	time.sleep(2)

	oled.clearDisplay()

	#BACK
	oled.PutString ("Back")
	print("Back")
	m.MotorSpeedSetAB(100,100)
	m.MotorDirectionSet(0b0101)	#0b0101  Rotating in the opposite direction
	time.sleep(2)
	oled.clearDisplay()

	#STOP
	print("Stop")
	oled.PutString("Stop")
	m.MotorSpeedSetAB(0,0)
	time.sleep(1)
	oled.clearDisplay()

	#Increase speed
	for i in range (100):
		print("Speed:",i)
		oled.setTextXY(0,3)
		oled.PutString("Speed" + i)
		m.MotorSpeedSetAB(i,i)
		time.sleep(.02)
		
	print("Stop")
	m.MotorSpeedSetAB(0,0)	
	
except IOError:
	print("Unable to find the motor driver, check the addrees and press reset on the motor driver and try again")
	