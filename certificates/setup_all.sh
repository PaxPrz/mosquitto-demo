#/bin/bash

cd ca/
./ca-certificate.sh
cd ../server
./certificate.sh
cd ../mosquitto
./certificate.sh
cd ../client/device1
./certificate.sh
cd ../device2
./certificate.sh
cd ../..