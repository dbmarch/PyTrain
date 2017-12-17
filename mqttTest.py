
import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	print("message retain flag=",message.retain)


def on_log(client, userdata, level, buf):
	print("log: ",buf)
	

client_name = "Loco"
#broker = "TheJoveExpress"
broker =  "192.168.1.79"

client = mqtt.Client(client_name)

print("connecting to broker")

client.connect( broker, port=1883, keepalive=60, bind_address="")

client.on_message = on_message        #attach function to callback
client.on_log = on_log

client.loop_start()    #start the loop

client.publish("house/light","ON")

print("Subscribing to topic","house/bulbs/bulb1")

client.subscribe("house/bulbs/bulb1")

print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")

client.loop_stop()


