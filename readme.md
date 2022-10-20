# Mosquitto demo

In order to run this project, you need to install mosquitto broker

`sudo apt install mosquitto`


Then to setup certificates using the script or doing it manually using
OpenSSL

```
cd certificates
find . -name "*.sh" -exec chmod +x {} \; 
./setup_all.sh
```

Setting up virtualenv

```
virtualenv -p python3.* .venv/
source .venv/bin/activate
```

Finally you're ready to connect as a server

```
python server/server.py
```

Connecting as client

```
python client/device1/client.py
```
