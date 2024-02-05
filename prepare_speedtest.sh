#!/bin/bash

EUID="id -u"
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt-get update
echo "#### Installing  python3, python3-pip"
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install python3-venv -y

echo ""

python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/pip3 install setuptools wheel retrying pythonping python-decouple mysql-connector-python 

chmod +x ./run_pingmonitor.sh
chmod +x ./run_csv_db_importer.sh


