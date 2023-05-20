#!/bin/bash

# install speedtest cli
#wget https://bintray.com/ookla/download/download_file?file_path=ookla-speedtest-1.0.0-x86_64-linux.tgz
#tar -xvzf download_file?file_path=ookla-speedtest-1.0.0-x86_64-linux.tgz
#mv speedtest /usr/local/bin/

## If migrating from prior bintray install instructions please first...
# sudo rm /etc/apt/sources.list.d/speedtest.list
# sudo apt-get update
# sudo apt-get remove speedtest
## Other non-official binaries will conflict with Speedtest CLI
# Example how to remove using apt-get
# sudo apt-get remove speedtest-cli
sudo apt-get install curl
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest

# install mysql connector
pip3 install mysql-connector-python

## create database and tables
#mysql -h mysql_localhost -u mysql_username -p mysql_password < database.sql
