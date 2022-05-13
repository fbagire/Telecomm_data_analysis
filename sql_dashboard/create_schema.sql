CREATE TABLE IF NOT EXISTS `TelcomData`
(
    `id` INT NOT NULL AUTO_INCREMENT,
    `Bearer Id` TEXT DEFAULT NULL,
    `MSISDN/Number` TEXT DEFAULT NULL ,
    `Avg RTT DL (ms)` FLOAT DEFAULT NULL,
    `Avg RTT UL (ms)` FLOAT DEFAULT NULL,
    `10 Kbps < UL TP < 50 Kbps (%)` FLOAT DEFAULT NULL,
    `250 Kbps < DL TP < 1 Mbps (%)` FLOAT DEFAULT NULL,
    `50 Kbps < DL TP < 250 Kbps (%)` FLOAT DEFAULT NULL,
    `Activity Duration DL (ms)` FLOAT DEFAULT NULL,
    `Activity Duration UL (ms)` FLOAT DEFAULT NULL,
    `Avg Bearer TP DL (kbps)` FLOAT DEFAULT NULL,
    `Avg Bearer TP UL (kbps)` FLOAT DEFAULT NULL,
    `DL TP < 50 Kbps (%)` FLOAT DEFAULT NULL,
    `DL TP > 1 Mbps (%)` FLOAT DEFAULT NULL,
    `Dur. (s)` FLOAT DEFAULT NULL,
    `Email DL (Bytes)` FLOAT DEFAULT NULL,
    `Email Total (megabytes)` FLOAT DEFAULT NULL,
    `Email UL (Bytes)` FLOAT DEFAULT NULL,
    `Gaming DL (Bytes)` FLOAT DEFAULT NULL,
    `Gaming Total (megabytes)` FLOAT DEFAULT NULL,
    `Gaming UL (Bytes)` FLOAT DEFAULT NULL,
    `Google DL (Bytes)` FLOAT DEFAULT NULL,
    `Google Total (megabytes)` FLOAT DEFAULT NULL,
    `Google UL (Bytes)` FLOAT DEFAULT NULL,
    `Handset Manufacturer` TEXT DEFAULT NULL,
    `Handset Type` TEXT DEFAULT NULL,
    `Nb of sec with Vol DL < 6250B` FLOAT DEFAULT NULL,
    `Nb of sec with Vol UL < 1250B` FLOAT DEFAULT NULL,
    `Netflix DL (Bytes)` FLOAT DEFAULT NULL,
    `Netflix Total (megabytes)` FLOAT DEFAULT NULL,
    `Netflix UL (Bytes)` FLOAT DEFAULT NULL,
    `Other DL (Bytes)` FLOAT DEFAULT NULL,
    `Other Total (megabytes)` FLOAT DEFAULT NULL,
    `Other UL (Bytes)` FLOAT DEFAULT NULL,
    `Social Media DL (Bytes)` FLOAT DEFAULT NULL,
    `Social Media Total (megabytes)` FLOAT DEFAULT NULL,
    `Social Media UL (Bytes)` FLOAT DEFAULT NULL,
    `Total DL (Bytes)` FLOAT DEFAULT NULL,
    `Total Data (megabytes)` FLOAT DEFAULT NULL,
    `Total UL (Bytes)` FLOAT DEFAULT NULL,
    `UL TP < 10 Kbps (%)` FLOAT DEFAULT NULL,
    `Youtube DL (Bytes)` FLOAT DEFAULT NULL,
    `Youtube Total (megabytes)` FLOAT DEFAULT NULL,
    `Youtube UL (Bytes)` FLOAT DEFAULT NULL,
    PRIMARY KEY (`id`)
)

ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
