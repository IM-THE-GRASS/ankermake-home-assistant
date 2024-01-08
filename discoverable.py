#!/usr/bin/env python3
import paho.mqtt.publish
auth = {'username':"PUT YOUR USERNAME HERE",'password':"PUT YOUR PASSOWRD HERE"}
paho.mqtt.publish.single("homeassistant/sensor/sensorNozzle/config",
"""
{
   "device_class":"temperature",
   "state_topic":"homeassistant/sensor/sensorNozzle/state",
   "unit_of_measurement":"°C",
   "value_template":"{{ value_json.temperature}}",
   "unique_id":"nozzle01",
   "device":{
      "identifiers":[
         "nozzle01"
      ],
      "name":"Nozzle temperature"
   }
}
"""
, hostname="192.168.1.144",port=1883, auth= auth)
paho.mqtt.publish.single("homeassistant/sensor/sensorHeatbed/config",
"""
{
   "device_class":"temperature",
   "state_topic":"homeassistant/sensor/sensorHeatbed/state",
   "unit_of_measurement":"°C",
   "value_template":"{{ value_json.temperature}}",
   "unique_id":"heatbed01",
   "device":{
      "identifiers":[
         "heatbed01"
      ],
      "name":"Bed temperature"
   }
}
"""
, hostname="192.168.1.144",port=1883, auth= auth)
paho.mqtt.publish.single("homeassistant/sensor/sensorTimeElapsed/config",
"""
{
   "device_class":"duration",
   "state_topic":"homeassistant/sensor/sensorTimeElapsed/state",
   "unit_of_measurement":"s",
   "value_template":"{{ value_json.duration}}",
   "unique_id":"TimeElapsed01",
   "device":{
      "identifiers":[
         "TimeElapsed01"
      ],
      "name":"Time elapsed in print"
   }
}
"""
, hostname="192.168.1.144",port=1883, auth= auth)
paho.mqtt.publish.single("homeassistant/sensor/sensorTimeLeft/config",
"""
{
   "device_class":"duration",
   "state_topic":"homeassistant/sensor/sensorTimeLeft/state",
   "unit_of_measurement":"s",
   "value_template":"{{ value_json.duration}}",
   "unique_id":"TimeLeft01",
   "device":{
      "identifiers":[
         "TimeLeft01"
      ],
      "name":"Time Left in print"
   }
}
"""
, hostname="192.168.1.144",port=1883, auth= auth)
paho.mqtt.publish.single("homeassistant/sensor/sensorPercentProgress/config",
"""
{
   "device_class":"battery",
   "state_topic":"homeassistant/sensor/sensorPercentProgress/state",
   "unit_of_measurement":"%",
   "value_template":"{{ value_json.percent}}",
   "unique_id":"PercentProgress01",
   "device":{
      "identifiers":[
         "PercentProgress01"
      ],
      "name":"Percent Progress in print"
   }
}
"""
, hostname="192.168.1.144",port=1883, auth= auth)
paho.mqtt.publish.single("homeassistant/sensor/sensorRealSpeed/config",
"""
{
   "device_class":"speed",
   "state_topic":"homeassistant/sensor/sensorRealSpeed/state",
   "unit_of_measurement":"mm/s",
   "value_template":"{{ value_json.speed}}",
   "unique_id":"RealSpeed01",
   "device":{
      "identifiers":[
         "RealSpeed01"
      ],
      "name":"Print speed"
   }
}
"""
, hostname="192.168.1.144",port=1883, auth= auth)
paho.mqtt.publish.single("homeassistant/sensor/sensorFilamentUsed/config",
"""
{
   "device_class":"weight",
   "state_topic":"homeassistant/sensor/sensorFilamentUsed/state",
   "unit_of_measurement":"g",
   "value_template":"{{ value_json.weight}}",
   "unique_id":"FilamentUsed01",
   "device":{
      "identifiers":[
         "FilamentUsed01"
      ],
      "name":"Filament used"
   }
}
"""
, hostname="192.168.1.144",port=1883, auth= auth)
#time_left = "1"
#time_elapsed = "2.1"
#filament_used = "5"
#real_speed = "12"
#percent_progress = "12"
#paho.mqtt.publish.single("homeassistant/sensor/sensorTimeLeft/state","""{"duration":"""+ time_left + "}", hostname="192.168.1.144",port=1883, auth= auth)#
#paho.mqtt.publish.single("homeassistant/sensor/sensorTimeElapsed/state","""{"duration":"""+ time_elapsed + "}", hostname="192.168.1.144",port=1883, auth= auth)#
#paho.mqtt.publish.single("homeassistant/sensor/sensorPercentProgress/state","""{"percent":""" + percent_progress + "}", hostname="192.168.1.144",port=1883, auth= auth)#
#paho.mqtt.publish.single("homeassistant/sensor/sensorRealSpeed/state", """{"speed":""" + real_speed + "}", hostname="192.168.1.144",port=1883, auth= auth)
#paho.mqtt.publish.single("homeassistant/sensor/sensorFilamentUsed/state","""{"weight":""" + filament_used + "}", hostname="192.168.1.144",port=1883, auth= auth)
#paho.mqtt.publish.single("homeassistant/sensor/sensorNozzle/state", """{"temperature":""" + str(21000 / 100) + "}", hostname="192.168.1.144",port=1883, auth= auth)
#paho.mqtt.publish.single("homeassistant/sensor/sensorHeatbed/state", """{"temperature":""" + str(21000 / 100) + "}", hostname="192.168.1.144",port=1883, auth= auth)