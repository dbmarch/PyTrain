#!/usr/bin/python

import paho.mqtt.client as mqtt

from netifaces import interfaces, ifaddresses, AF_INET

from grovepi import *
import grove_i2c_motor_driver 
import grove_128_64_oled as oled
import socket
import time

#what we subscribe to 
lifeCycleFeedback     = "lifecycle/feedback"
internalMqttConnect   = "MQTT/Connection"
shutdownControl       = "lifecycle/control/shutdown"
allFeedback           = "feedback"
actuatorPowerInternal = "actuator/power/internal"

enginePowerControl    = "engine/power/control"
engineCalibrationControl = "engine/calibration/control"

billboardImageControl = "billboard/image/control"

# what we publish:
enginePowerFeedback   = "engine/power/feedback"
engineCalibrationFeedback = "engine/calibration/feedback"

lightsOverrideFeedback = "lights/override/feedback"
lightsPowerFeedback    = "lights/power/feedback"
lightsCalibrationFeedback  = "lights/calibration/feedback"

billboardImageFeedback = "billboard/spec/feedback"


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    if message.topic == enginePowerControl:
        engineSpeed = int(message.payload.decode("utf-8"))
        print (message.payload.decode("utf-8"))
        print (engineSpeed)
        if engineSpeed < 0:
            m.MotorDirectionSet(0b0101) #'0b0101" reverses polarity of motor.
        else:
            m.MotorDirectionSet(0b1010) #"0b1010" defines the output polarity, "10" means the M+ is "positive" while the M- is "negtive"

        engineSpeed = abs(engineSpeed)        

        if engineSpeed > 100:
            engineSpeed = 100    

        print ("Setting engine speed to ", engineSpeed)
        oled.clearDisplay()
        oled.setTextXY(0,3)
        oled.putString("Speed" + str(engineSpeed))
        m.MotorSpeedSetAB(engineSpeed,engineSpeed)
    if message.topic == shutdownControl:
        print  ("shutdown requested")
        oled.clearDisplay()
        oled.setTextXY(0,3)
        m.MotorSpeedSetAB(0,0)
        oled.putString("Shutdown")
        exit()



def on_log(client, userdata, level, buf):
    print("log: ",buf)


def initDisplay():
    brightness = 255

    #Start and initialize the OLED

    oled.sendCommand(0x8D)
    oled.sendCommand(0x14)

    oled.init()
    oled.clearDisplay()
    oled.setNormalDisplay()

    oled.deactivateScroll()
    oled.sendCommand(0xc8)
    oled.sendCommand(0xa1)
    oled.setHorizontalMode();
    oled.setBrightness(brightness);


def outputIpAddress():
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



# Program starts here
try:

    # You can initialize with a different address too: grove_i2c_motor_driver.motor_driver(address=0x0a)
    m= grove_i2c_motor_driver.motor_driver()
    m.MotorDirectionSet(0b1010) #"0b1010" defines the output polarity, "10" means the M+ is "positive" while the M- is "negtive"
    m.MotorSpeedSetAB(0,0)


except IOError:
    print("Unable to find the motor driver, check the addrees and press reset on the motor driver and try again")

initDisplay()
oled.clearDisplay()
oled.setTextXY(0,3)

client_name = "Loco"
#broker = "TheJoveExpress"
broker =  "192.168.1.79"

client = mqtt.Client(client_name)

print("connecting to broker")

client.connect( broker, port=1883, keepalive=60, bind_address="")

client.on_message = on_message        #attach function to callback
client.on_log = on_log

client.loop_start()    #start the loop

oled.clearDisplay()

client.subscribe(enginePowerControl)
client.subscribe(shutdownControl)

while 1:
    time.sleep(10)


   
