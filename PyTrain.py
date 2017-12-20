#!/usr/bin/python

import paho.mqtt.client as mqtt

from netifaces import interfaces, ifaddresses, AF_INET

from grovepi import *
import grovepi
import grove_i2c_motor_driver 
import grove_128_64_oled as oled
import socket
import time


logging               = 1

light_sensor          = 0     # Light Sensor on Analog port 0
light_threshold        = 10    #initial sensor threshold

#what we subscribe to 
lifeCycleFeedback     = "lifecycle/feedback"
internalMqttConnect   = "MQTT/Connection"
shutdownControl       = "lifecycle/control/shutdown"
allFeedback           = "feedback"
actuatorPowerInternal = "actuator/power/internal"

enginePowerControl    = "engine/power/control"
engineCalibrationControl = "engine/calibration/control"

billboardImageControl = "billboard/image/control"
billboardMessageControl= "billboard/message/control"

lightsOverrideControl = "lights/override/control"
lightsCalibrationControl    = "lights/power/control"
lightsAmbientFeedback  = "lights/ambient/feedback"

# what we publish:
enginePowerFeedback   = "engine/power/feedback"
engineCalibrationFeedback = "engine/calibration/feedback"

lightsOverrideFeedback = "lights/override/feedback"
lightsPowerFeedback    = "lights/power/feedback"
lightsCalibrationFeedback  = "lights/calibration/feedback"


billboardImageFeedback = "billboard/spec/feedback"


def handlePowerControl (client, userdata, message):
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
    oled.putString("Speed:   " + str(engineSpeed))
    m.MotorSpeedSetAB(engineSpeed,engineSpeed)

def handleShutdownControl(client, userdata, message):
    print  ("shutdown requested")
    oled.clearDisplay()
    oled.setTextXY(0,3)
    m.MotorSpeedSetAB(0,0)
    oled.putString("Shutdown")
    exit()


def handleCalibrationControl(client,userdata,message):
    print("Received: Calibration Control")

def handleMQTTconnect (client,userdata,message):
    print ("Received: MQTT Connect")

def handleBillboardImage (client,userdata,message):
    print ("Received: Billboard Image")

def handleBillboardMessage (client,userdata,message):
    print ("Received: Billboard Message")
    oled.setTextXY(0,5)
    oled.putString(message.payload)
    oled.setTextXY(0,3)

def handleActuatorPowerInternal (client,userdata,message):
    print ("Received: Actuator Power Internal Message")

def handleLightsCalibration(client,userdata,message):
    print ("Received: LightsCalibration")

def handleLightsOverride(client,userdata,message):
    print ("Received: LightsOverride")

def handleAmbientFeedback(client,userdata,message):
    print ("Received: lightsAmbientFeedback")

def on_message(client, userdata, message):
    print("message client", client)
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    if message.topic == enginePowerControl:
        handlePowerControl(client,userdata,message)
    elif message.topic == shutdownControl:
        handleShutdownControl(client,userdata,message)
    elif message.topic == engineCalibrationControl:
        handleCalibrationControl(client,userdata,message)
    elif message.topic == internalMqttConnect:
        handleMQTTconnect(client,userdata,message)
    elif message.topic == billboardImageControl:
        handleBillboardImage(client,userdata,message)
    elif message.topic == billboardMessageControl:
        handleBillboardMessage(client,userdata,message)
    elif message.topic == actuatorPowerInternal:
        handleActuatorPowerInternal(client,userdata,message)
    elif message.topic == lightsCalibrationControl:
        handleLightsCalibration(client,userdata,message)
    elif message.topic == lightsOverrideControl:
        handleLightsOverride(client,userdata,message)
    elif message.topic == lightsAmbientFeedback:
        handleAmbientFeedback(client,userdata,message)


def on_log(client, userdata, level, buf):
    if logging == 1:
        print("log: ",buf)


def initDisplay():
    oled.sendCommand(0x8D)
    oled.sendCommand(0x14)

    oled.init()
    oled.clearDisplay()
    oled.setNormalDisplay()

    oled.deactivateScroll()
    oled.sendCommand(0xc8)
    oled.sendCommand(0xa1)
    oled.setHorizontalMode();
    oled.setBrightness(255);


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

grovepi.pinMode(light_sensor,"INPUT")


client_name = "Loco"
#broker = "TheJoveExpress"
broker =  "192.168.1.79"

client = mqtt.Client(client_name)

print("connecting to broker")

client.connect( broker, port=1883, keepalive=60, bind_address="")

client.on_message = on_message        #attach function to callback
client.on_log = on_log

client.loop_start()    #start the loop

client.subscribe(enginePowerControl)
client.subscribe(shutdownControl)
client.subscribe(lifeCycleFeedback)
client.subscribe(engineCalibrationFeedback)
client.subscribe(billboardImageControl)
client.subscribe(billboardMessageControl)
client.subscribe(internalMqttConnect)
client.subscribe(actuatorPowerInternal)
client.subscribe(lightsCalibrationControl)
client.subscribe(lightsOverrideControl)
client.subscribe(lightsAmbientFeedback)

oled.putString("Train Ready")

while 1:
    
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        # Calculate resistance of sensor in K
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value

        if resistance > light_threshold:
            print ("light Sensor activated")
        else:
            print ("light Sensor de-activated")

        print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
      
    except IOError:
        print ("Error")

    time.sleep(10)

   
