-- create the database
CREATE DATABASE internet_monitor;

-- switch to the new database
USE internet_monitor;

-- internet_monitor.tb002_servers definition
CREATE TABLE tb002_servers 
    server_id INT NOT NULL,
    server_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (server_id),
);

-- internet_monitor.tb001_monitor_hosts definition
CREATE TABLE `tb001_monitor_hosts` (
  `id_monitor_host` tinyint(4) NOT NULL AUTO_INCREMENT,
  `nome_monitor_host` varchar(100) NOT NULL,
  PRIMARY KEY (`id_monitor_host`),
  UNIQUE KEY `monitor_hosts_nome_host_id_IDX` (`nome_monitor_host`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;



-- internet_monitor.tb003_speedtest_results definition
CREATE TABLE `tb003_speedtest_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  `download_speed` float NOT NULL,
  `upload_speed` float NOT NULL,
  `ping` float NOT NULL,
  `server_id` int(11) NOT NULL,
  `id_monitor_host` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tb003_FK_tb001` (`id_monitor_host`),
  KEY `tb003_FK_tb002` (`server_id`),
  CONSTRAINT `speedtest_results_FK` FOREIGN KEY (`id_monitor_host`) REFERENCES `tb001_monitor_hosts` (`id_monitor_host`),
  CONSTRAINT `tb003_speedtest_results_FK` FOREIGN KEY (`server_id`) REFERENCES `tb002_servers` (`server_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4646 DEFAULT CHARSET=utf8mb4;
