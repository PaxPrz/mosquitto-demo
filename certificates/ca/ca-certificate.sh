#!/bin/bash

openssl genrsa 2048 > ca.key
openssl req -new -x509 -nodes -days 365 \
   -key ca.key \
   -out ca.crt
