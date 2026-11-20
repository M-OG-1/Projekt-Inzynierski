#!/bin/sh

if [ ! -e "cert.pem" ] || [ ! -e "key.pem" ]
then
  openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
fi

.venv/bin/python3 -m projekt_inzynierski