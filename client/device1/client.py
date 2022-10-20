
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
CLIENT_NAME = "LILY"
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(Path(__file__).parent / ".env")  # load client env
load_dotenv(ROOT_DIR / ".env")  # load main env
MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = os.environ.get("MQTT_PORT", 1883)
MQTT_KEEP_ALIVE = os.environ.get("MQTT_KEEP_ALIVE", 60)
CA_CERT = os.environ.get("CA_CERT")
CA_CERT = ROOT_DIR / CA_CERT if CA_CERT else None
CLIENT_CERT = os.environ.get("CLIENT_CERTFILE")
CLIENT_CERT = ROOT_DIR / CLIENT_CERT if CLIENT_CERT else None
CLIENT_KEY = os.environ.get("CLIENT_KEYFILE")
CLIENT_KEY = ROOT_DIR / CLIENT_KEY if CLIENT_KEY else None
DENY_SSL = str(sys.argv[-1]) == '0'


def on_connect(client: Client, userdata: Union[None, Any], flags: Dict[str, Any], rc: int) -> None:
    LOGGER.info(f"Conneected with result code: {str(rc)}")
    LOGGER.debug(f"Subscribing to {CLIENT_NAME=}")
    client.subscribe(CLIENT_NAME)


def on_message(client: Client, userdata: Union[None, Any], msg: MQTTMessage) -> None:
    LOGGER.info(f"{msg.topic}: {str(msg.payload)}")


if __name__ == "__main__":
    LOGGER.debug(f"Stating up client: {CLIENT_NAME}")
    client = Client(client_id=CLIENT_NAME, userdata={"client_id": 2})
    if not DENY_SSL and CA_CERT and CLIENT_CERT and CLIENT_KEY:
        LOGGER.debug("Setting up Certificates...")
        client.tls_set(ca_certs=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.on_connect = on_connect
    client.on_message = on_message
    LOGGER.info(f"Connecting to MQTT broker: {MQTT_HOST}:{MQTT_PORT}")
    client.connect(host=MQTT_HOST, port=MQTT_PORT, keepalive=MQTT_KEEP_ALIVE)
    msg = ""
    while True:
        msg = input("Enter message to send (exit): ")
        if msg == "exit":
            break
        client.publish(CHANNEL, msg)
    LOGGER.info(f"Shutting down client: {CLIENT_NAME}")

