import paho.mqtt.client as mqtt
import paho.mqtt
import ssl
import json

from datetime import datetime, timedelta

from libflagship.mqtt import MqttMsg


class AnkerMQTTBaseClient:

    def __init__(self, printersn, mqtt, key, guid=None):
        self._mqtt = mqtt
        self._printersn = printersn
        self._key = key
        self._mqtt.on_connect    = self._on_connect
        self._mqtt.on_disconnect = self._on_disconnect
        self._mqtt.on_message    = self._on_message
        self._mqtt.on_publish    = self.on_publish
        self._queue = []

        self._connected = False

    # internal function
    def _on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            raise IOError(f"could not connect: rc={rc} ({paho.mqtt.client.error_string(rc)})")
        mqtt = self._mqtt
        mqtt.subscribe(f"/phone/maker/{self.sn}/notice")
        mqtt.subscribe(f"/phone/maker/{self.sn}/command/reply")
        mqtt.subscribe(f"/phone/maker/{self.sn}/query/reply")
        self._connected = True
        self.on_connect(client, userdata, flags)

    # internal function
    def _on_disconnect(self, client, userdata, rc):
        self._connected = False

    # public api: override in subclass (if needed)
    def on_connect(self, client, userdata, flags):
        print("connected")

    # public api: override in subclass (if needed)
    def on_publish(self, client, userdata, result):
        pass

    # internal function
    def _on_message(self, client, userdata, msg):
        try:
            pkt, tail = MqttMsg.parse(msg.payload, key=self._key)
        except Exception as E:
            hexStr =' '.join([f'0x{byte:02x}' for byte in msg.payload])
            print(f"Failed to decode mqtt message\n Exception: {E}\n Message : {hexStr}")
            return

        data = json.loads(pkt.data)
        if isinstance(data, list):
            self._queue.append((msg, data))
        else:
            self._queue.append((msg, [data]))

        if tail:
            print(f"UNPARSED TAIL DATA: {tail}")

        self.on_message(client, userdata, msg, pkt, tail)

    # public api: override in subclass (if needed)
    def on_message(self, client, userdata, msg, pkt, tail):
        pass

    @classmethod
    def login(cls, printersn, username, password, key, ca_certs=None, verify=True):
        client = mqtt.Client()
        cert_reqs = ssl.CERT_NONE if not verify else ssl.VERIFY_DEFAULT
        client.tls_set(ca_certs=ca_certs, cert_reqs=cert_reqs)
        client.tls_insecure_set(not verify)
        client.username_pw_set(username, password)

        return cls(printersn, client, key)

    def connect(self, server, port=8789, timeout=60):
        self._mqtt.connect(server, port, timeout)

        start = datetime.now()
        end = start + timedelta(seconds=timeout)

        while datetime.now() < end:
            timeout = (end - datetime.now()).total_seconds()
            self._mqtt.loop(timeout=timeout)
            if self._connected:
                return

        raise IOError("Timeout while connecting to mqtt server")

    @property
    def sn(self):
        return self._printersn

    def loop(self):
        self._mqtt.loop_forever()

    def fetch(self, timeout=1.0):
        self._mqtt.loop(timeout=timeout)
        return self.clear_queue()

    def fetchloop(self):
        while True:
            self._mqtt.loop(timeout=1.0)
            yield from self.clear_queue()

    def clear_queue(self):
        res = self._queue[:]
        self._queue.clear()
        return res

