#!/usr/bin/env python3
import paho.mqtt.publish
import json
import click

from cli.config import configmgr
from cli.mqtt import mqtt_open

from libflagship.mqtt import MqttMsgType
auth = {'username':"PUT YOUR USERNAME HERE",'password':"PUT YOUR PASSOWRD HERE"}

class Environment:

    def load_config(self, required=True):
        with self.config.open() as config:
            if not getattr(config, 'printers', False):
                msg = "No printers found in config. Please upload configuration " \
                    "using the webserver or 'ankerctl.py config import'"


pass_env = click.make_pass_decorator(Environment)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.pass_context
def main(ctx):
    ctx.ensure_object(Environment)
    env = ctx.obj
    env.config   = configmgr()


@main.group("mqtt", help="Low-level mqtt api access")
@pass_env
def mqtt(env):
    env.load_config()

def printstuff(id, jso, name):
    print("id: " + str(id))
    print("json:" + jso)
    print("name: " + name)
@mqtt.command("monitor")
@pass_env
def mqtt_monitor(env):
    """
    Connect to mqtt broker, and show low-level events in realtime.
    """

    client = mqtt_open(env.config, 0, False)

    for msg, body in client.fetchloop():
        for obj in body:
            try:
                id = int(MqttMsgType(obj["commandType"]))
                jso = obj
                name =str(MqttMsgType(obj["commandType"]).name)
            except:
                print("darn" + str(obj["commandType"]))
            if name.startswith("ZZ_MQTT_CMD_"):
                name = name[len("ZZ_MQTT_CMD_"):].lower()#
            match obj["commandType"]:
                case 1003:
                    paho.mqtt.publish.single("homeassistant/sensor/sensorNozzle/state", """{"temperature":""" + str(round(int(obj['currentTemp']) / 100)) + "}", hostname="192.168.1.144",port=1883, auth= auth)
                case 1004:
                    paho.mqtt.publish.single("homeassistant/sensor/sensorHeatbed/state", """{"temperature":""" + str(round(int(obj['currentTemp']) / 100)) + "}", hostname="192.168.1.144",port=1883, auth= auth)
                case 1001:
                    #print schedule
                    time_left = str(round(int(obj['time'])))
                    time_elapsed = str(round(int(obj['totalTime'])))
                    percent_progress = str(round(int(obj['progress']) / 100))
                    real_speed = str(obj['realSpeed'])
                    filament_used = str(obj['filamentUsed'])
                    model_name = str(obj['name'])
                    if model_name.endswith(".gcode"):
                        model_name = model_name[:len(model_name) - len(".gcode")]


                    print("time left: "+str(round(int(time_left) / 60 )) + " minutes")#total time it will take
                    print("so far "+str(round(int(time_elapsed) / 60 )) + " minutes")#time used so far
                    print(percent_progress + "%"+" done")#% progress
                    print("real speed: " + real_speed + " mm/s")#real speed
                    print("model name: " + model_name)
                    print("filament total: " + filament_used + " g")
                    print("\n")
                    paho.mqtt.publish.single("homeassistant/sensor/sensorTimeLeft/state","""{"duration":"""+ time_left + "}", hostname="192.168.1.144",port=1883, auth= auth)
                    paho.mqtt.publish.single("homeassistant/sensor/sensorTimeElapsed/state","""{"duration":"""+ time_elapsed + "}", hostname="192.168.1.144",port=1883, auth= auth)
                    paho.mqtt.publish.single("homeassistant/sensor/sensorPercentProgress/state","""{"percent":""" + percent_progress + "}", hostname="192.168.1.144",port=1883, auth= auth)
                    paho.mqtt.publish.single("homeassistant/sensor/sensorRealSpeed/state", """{"speed":""" + real_speed + "}", hostname="192.168.1.144",port=1883, auth= auth)
                    paho.mqtt.publish.single("homeassistant/sensor/sensorFilamentUsed/state","""{"weight":""" + filament_used + "}", hostname="192.168.1.144",port=1883, auth= auth)
                #case _:
                    












if __name__ == "__main__":
    main()
