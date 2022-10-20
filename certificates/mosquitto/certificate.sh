#!/bin/bash

openssl req -newkey rsa:2048 -nodes -days 365 \
   -keyout mosquitto.key \
   -out mosquitto.csr

openssl x509 -req -days 365 -set_serial 01 \
   -in mosquitto.csr\
   -out mosquitto.crt\
   -CA ../ca/ca.crt\
   -CAkey ../ca/ca.key
