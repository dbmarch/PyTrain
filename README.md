# Setting up the PI:

Instructions to setup the PI to run the MQTT client in python talking to the Mosquitto broker.
You can control the train by publishing MQTT commands.  

Load Raspian
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install build-essential 

Configure raspi-config to enable the I2C, camera, ssh, etc
    sudo raspi-config

## 1) Install Dexter Libraries:


Install Grove PI Libraries from Dexter: (PYTHON)

Setting up the PI:

    sudo curl -kL dexterindustries.com/update_grovepi | bash

    sudo reboot


## 2) Install MQTT Client Python libraries:

---
git clone https://github.com/eclipse/paho.mqtt.python
cd paho.mqtt.python
sudo python setup.py install
---

Useful links:

a) https://pypi.python.org/pypi/paho-mqtt

b) https://www.eclipse.org/paho/downloads.php


## 3) Install MQTT Broker and Mosquitto:

    sudo mosquitto -v -c /etc/mosquitto/mosquitto.conf

## 4) Some useful Python Libaries:

    sudo pip install netifaces


## 5) Misc Info on Open Edge
defaultTelemetryPort = 8098

Starting a GL application:
--t False               <Turns off TLS>
--s path_to_webpage     <
java -jar example.jar --t False --s ./demoSite/index.html --p 8080

To Skip Tests when building code 
-Dmaven.test.skip=true

To remove old installed libraries
cd
rm .m2 -Rf



## 6) Commands to connect to your target from linux console:

ssh -l pi 192.168.1.79


## 7) Install Mosquitto Broker

[Setting up MQTT on PI](https://learn.adafruit.com/diy-esp8266-home-security-with-lua-and-mqtt/configuring-mqtt-on-the-raspberry-pi)

----
>// Install MQTT Mosquitto
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get dist-upgrade
    sudo apt-get install mosquitto mosquitto-clients python-mosquitto
----

To startup the mosquitto server:

In foreground in separate window:

    sudo mosquitto -v -c /etc/mosquitto/mosquitto.conf

As daemon:

    sudo mosquitto -v -d -c /etc/mosquitto/mosquitto.conf

to kill background mosquitto :


    sudo kill $(ps aux |awk '/mosquitto/ {print $2}')


## 8) If you can't install successfully, , build and install the mosquitto broker

See [Building MQTT Broker](http://goochgooch.co.uk/2014/08/01/building-mosquitto-1-4/)

----
Install libwebsockets

Option 1: build instructions for an newer version…

    sudo apt-get install cmake libssl-dev
    cd <SRC>   # i.e. your source code home

    wget http://git.warmcat.com/cgi-bin/cgit/libwebsockets/snapshot/libwebsockets-1.3-chrome37-firefox30.tar.gz

    tar -xzvf libwebsockets-1.3-chrome37-firefox30.tar.gz
    cd libwebsockets-1.3-chrome37-firefox30/
    mkdir build
    cd build
    cmake .. -DOPENSSL_ROOT_DIR=/usr/bin/openssl
    make
    sudo make install
----

## Install git tools

    sudo apt-get install git    

Clone the Mosquitto repo and switch to the 1.4 branch

    cd <SRC>   # i.e. your source code home

----
    cd mosquitto/
    git clone https://git.eclipse.org/r/mosquitto/org.eclipse.mosquitto
    cd org.eclipse.mosquitto/
    git checkout origin/1.4
make it

First edit config.mk and ensure that the websockets option is set to “yes”.

WITH_WEBSOCKETS:=yes

Then install pre-reqs:-

    sudo apt-get install uuid-dev xsltproc docbook-xsl

And then…

    make
    make test
    sudo make install

If need be, edit or create your config file and create the service user ID.

    sudo vi /etc/mosquitto/mosquitto.conf
    sudo useradd -r -m -d /var/lib/mosquitto -s /usr/sbin/nologin -g nogroup mosquitto

Then start it up…

    sudo /usr/local/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf

And you’re done.


## 9) Useful blog on using Paho mosquitto.

[Paho Blog](http://www.steves-internet-guide.com/client-objects-python-mqtt/)

## 10) Download FileZilla to upload files to PI:
https://wiki.filezilla-project.org/Client_Installation


## 11) Install python tools

----
    sudo apt-get install python-pip python-dev 

## 12) Markdown

[viewer](http://markdownlivepreview.com/)
[cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
