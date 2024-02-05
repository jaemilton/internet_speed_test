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




#install runnitor 
wget https://github.com/bdd/runitor/releases/download/v1.2.0/runitor-v1.2.0-linux-arm64
mv runitor-v1.2.0-linux-arm64 /opt
chmod +x /opt/runitor-v1.2.0-linux-arm64

## create database and tables
#mysql -h mysql_localhost -u mysql_username -p mysql_password < database.sql


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
#echo "Script directory: $SCRIPT_DIR"

cd $SCRIPT_DIR
source .venv/bin/activate

.venv/bin/pip install -r requirements.txt
