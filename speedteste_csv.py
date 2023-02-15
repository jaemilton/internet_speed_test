import os
import json
import csv
import datetime
import socket
import mysql.connector
from subprocess import check_output

def check_speed():
    speedtest_output = check_output("speedtest --json", shell=True)
    speedtest_output = json.loads(speedtest_output)
    download = speedtest_output["download"]
    upload = speedtest_output["upload"]
    ping = speedtest_output["ping"]
    server_id = speedtest_output["server"]["id"]
    server_name = speedtest_output["server"]["name"]
    return download, upload, ping, server_id, server_name

def persist_to_db(download, upload, ping, server_id, server_name, date_time, hostname):
    conn = mysql.connector.connect(
        host="hostname",
        user="username",
        password="password",
        database="internet_speed_test"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO server_info (server_id, server_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_name = server_name", (server_id, server_name))
    cursor.execute("INSERT INTO internet_speed (datetime, download, upload, ping, server_id, hostname) VALUES (%s, %s, %s, %s, %s, %s)", (date_time, download, upload, ping, server_id, hostname))
    conn.commit()
    cursor.close()
    conn.close()

def persist_to_csv(download, upload, ping, server_name, date_time, hostname):
    filename = "internet_speed_test.csv"
    header = ["datetime", "download", "upload", "ping", "server_name", "hostname"]
    data = [date_time, download, upload, ping, server_name, hostname]

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(data)
    else:
        with open(filename, "a") as f:
            writer = csv.writer(f)
            writer.writerow(data)

if __name__ == "__main__":
    date_time = datetime.datetime.now()
    hostname = socket.gethostname()
    download, upload, ping, server_id, server_name = check_speed()
    persist_to_db(download, upload, ping, server_id, server_name, date_time, hostname)
    persist_to_csv(download, upload, ping, server_id, server_name, date_time, hostname)
