-- create the database
CREATE DATABASE internet_speed_test;

-- switch to the new database
USE internet_speed_test;

-- create the results table
CREATE TABLE results (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    datetime DATETIME NOT NULL,
    download_speed FLOAT NOT NULL,
    upload_speed FLOAT NOT NULL,
    ping FLOAT NOT NULL,
    server_id INT NOT NULL,
    server_name VARCHAR(255) NOT NULL,
    hostname VARCHAR(255) NOT NULL
);

-- create the servers table
CREATE TABLE servers (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    server_id INT NOT NULL,
    server_name VARCHAR(255) NOT NULL,
    UNIQUE (server_id)
);
