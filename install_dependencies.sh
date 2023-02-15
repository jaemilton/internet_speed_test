#!/bin/bash

# install speedtest cli
wget https://bintray.com/ookla/download/download_file?file_path=ookla-speedtest-1.0.0-x86_64-linux.tgz
tar -xvzf download_file?file_path=ookla-speedtest-1.0.0-x86_64-linux.tgz
mv speedtest /usr/local/bin/

# install mysql connector
pip3 install mysql-connector-python

# create database and tables
mysql -u root -p -e "CREATE DATABASE internet_speed_test"
mysql -u root -p internet_speed_test < internet_speed_test.sql
