from typing import Union, Dict, Any
import os
import logging
from paho.mqtt.client import Client, MQTTMessage
from dotenv import load_dotenv
from pathlib import Path
import ssl
import sys


LOGGER = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
LOGGER.addHandler(stream_handler)
LOGGER.setLevel(logging.DEBUG)
stream_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(message)s"
    )
)

CHANNEL = "channel"
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(Path(__file__).parent / ".env")  # load server env
load_dotenv(ROOT_DIR / ".env")  # load main env
MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = os.environ.get("MQTT_PORT", 1883)
MQTT_KEEP_ALIVE = os.environ.get("MQTT_KEEP_ALIVE", 60)
CA_CERT = os.environ.get("CA_CERT")
CA_CERT = ROOT_DIR / CA_CERT if CA_CERT else None
SERVER_CERT = os.environ.get("SERVER_CERTFILE")
SERVER_CERT = ROOT_DIR / SERVER_CERT if SERVER_CERT else None
SERVER_KEY = os.environ.get("SERVER_KEYFILE")
SERVER_KEY = ROOT_DIR / SERVER_KEY if SERVER_KEY else None
DENY_SSL = str(sys.argv[-1]) == '0'


def on_connect(client: Client, userdata: Union[None, Any], flags: Dict[str, Any], rc: int) -> None:
    LOGGER.info(f"Connected with result code: {str(rc)}")
    LOGGER.debug(f"Subscribing to {CHANNEL=}")
    client.subscribe(CHANNEL)


def on_message(client: Client, userdata: Union[None, Any], msg: MQTTMessage) -> None:
    LOGGER.info(f"{msg.topic}: {str(msg.payload)}")
    if b"repeat" in msg.payload:
        client.publish(CHANNEL, "So you want to hear it again?", qos=0)


if __name__ == "__main__":
    LOGGER.debug("Starting up system")
    client = Client(client_id="SERVER", userdata={"server": "me"})
    if not DENY_SSL and CA_CERT and SERVER_CERT and SERVER_KEY:
        LOGGER.debug("Setting up Certificates...")
        client.tls_set(ca_certs=CA_CERT, certfile=SERVER_CERT, keyfile=SERVER_KEY, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.on_connect = on_connect
    client.on_message = on_message
    LOGGER.info(f"Connecting to MQTT broker: {MQTT_HOST}:{MQTT_PORT}")
    client.connect(host=MQTT_HOST, port=MQTT_PORT, keepalive=MQTT_KEEP_ALIVE)
    LOGGER.debug("Looping forever...")
    client.loop_forever()
