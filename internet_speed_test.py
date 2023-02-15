import subprocess
import json
import mysql.connector
import csv
import argparse
from datetime import datetime
import socket


def get_speedtest_data():
    result = subprocess.run(["/usr/bin/speedtest", "--accept-license", "--accept-gdpr", "-f", "json"], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def persist_to_csv(data, file_name):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(["datetime", "download_speed", "upload_speed", "ping", "server_id", "server_name", "hostname"])

        writer.writerow([data['timestamp'], data['download']['bandwidth'], data['upload']['bandwidth'], data['ping']['latency'], data['server']['id'], data['server']['name'], data['hostname']])


def persist_to_mysql(data, host, username, password, database_name):
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database_name
    )
    cursor = conn.cursor()

    # Insert data into 'speedtest_results' table
    sql = "INSERT INTO speedtest_results (datetime, download_speed, upload_speed, ping, server_id, server_name, hostname) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (data['timestamp'], data['download']['bandwidth'], data['upload']['bandwidth'], data['ping']['latency'], data['server']['id'], data['server']['name'], data['hostname'])
    cursor.execute(sql, values)

    # Insert server information into 'speedtest_servers' table
    # insert data into server table
    sql_query = "INSERT INTO servers (server_id, server_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_name = %s"
    cursor.execute(sql_query, (data['server']['id'], data['server']['name'], data['server']['name']))

    conn.commit()
    cursor.close()
    conn.close()


# parse command line arguments
parser = argparse.ArgumentParser(description="Check internet speed")
parser.add_argument("-d", "--database", help="Persist results to a MySQL database", action="store_true")

parser = argparse.ArgumentParser(description="Check internet speed")
parser.add_argument("-d", "--database", help="Persist results to a MySQL database", action="store_true")
parser.add_argument("--host", help="MySQL hostname")
parser.add_argument("--user", help="MySQL username")
parser.add_argument("--password", help="MySQL password")
parser.add_argument("--database_name", help="MySQL database_name")
      

parser.add_argument("-c", "--csv", help="Persist results to a CSV file", action="store_true")
parser.add_argument("--output-file", help="CSV file_name")
                  
args = parser.parse_args()

# parse json output
json_output = get_speedtest_data()
json_output['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json_output['hostname'] = socket.gethostname()

# persist data to database or csv file
if args.database:
    persist_to_mysql(data=json_output, 
                        host=args.host, 
                        username=args.user, 
                        password=args.password, 
                        database_name=args.database_name)
elif args.csv:
    persist_to_csv(data=json_output, file_name=args.output_file)
    