-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: localhost    Database: metricsDB
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `benchmark`
--

DROP TABLE IF EXISTS `benchmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `benchmark` (
  `id` int NOT NULL AUTO_INCREMENT,
  `inst_id` int NOT NULL,
  `t_entry` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `cpu_score` int DEFAULT NULL,
  `latency` int DEFAULT NULL,
  `tail_latency` int DEFAULT NULL,
  `avail` decimal(3,2) DEFAULT '1.00',
  PRIMARY KEY (`id`),
  KEY `inst_id` (`inst_id`),
  CONSTRAINT `benchmark_ibfk_1` FOREIGN KEY (`inst_id`) REFERENCES `instances` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `benchmark`
--

LOCK TABLES `benchmark` WRITE;
/*!40000 ALTER TABLE `benchmark` DISABLE KEYS */;
INSERT INTO `benchmark` VALUES (2,1,'2020-05-04 17:30:50',92,100,145,1.00),(3,1,'2020-05-04 17:43:16',92,100,145,1.00),(4,1,'2020-05-04 17:51:23',92,100,145,1.00),(5,1,'2020-05-04 17:52:54',92,100,145,1.00),(6,1,'2020-05-04 17:53:44',92,100,145,1.00),(7,1,'2020-05-04 17:54:16',92,100,145,1.00),(8,1,'2020-05-04 18:06:43',92,100,145,1.00),(9,1,'2020-05-04 18:07:52',92,100,145,1.00),(10,1,'2020-05-04 18:08:12',92,100,145,1.00),(11,1,'2020-05-04 18:28:09',92,100,145,1.00),(12,1,'2020-05-04 18:28:59',92,100,145,1.00),(13,1,'2020-05-04 18:29:21',92,100,145,1.00),(14,1,'2020-05-04 18:35:22',92,100,145,1.00),(15,1,'2020-05-04 18:36:16',92,100,145,1.00),(17,2,'2020-05-04 19:13:11',92,100,145,1.00),(26,1,'2020-05-04 19:28:34',92,100,145,1.00),(27,1,'2020-05-04 19:29:49',92,100,145,1.00),(28,1,'2020-05-04 19:30:16',92,100,145,1.00),(29,1,'2020-05-04 19:36:45',92,100,145,1.00),(30,1,'2020-05-04 19:38:37',92,100,145,1.00),(31,1,'2020-05-04 19:38:58',92,100,145,1.00),(32,1,'2020-05-04 19:39:18',92,100,145,1.00),(33,1,'2020-05-04 19:41:08',92,100,145,1.00),(34,1,'2020-05-04 19:43:17',92,100,145,1.00),(35,1,'2020-05-04 19:44:08',92,100,145,1.00),(36,1,'2020-05-04 19:46:13',92,100,145,1.00),(37,1,'2020-05-04 19:49:04',92,100,145,1.00),(38,1,'2020-05-04 19:50:05',92,100,145,1.00),(39,1,'2020-05-04 19:50:59',92,100,145,1.00),(40,1,'2020-05-04 19:52:07',92,100,145,1.00),(41,1,'2020-05-04 19:53:02',92,100,145,1.00),(42,1,'2020-05-04 19:56:10',92,100,145,1.00),(43,1,'2020-05-04 20:01:01',92,100,145,1.00),(44,1,'2020-05-04 20:01:55',92,100,145,1.00),(45,1,'2020-05-04 20:03:43',92,100,145,1.00),(46,1,'2020-05-04 20:03:54',92,100,145,1.00),(47,1,'2020-05-04 20:04:48',92,100,145,1.00),(48,1,'2020-05-04 20:05:31',92,100,145,1.00),(49,1,'2020-05-04 22:23:50',92,100,145,1.00);
/*!40000 ALTER TABLE `benchmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instance_sizes`
--

DROP TABLE IF EXISTS `instance_sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instance_sizes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(11) GENERATED ALWAYS AS (concat(left(`provider`,3),left(`type`,3),left(`size`,3),right(`size`,2))) STORED,
  `name` varchar(22) DEFAULT NULL,
  `provider` varchar(8) DEFAULT NULL,
  `type` varchar(6) DEFAULT NULL,
  `size` varchar(12) DEFAULT NULL,
  `cpu` int DEFAULT '0',
  `gpu` int DEFAULT '0',
  `memory` int DEFAULT '0',
  `bandwidth` int DEFAULT '0',
  `price` float DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1138 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instance_sizes`
--

LOCK TABLES `instance_sizes` WRITE;
/*!40000 ALTER TABLE `instance_sizes` DISABLE KEYS */;
INSERT INTO `instance_sizes` (`id`, `name`, `provider`, `type`, `size`, `cpu`, `gpu`, `memory`, `bandwidth`, `price`) VALUES (1008,'c4.8xlarge',NULL,'61440','8xlarge',0,0,10,2,0),(1012,'c5.18xlarge',NULL,'147456','18xlarge',0,0,25,3,0),(1014,'c5.2xlarge',NULL,'16384','2xlarge',0,0,10,0,0),(1015,'c5.4xlarge',NULL,'32768','4xlarge',0,0,10,1,0),(1016,'c5.9xlarge',NULL,'73728','9xlarge',0,0,10,2,0),(1017,'c5.large',NULL,'4096','large',0,0,10,0,0),(1018,'c5.xlarge',NULL,'8192','xlarge',0,0,10,0,0),(1020,'c5d.18xlarge',NULL,'147456','18xlarge',1800,0,25,3,0),(1022,'c5d.2xlarge',NULL,'16384','2xlarge',200,0,10,0,0),(1023,'c5d.4xlarge',NULL,'32768','4xlarge',400,0,10,1,0),(1024,'c5d.9xlarge',NULL,'73728','9xlarge',900,0,10,2,0),(1025,'c5d.large',NULL,'4096','large',50,0,10,0,0),(1026,'c5d.xlarge',NULL,'8192','xlarge',100,0,10,0,0),(1035,'d2.8xlarge',NULL,'249856','8xlarge',48000,0,10,6,0),(1037,'g3.16xlarge',NULL,'499712','16xlarge',0,4,20,5,0),(1038,'g3.4xlarge',NULL,'124928','4xlarge',0,1,10,1,0),(1039,'g3.8xlarge',NULL,'249856','8xlarge',0,2,10,2,0),(1047,'h1.16xlarge',NULL,'262144','16xlarge',16000,0,25,4,0),(1048,'h1.2xlarge',NULL,'32768','2xlarge',2000,0,10,0,0),(1049,'h1.4xlarge',NULL,'65536','4xlarge',4000,0,10,1,0),(1050,'h1.8xlarge',NULL,'131072','8xlarge',8000,0,10,2,0),(1053,'i2.8xlarge',NULL,'249856','8xlarge',6400,0,10,7,0),(1055,'i3.16xlarge',NULL,'499712','16xlarge',15200,0,20,5,0),(1056,'i3.2xlarge',NULL,'62464','2xlarge',1900,0,10,1,0),(1057,'i3.4xlarge',NULL,'124928','4xlarge',3800,0,10,1,0),(1058,'i3.8xlarge',NULL,'249856','8xlarge',7600,0,10,2,0),(1059,'i3.large',NULL,'15616','large',475,0,10,0,0),(1060,'i3.xlarge',NULL,'31232','xlarge',950,0,10,0,0),(1068,'m4.10xlarge',NULL,'163840','10xlarge',0,0,10,2,0),(1069,'m4.16xlarge',NULL,'262144','16xlarge',0,0,20,3,0),(1074,'m5.12xlarge',NULL,'196608','12xlarge',0,0,10,2,0),(1076,'m5.24xlarge',NULL,'393216','24xlarge',0,0,25,5,0),(1077,'m5.2xlarge',NULL,'32768','2xlarge',0,0,10,0,0),(1078,'m5.4xlarge',NULL,'65536','4xlarge',0,0,10,1,0),(1080,'m5.large',NULL,'8192','large',0,0,10,0,0),(1082,'m5.xlarge',NULL,'16384','xlarge',0,0,10,0,0),(1097,'m5d.12xlarge',NULL,'196608','12xlarge',1800,0,10,3,0),(1099,'m5d.24xlarge',NULL,'393216','24xlarge',3600,0,25,5,0),(1100,'m5d.2xlarge',NULL,'32768','2xlarge',300,0,10,0,0),(1101,'m5d.4xlarge',NULL,'65536','4xlarge',600,0,10,1,0),(1103,'m5d.large',NULL,'8192','large',75,0,10,0,0),(1104,'m5d.xlarge',NULL,'16384','xlarge',150,0,10,0,0),(1121,'p2.16xlarge',NULL,'749568','16xlarge',0,16,20,14,0),(1122,'p2.8xlarge',NULL,'499712','8xlarge',0,8,10,7,0),(1124,'p3.16xlarge',NULL,'499712','16xlarge',0,8,25,24,0),(1125,'p3.2xlarge',NULL,'62464','2xlarge',0,1,10,3,0),(1126,'p3.8xlarge',NULL,'249856','8xlarge',0,4,10,12,0),(1129,'r3.8xlarge',NULL,'249856','8xlarge',640,0,10,3,0),(1132,'r4.16xlarge',NULL,'499712','16xlarge',0,0,20,4,0),(1133,'r4.2xlarge',NULL,'62464','2xlarge',0,0,10,1,0),(1134,'r4.4xlarge',NULL,'124928','4xlarge',0,0,10,1,0),(1135,'r4.8xlarge',NULL,'249856','8xlarge',0,0,10,2,0),(1136,'r4.large',NULL,'15616','large',0,0,10,0,0),(1137,'r4.xlarge',NULL,'31232','xlarge',0,0,10,0,0);
/*!40000 ALTER TABLE `instance_sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instances`
--

DROP TABLE IF EXISTS `instances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instances` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(10) GENERATED ALWAYS AS (lower(concat(left(`provider`,3),left(`type`,3),left(`tier`,4)))) STORED,
  `provider` varchar(8) DEFAULT NULL,
  `type` varchar(6) DEFAULT NULL,
  `tier` varchar(8) DEFAULT NULL,
  `cpu` int DEFAULT NULL,
  `gpu` int DEFAULT NULL,
  `memory` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instances`
--

LOCK TABLES `instances` WRITE;
/*!40000 ALTER TABLE `instances` DISABLE KEYS */;
INSERT INTO `instances` (`id`, `provider`, `type`, `tier`, `cpu`, `gpu`, `memory`) VALUES (1,'AWS','t1','micro',4,1,16),(2,'GCE','small','1',1,1,16),(3,'AWS','s1','micro',4,1,16);
/*!40000 ALTER TABLE `instances` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-10  4:06:38
