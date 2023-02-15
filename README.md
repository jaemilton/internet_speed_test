#to run the speed test and save de result on .csv file
python internet_speed_test.py --csv --output-file my_speed_test_results.csv

#to run the speed test and save de result on mysql database
python internet_speed_test.py --database "--host", "mysql_hostname", "--user", "username", "--password", "your_password", "--database_name", "internet_speed_test"

#to schedule executions using cron add the following line do crontab -e
*/20 * * * * /root/git/internet_speed_test/internet_speed_test.py --database --host mysql.rede.jai --user internet_monitor --password EoiV@BvA9u3Nrc --database_name internet_monitor 


