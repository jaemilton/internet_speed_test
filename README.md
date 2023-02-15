#to run the speed test and save de result on .csv file
python internet_speed_test.py --csv --output-file my_speed_test_results.csv

#to run the speed test and save de result on mysql database
python internet_speed_test.py --database "--host", "mysql_hostname", "--user", "username", "--password", "your_password", "--database_name", "internet_speed_test"

#to schedule executions using cron add the following line do crontab -e
0 5 * * 1 tar -zcf /var/backups/home.tgz /home/


