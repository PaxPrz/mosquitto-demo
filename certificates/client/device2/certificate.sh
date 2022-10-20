#!/bin/bash

openssl req -newkey rsa:2048 -nodes -days 365 \
   -keyout client.key \
   -out client.csr

openssl x509 -req -days 365 -set_serial 01 \
   -in client.csr\
   -out client.crt\
   -CA ../../ca/ca.crt\
   -CAkey ../../ca/ca.key
