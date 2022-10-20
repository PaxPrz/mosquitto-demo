#!/bin/bash

openssl req -newkey rsa:2048 -nodes -days 365 \
   -keyout server.key \
   -out server.csr

openssl x509 -req -days 365 -set_serial 01 \
   -in server.csr\
   -out server.crt\
   -CA ../ca/ca.crt\
   -CAkey ../ca/ca.key
