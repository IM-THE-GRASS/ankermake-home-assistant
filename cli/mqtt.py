
from libflagship import ROOT_DIR
from libflagship.mqttapi import AnkerMQTTBaseClient

servertable = {
    "eu": "make-mqtt-eu.ankermake.com",
    "us": "make-mqtt.ankermake.com",
}


def mqtt_open(config, printer_index, insecure):

    with config.open() as cfg:
        if printer_index >= len(cfg.printers):
            print("idk what to say")
        printer = cfg.printers[printer_index]
        acct = cfg.account
        server = servertable[acct.region]
        client = AnkerMQTTBaseClient.login(
            printer.sn,
            acct.mqtt_username,
            acct.mqtt_password,
            printer.mqtt_key,
            ca_certs=ROOT_DIR / "ssl/ankermake-mqtt.crt",
            verify=not insecure,
        )
        client.connect(server)
        return client


