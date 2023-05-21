import subprocess
import json
import mysql.connector
import csv
import argparse
from datetime import datetime
import socket
from common_lib.cache_util import CacheUtil
from common_lib.storage_type import StorageType

class InternetSpeedTest(CacheUtil):
    def __init__(self,
                storage_type: StorageType,
                host: str, 
                username: str, 
                password: str, 
                database_name: str,
                output_file: str = None) -> None:
        self.storage_type = storage_type
        self.host = host
        self.username = username
        self.password = password
        self.database_name = database_name
        self.output_file = output_file
        
        super().__init__()

    def get_speedtest_data(self):
        result = subprocess.run(["/usr/bin/speedtest", "--accept-license", "--accept-gdpr", "-f", "json"], stdout=subprocess.PIPE)
        return json.loads(result.stdout)

    def persist_to_csv(self, data, file_name):
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(["datetime", "download_speed", "upload_speed", "ping", "server_id", "server_name", "hostname"])

            writer.writerow([data['timestamp'], data['download']['bandwidth'], data['upload']['bandwidth'], data['ping']['latency'], data['server']['id'], data['server']['name'], data['hostname']])

    def get_mysql_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database_name
        )

    def __insert_monitor_host(self, hostname: str) -> int:
        id_monitor_host: int
        try:
            connection = self.get_mysql_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO tb001_monitor_hosts (nome_monitor_host) VALUES (%s)"
            cursor.execute(sql, (hostname,))
            connection.commit()
            id_monitor_host = cursor.lastrowid
        
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
        
        return id_monitor_host

    def __get_monitor_host_id(self, **kwargs) -> int:
        id_monitor_host: int = None
        try:
            hostname = kwargs.get('hostname')
            connection = self.get_mysql_connection()
            cursor = connection.cursor()
            sql = "SELECT id_monitor_host from tb001_monitor_hosts WHERE nome_monitor_host = %s"
            cursor.execute(sql, (hostname,))
            record = cursor.fetchone()
            if record:
                id_monitor_host = record[0]
            connection.close()
            
            if id_monitor_host is None:
                id_monitor_host = self.__insert_monitor_host(hostname)
            
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
                
        ttl = 43200  #12 hours
        return (id_monitor_host, ttl)

    def get_monitor_host_id(self) -> int: 
        fqdn = socket.getfqdn()
        return self._get_cached_value(key=fqdn, 
                                        func_get_value=self.__get_monitor_host_id, 
                                        hostname=fqdn)

    def persist_to_mysql(self, data):
        
        id_monitor_host = self.get_monitor_host_id()
        
        try:
            connection = self.get_mysql_connection()
            cursor = connection.cursor()

            # Insert server information into 'speedtest_servers' table
            # insert data into server table
            sql_query = "INSERT INTO tb002_servers (server_id, server_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE server_name = %s"
            cursor.execute(sql_query, (data['server']['id'], data['server']['name'], data['server']['name']))
            
            # Insert data into 'speedtest_results' table
            sql = "INSERT INTO tb003_speedtest_results (datetime, download_speed, upload_speed, ping, server_id, id_monitor_host) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (data['timestamp'], data['download']['bandwidth'], data['upload']['bandwidth'], data['ping']['latency'], data['server']['id'],  id_monitor_host)
            cursor.execute(sql, values)
            connection.commit()
        except mysql.connector.Error as e:
            print("Error inserting data on MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
           

    def start(self):
        # parse json output
        json_output = self.get_speedtest_data()
        json_output['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_output['hostname'] = socket.gethostname()

        print(json_output)

        # persist data to database or csv file
        if self.storage_type == StorageType.DATABASE:
            self.persist_to_mysql(data=json_output)
        elif self.storage_type == StorageType.CSV:
            self.persist_to_csv(data=json_output, file_name=self.output_file)
        
        print("internet_speed_test data persisted.")



# parse command line arguments
parser = argparse.ArgumentParser(description="Check internet speed")
parser.add_argument("-d", "--database", help="Persist results to a MySQL database", action="store_true")
parser.add_argument("--host", help="MySQL hostname")
parser.add_argument("--user", help="MySQL username")
parser.add_argument("--password", help="MySQL password")
parser.add_argument("--database_name", help="MySQL database_name")
parser.add_argument("-c", "--csv", help="Persist results to a CSV file", action="store_true")
parser.add_argument("--output-file", help="CSV file_name")
                  
args = parser.parse_args()
storage_type: StorageType
internet_speedtest: InternetSpeedTest
if args.database:
    storage_type = StorageType.DATABASE
elif args.csv:
    storage_type = StorageType.CSV 

internet_speedtest =  InternetSpeedTest(storage_type=storage_type,
                                            host=args.host, 
                                            username=args.user, 
                                            password=args.password, 
                                            database_name=args.database_name,
                                            output_file=args.output_file)

internet_speedtest.start()
