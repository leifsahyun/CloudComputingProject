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
-- Table structure for table `aws_instances_nonull`
--

DROP TABLE IF EXISTS `aws_instances_nonull`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aws_instances_nonull` (
  `id` int DEFAULT NULL,
  `name` text,
  `type` text,
  `size` text,
  `ram` int DEFAULT NULL,
  `cpu` int DEFAULT NULL,
  `disk` int DEFAULT NULL,
  `gpu` int DEFAULT NULL,
  `bandwidth` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  `provider` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aws_instances_nonull`
--

LOCK TABLES `aws_instances_nonull` WRITE;
/*!40000 ALTER TABLE `aws_instances_nonull` DISABLE KEYS */;
INSERT INTO `aws_instances_nonull` VALUES (1,'a1.2xlarge','a1','2xlarge',16384,8,0,0,10,0,'AWS'),(2,'a1.4xlarge','a1','4xlarge',32768,16,0,0,10,0,'AWS'),(3,'a1.large','a1','large',4096,2,0,0,10,0,'AWS'),(4,'a1.medium','a1','medium',2048,1,0,0,10,0,'AWS'),(5,'a1.xlarge','a1','xlarge',8192,4,0,0,10,0,'AWS'),(6,'c4.2xlarge','c4','2xlarge',15360,8,0,0,0,0,'AWS'),(7,'c4.4xlarge','c4','4xlarge',30720,16,0,0,0,1,'AWS'),(8,'c4.8xlarge','c4','8xlarge',61440,36,0,0,10,2,'AWS'),(9,'c4.large','c4','large',3840,2,0,0,0,0,'AWS'),(10,'c4.xlarge','c4','xlarge',7680,4,0,0,0,0,'AWS'),(11,'c5.12xlarge','c5','12xlarge',98304,48,0,0,12,0,'AWS'),(12,'c5.18xlarge','c5','18xlarge',147456,72,0,0,25,3,'AWS'),(13,'c5.24xlarge','c5','24xlarge',196608,96,0,0,25,0,'AWS'),(14,'c5.2xlarge','c5','2xlarge',16384,8,0,0,10,0,'AWS'),(15,'c5.4xlarge','c5','4xlarge',32768,16,0,0,10,1,'AWS'),(16,'c5.9xlarge','c5','9xlarge',73728,36,0,0,10,2,'AWS'),(17,'c5.large','c5','large',4096,2,0,0,10,0,'AWS'),(18,'c5.xlarge','c5','xlarge',8192,4,0,0,10,0,'AWS'),(19,'c5d.12xlarge','c5d','12xlarge',98304,48,1800,0,12,0,'AWS'),(20,'c5d.18xlarge','c5d','18xlarge',147456,72,1800,0,25,3,'AWS'),(21,'c5d.24xlarge','c5d','24xlarge',196608,96,3600,0,25,0,'AWS'),(22,'c5d.2xlarge','c5d','2xlarge',16384,8,200,0,10,0,'AWS'),(23,'c5d.4xlarge','c5d','4xlarge',32768,16,400,0,10,1,'AWS'),(24,'c5d.9xlarge','c5d','9xlarge',73728,36,900,0,10,2,'AWS'),(25,'c5d.large','c5d','large',4096,2,50,0,10,0,'AWS'),(26,'c5d.xlarge','c5d','xlarge',8192,4,100,0,10,0,'AWS'),(27,'c5n.18xlarge','c5n','18xlarge',196608,72,0,0,100,0,'AWS'),(28,'c5n.2xlarge','c5n','2xlarge',21504,8,0,0,25,0,'AWS'),(29,'c5n.4xlarge','c5n','4xlarge',43008,16,0,0,25,0,'AWS'),(30,'c5n.9xlarge','c5n','9xlarge',98304,36,0,0,50,0,'AWS'),(31,'c5n.large','c5n','large',5376,2,0,0,25,0,'AWS'),(32,'c5n.xlarge','c5n','xlarge',10752,4,0,0,25,0,'AWS'),(33,'d2.2xlarge','d2','2xlarge',62464,8,12000,0,0,1,'AWS'),(34,'d2.4xlarge','d2','4xlarge',124928,16,24000,0,0,3,'AWS'),(35,'d2.8xlarge','d2','8xlarge',249856,36,48000,0,10,6,'AWS'),(36,'d2.xlarge','d2','xlarge',31232,4,6000,0,0,1,'AWS'),(37,'g3.16xlarge','g3','16xlarge',499712,64,0,4,20,5,'AWS'),(38,'g3.4xlarge','g3','4xlarge',124928,16,0,1,10,1,'AWS'),(39,'g3.8xlarge','g3','8xlarge',249856,32,0,2,10,2,'AWS'),(40,'g3s.xlarge','g3s','xlarge',31232,4,0,1,10,0,'AWS'),(41,'g4dn.12xlarge','g4dn','12xlarge',196608,48,900,4,50,0,'AWS'),(42,'g4dn.16xlarge','g4dn','16xlarge',262144,64,900,1,50,0,'AWS'),(43,'g4dn.2xlarge','g4dn','2xlarge',32768,8,225,1,25,0,'AWS'),(44,'g4dn.4xlarge','g4dn','4xlarge',65536,16,225,1,25,0,'AWS'),(45,'g4dn.8xlarge','g4dn','8xlarge',131072,32,900,1,50,0,'AWS'),(46,'g4dn.xlarge','g4dn','xlarge',16384,4,125,1,25,0,'AWS'),(47,'h1.16xlarge','h1','16xlarge',262144,64,16000,0,25,4,'AWS'),(48,'h1.2xlarge','h1','2xlarge',32768,8,2000,0,10,0,'AWS'),(49,'h1.4xlarge','h1','4xlarge',65536,16,4000,0,10,1,'AWS'),(50,'h1.8xlarge','h1','8xlarge',131072,32,8000,0,10,2,'AWS'),(51,'i2.2xlarge','i2','2xlarge',62464,8,1600,0,0,2,'AWS'),(52,'i2.4xlarge','i2','4xlarge',124928,16,3200,0,0,3,'AWS'),(53,'i2.8xlarge','i2','8xlarge',249856,32,6400,0,10,7,'AWS'),(54,'i2.xlarge','i2','xlarge',31232,4,800,0,0,1,'AWS'),(55,'i3.16xlarge','i3','16xlarge',499712,64,15200,0,20,5,'AWS'),(56,'i3.2xlarge','i3','2xlarge',62464,8,1900,0,10,1,'AWS'),(57,'i3.4xlarge','i3','4xlarge',124928,16,3800,0,10,1,'AWS'),(58,'i3.8xlarge','i3','8xlarge',249856,32,7600,0,10,2,'AWS'),(59,'i3.large','i3','large',15616,2,475,0,10,0,'AWS'),(60,'i3.xlarge','i3','xlarge',31232,4,950,0,10,0,'AWS'),(61,'i3en.12xlarge','i3en','12xlarge',393216,48,30000,0,50,0,'AWS'),(62,'i3en.24xlarge','i3en','24xlarge',786432,96,60000,0,100,0,'AWS'),(63,'i3en.2xlarge','i3en','2xlarge',65536,8,5000,0,25,0,'AWS'),(64,'i3en.3xlarge','i3en','3xlarge',98304,12,7500,0,25,0,'AWS'),(65,'i3en.6xlarge','i3en','6xlarge',196608,24,15000,0,25,0,'AWS'),(66,'i3en.large','i3en','large',16384,2,1250,0,25,0,'AWS'),(67,'i3en.xlarge','i3en','xlarge',32768,4,2500,0,25,0,'AWS'),(68,'m4.10xlarge','m4','10xlarge',163840,40,0,0,10,2,'AWS'),(69,'m4.16xlarge','m4','16xlarge',262144,64,0,0,20,3,'AWS'),(70,'m4.2xlarge','m4','2xlarge',32768,8,0,0,0,0,'AWS'),(71,'m4.4xlarge','m4','4xlarge',65536,16,0,0,0,1,'AWS'),(72,'m4.large','m4','large',8192,2,0,0,0,0,'AWS'),(73,'m4.xlarge','m4','xlarge',16384,4,0,0,0,0,'AWS'),(74,'m5.12xlarge','m5','12xlarge',196608,48,0,0,10,2,'AWS'),(75,'m5.16xlarge','m5','16xlarge',262144,64,0,0,20,0,'AWS'),(76,'m5.24xlarge','m5','24xlarge',393216,96,0,0,25,5,'AWS'),(77,'m5.2xlarge','m5','2xlarge',32768,8,0,0,10,0,'AWS'),(78,'m5.4xlarge','m5','4xlarge',65536,16,0,0,10,1,'AWS'),(79,'m5.8xlarge','m5','8xlarge',131072,32,0,0,10,0,'AWS'),(80,'m5.large','m5','large',8192,2,0,0,10,0,'AWS'),(81,'m5.metal','m5','metal',393216,96,0,0,25,0,'AWS'),(82,'m5.xlarge','m5','xlarge',16384,4,0,0,10,0,'AWS'),(83,'m5a.12xlarge','m5a','12xlarge',196608,48,0,0,10,0,'AWS'),(84,'m5a.16xlarge','m5a','16xlarge',262144,64,0,0,12,0,'AWS'),(85,'m5a.24xlarge','m5a','24xlarge',393216,96,0,0,20,0,'AWS'),(86,'m5a.2xlarge','m5a','2xlarge',32768,8,0,0,10,0,'AWS'),(87,'m5a.4xlarge','m5a','4xlarge',65536,16,0,0,10,0,'AWS'),(88,'m5a.8xlarge','m5a','8xlarge',131072,32,0,0,10,0,'AWS'),(89,'m5a.large','m5a','large',8192,2,0,0,10,0,'AWS'),(90,'m5a.xlarge','m5a','xlarge',16384,4,0,0,10,0,'AWS'),(91,'m5ad.12xlarge','m5ad','12xlarge',196608,48,1800,0,10,0,'AWS'),(92,'m5ad.24xlarge','m5ad','24xlarge',393216,96,3600,0,20,0,'AWS'),(93,'m5ad.2xlarge','m5ad','2xlarge',32768,8,300,0,10,0,'AWS'),(94,'m5ad.4xlarge','m5ad','4xlarge',65536,16,600,0,10,0,'AWS'),(95,'m5ad.large','m5ad','large',8192,2,75,0,10,0,'AWS'),(96,'m5ad.xlarge','m5ad','xlarge',16384,4,150,0,10,0,'AWS'),(97,'m5d.12xlarge','m5d','12xlarge',196608,48,1800,0,10,3,'AWS'),(98,'m5d.16xlarge','m5d','16xlarge',262144,64,2400,0,20,0,'AWS'),(99,'m5d.24xlarge','m5d','24xlarge',393216,96,3600,0,25,5,'AWS'),(100,'m5d.2xlarge','m5d','2xlarge',32768,8,300,0,10,0,'AWS'),(101,'m5d.4xlarge','m5d','4xlarge',65536,16,600,0,10,1,'AWS'),(102,'m5d.8xlarge','m5d','8xlarge',131072,32,1200,0,10,0,'AWS'),(103,'m5d.large','m5d','large',8192,2,75,0,10,0,'AWS'),(104,'m5d.xlarge','m5d','xlarge',16384,4,150,0,10,0,'AWS'),(105,'m5dn.12xlarge','m5dn','12xlarge',196608,48,1800,0,50,0,'AWS'),(106,'m5dn.16xlarge','m5dn','16xlarge',262144,64,2400,0,75,0,'AWS'),(107,'m5dn.24xlarge','m5dn','24xlarge',393216,96,3600,0,100,0,'AWS'),(108,'m5dn.2xlarge','m5dn','2xlarge',32768,8,300,0,25,0,'AWS'),(109,'m5dn.4xlarge','m5dn','4xlarge',65536,16,600,0,25,0,'AWS'),(110,'m5dn.8xlarge','m5dn','8xlarge',131072,32,1200,0,25,0,'AWS'),(111,'m5dn.large','m5dn','large',8192,2,75,0,25,0,'AWS'),(112,'m5dn.xlarge','m5dn','xlarge',16384,4,150,0,25,0,'AWS'),(113,'m5n.12xlarge','m5n','12xlarge',196608,48,0,0,50,0,'AWS'),(114,'m5n.16xlarge','m5n','16xlarge',262144,64,0,0,75,0,'AWS'),(115,'m5n.24xlarge','m5n','24xlarge',393216,96,0,0,100,0,'AWS'),(116,'m5n.2xlarge','m5n','2xlarge',32768,8,0,0,25,0,'AWS'),(117,'m5n.4xlarge','m5n','4xlarge',65536,16,0,0,25,0,'AWS'),(118,'m5n.8xlarge','m5n','8xlarge',131072,32,0,0,25,0,'AWS'),(119,'m5n.large','m5n','large',8192,2,0,0,25,0,'AWS'),(120,'m5n.xlarge','m5n','xlarge',16384,4,0,0,25,0,'AWS'),(121,'p2.16xlarge','p2','16xlarge',749568,64,0,16,20,14,'AWS'),(122,'p2.8xlarge','p2','8xlarge',499712,32,0,8,10,7,'AWS'),(123,'p2.xlarge','p2','xlarge',62464,4,0,1,0,1,'AWS'),(124,'p3.16xlarge','p3','16xlarge',499712,64,0,8,25,24,'AWS'),(125,'p3.2xlarge','p3','2xlarge',62464,8,0,1,10,3,'AWS'),(126,'p3.8xlarge','p3','8xlarge',249856,32,0,4,10,12,'AWS'),(127,'r3.2xlarge','r3','2xlarge',62464,8,160,0,0,1,'AWS'),(128,'r3.4xlarge','r3','4xlarge',124928,16,320,0,0,1,'AWS'),(129,'r3.8xlarge','r3','8xlarge',249856,32,640,0,10,3,'AWS'),(130,'r3.large','r3','large',15616,2,32,0,0,0,'AWS'),(131,'r3.xlarge','r3','xlarge',31232,4,80,0,0,0,'AWS'),(132,'r4.16xlarge','r4','16xlarge',499712,64,0,0,20,4,'AWS'),(133,'r4.2xlarge','r4','2xlarge',62464,8,0,0,10,1,'AWS'),(134,'r4.4xlarge','r4','4xlarge',124928,16,0,0,10,1,'AWS'),(135,'r4.8xlarge','r4','8xlarge',249856,32,0,0,10,2,'AWS'),(136,'r4.large','r4','large',15616,2,0,0,10,0,'AWS'),(137,'r4.xlarge','r4','xlarge',31232,4,0,0,10,0,'AWS'),(138,'r5.12xlarge','r5','12xlarge',393216,48,0,0,10,0,'AWS'),(139,'r5.16xlarge','r5','16xlarge',524288,64,0,0,20,0,'AWS'),(140,'r5.24xlarge','r5','24xlarge',786432,96,0,0,25,0,'AWS'),(141,'r5.2xlarge','r5','2xlarge',65536,8,0,0,10,0,'AWS'),(142,'r5.4xlarge','r5','4xlarge',131072,16,0,0,10,0,'AWS'),(143,'r5.8xlarge','r5','8xlarge',262144,32,0,0,10,0,'AWS'),(144,'r5.large','r5','large',16384,2,0,0,10,0,'AWS'),(145,'r5.xlarge','r5','xlarge',32768,4,0,0,10,0,'AWS'),(146,'r5a.12xlarge','r5a','12xlarge',393216,48,0,0,10,0,'AWS'),(147,'r5a.16xlarge','r5a','16xlarge',524288,64,0,0,12,0,'AWS'),(148,'r5a.24xlarge','r5a','24xlarge',786432,96,0,0,20,0,'AWS'),(149,'r5a.2xlarge','r5a','2xlarge',65536,8,0,0,10,0,'AWS'),(150,'r5a.4xlarge','r5a','4xlarge',131072,16,0,0,10,0,'AWS'),(151,'r5a.8xlarge','r5a','8xlarge',262144,32,0,0,10,0,'AWS'),(152,'r5a.large','r5a','large',16384,2,0,0,10,0,'AWS'),(153,'r5a.xlarge','r5a','xlarge',32768,4,0,0,10,0,'AWS'),(154,'r5ad.12xlarge','r5ad','12xlarge',393216,48,1800,0,10,0,'AWS'),(155,'r5ad.24xlarge','r5ad','24xlarge',786432,96,3600,0,20,0,'AWS'),(156,'r5ad.2xlarge','r5ad','2xlarge',65536,8,300,0,10,0,'AWS'),(157,'r5ad.4xlarge','r5ad','4xlarge',131072,16,600,0,10,0,'AWS'),(158,'r5ad.large','r5ad','large',16384,2,75,0,10,0,'AWS'),(159,'r5ad.xlarge','r5ad','xlarge',32768,4,150,0,10,0,'AWS'),(160,'r5d.12xlarge','r5d','12xlarge',393216,48,1800,0,10,0,'AWS'),(161,'r5d.16xlarge','r5d','16xlarge',524288,64,2400,0,20,0,'AWS'),(162,'r5d.24xlarge','r5d','24xlarge',786432,96,3600,0,25,0,'AWS'),(163,'r5d.2xlarge','r5d','2xlarge',65536,8,300,0,10,0,'AWS'),(164,'r5d.4xlarge','r5d','4xlarge',131072,16,600,0,10,0,'AWS'),(165,'r5d.8xlarge','r5d','8xlarge',262144,32,1200,0,10,0,'AWS'),(166,'r5d.large','r5d','large',16384,2,75,0,10,0,'AWS'),(167,'r5d.xlarge','r5d','xlarge',32768,4,150,0,10,0,'AWS'),(168,'r5dn.12xlarge','r5dn','12xlarge',393216,48,1800,0,50,0,'AWS'),(169,'r5dn.16xlarge','r5dn','16xlarge',524288,64,2400,0,75,0,'AWS'),(170,'r5dn.24xlarge','r5dn','24xlarge',786432,96,3600,0,100,0,'AWS'),(171,'r5dn.2xlarge','r5dn','2xlarge',65536,8,300,0,25,0,'AWS'),(172,'r5dn.4xlarge','r5dn','4xlarge',131072,16,600,0,25,0,'AWS'),(173,'r5dn.8xlarge','r5dn','8xlarge',262144,32,1200,0,25,0,'AWS'),(174,'r5dn.large','r5dn','large',16384,2,75,0,25,0,'AWS'),(175,'r5dn.xlarge','r5dn','xlarge',32768,4,150,0,25,0,'AWS'),(176,'r5n.12xlarge','r5n','12xlarge',393216,48,0,0,50,0,'AWS'),(177,'r5n.16xlarge','r5n','16xlarge',524288,64,0,0,75,0,'AWS'),(178,'r5n.24xlarge','r5n','24xlarge',786432,96,0,0,100,0,'AWS'),(179,'r5n.2xlarge','r5n','2xlarge',65536,8,0,0,25,0,'AWS'),(180,'r5n.4xlarge','r5n','4xlarge',131072,16,0,0,25,0,'AWS'),(181,'r5n.8xlarge','r5n','8xlarge',262144,32,0,0,25,0,'AWS'),(182,'r5n.large','r5n','large',16384,2,0,0,25,0,'AWS'),(183,'r5n.xlarge','r5n','xlarge',32768,4,0,0,25,0,'AWS'),(184,'t2.2xlarge','t2','2xlarge',32768,8,0,0,0,0,'AWS'),(185,'t2.large','t2','large',8192,2,0,0,0,0,'AWS'),(186,'t2.medium','t2','medium',4096,2,0,0,0,0,'AWS'),(187,'t2.micro','t2','micro',1024,1,0,0,0,0,'AWS'),(188,'t2.nano','t2','nano',512,1,0,0,0,0,'AWS'),(189,'t2.small','t2','small',2048,1,0,0,0,0,'AWS'),(190,'t2.xlarge','t2','xlarge',16384,4,0,0,0,0,'AWS'),(191,'t3.2xlarge','t3','2xlarge',32768,8,0,0,0,0,'AWS'),(192,'t3.large','t3','large',8192,2,0,0,0,0,'AWS'),(193,'t3.medium','t3','medium',4096,2,0,0,0,0,'AWS'),(194,'t3.micro','t3','micro',1024,2,0,0,0,0,'AWS'),(195,'t3.nano','t3','nano',512,2,0,0,0,0,'AWS'),(196,'t3.small','t3','small',2048,2,0,0,0,0,'AWS'),(197,'t3.xlarge','t3','xlarge',16384,4,0,0,0,0,'AWS'),(198,'t3a.2xlarge','t3a','2xlarge',32768,8,0,0,0,0,'AWS'),(199,'t3a.large','t3a','large',8192,2,0,0,0,0,'AWS'),(200,'t3a.medium','t3a','medium',4096,2,0,0,0,0,'AWS'),(201,'t3a.micro','t3a','micro',1024,2,0,0,0,0,'AWS'),(202,'t3a.nano','t3a','nano',512,2,0,0,0,0,'AWS'),(203,'t3a.small','t3a','small',2048,2,0,0,0,0,'AWS'),(204,'t3a.xlarge','t3a','xlarge',16384,4,0,0,0,0,'AWS'),(205,'x1.16xlarge','x1','16xlarge',999424,64,1920,0,0,7,'AWS'),(206,'x1.32xlarge','x1','32xlarge',1998848,128,3840,0,0,13,'AWS'),(207,'x1e.16xlarge','x1e','16xlarge',1998848,64,1920,0,10,0,'AWS'),(208,'x1e.2xlarge','x1e','2xlarge',249856,8,240,0,10,0,'AWS'),(209,'x1e.32xlarge','x1e','32xlarge',3997696,128,3840,0,25,0,'AWS'),(210,'x1e.4xlarge','x1e','4xlarge',499712,16,480,0,10,0,'AWS'),(211,'x1e.8xlarge','x1e','8xlarge',999424,32,960,0,10,0,'AWS'),(212,'x1e.xlarge','x1e','xlarge',124928,4,120,0,10,0,'AWS'),(213,'z1d.12xlarge','z1d','12xlarge',393216,48,1800,0,25,0,'AWS'),(214,'z1d.2xlarge','z1d','2xlarge',65536,8,300,0,10,0,'AWS'),(215,'z1d.3xlarge','z1d','3xlarge',98304,12,450,0,10,0,'AWS'),(216,'z1d.6xlarge','z1d','6xlarge',196608,24,900,0,10,0,'AWS'),(217,'z1d.large','z1d','large',16384,2,75,0,10,0,'AWS'),(218,'z1d.xlarge','z1d','xlarge',32768,4,150,0,10,0,'AWS');
/*!40000 ALTER TABLE `aws_instances_nonull` ENABLE KEYS */;
UNLOCK TABLES;

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
  CONSTRAINT `benchmark_ibfk_1` FOREIGN KEY (`inst_id`) REFERENCES `instance_stub` (`id`)
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
-- Table structure for table `instance_stub`
--

DROP TABLE IF EXISTS `instance_stub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instance_stub` (
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
-- Dumping data for table `instance_stub`
--

LOCK TABLES `instance_stub` WRITE;
/*!40000 ALTER TABLE `instance_stub` DISABLE KEYS */;
INSERT INTO `instance_stub` (`id`, `provider`, `type`, `tier`, `cpu`, `gpu`, `memory`) VALUES (1,'AWS','t1','micro',4,1,16),(2,'GCE','small','1',1,1,16),(3,'AWS','s1','micro',4,1,16);
/*!40000 ALTER TABLE `instance_stub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sizes_full`
--

DROP TABLE IF EXISTS `sizes_full`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sizes_full` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(11) GENERATED ALWAYS AS (concat(left(`provider`,3),left(`type`,3),left(`size`,3),right(`size`,2))) STORED,
  `name` varchar(22) DEFAULT NULL,
  `provider` varchar(8) DEFAULT NULL,
  `type` varchar(6) DEFAULT NULL,
  `size` varchar(12) DEFAULT NULL,
  `cpu` int DEFAULT '0',
  `gpu` int DEFAULT '0',
  `ram` int DEFAULT '0',
  `bandwidth` int DEFAULT '0',
  `price` float DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `tag_UNIQUE` (`tag`)
) ENGINE=InnoDB AUTO_INCREMENT=219 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sizes_full`
--

LOCK TABLES `sizes_full` WRITE;
/*!40000 ALTER TABLE `sizes_full` DISABLE KEYS */;
/*!40000 ALTER TABLE `sizes_full` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sizes_lite`
--

DROP TABLE IF EXISTS `sizes_lite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sizes_lite` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `tag` varchar(11) GENERATED ALWAYS AS (concat(left(`provider`,3),left(`type`,3),left(`size`,3),right(`size`,2))) STORED,
  `name` varchar(22) DEFAULT NULL,
  `provider` varchar(8) DEFAULT NULL,
  `type` varchar(6) DEFAULT NULL,
  `size` varchar(12) DEFAULT NULL,
  `cpu` int DEFAULT '0',
  `gpu` int DEFAULT '0',
  `ram` int DEFAULT '0',
  `bandwidth` int DEFAULT '0',
  `price` float DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `tag_UNIQUE` (`tag`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1138 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sizes_lite`
--

LOCK TABLES `sizes_lite` WRITE;
/*!40000 ALTER TABLE `sizes_lite` DISABLE KEYS */;
/*!40000 ALTER TABLE `sizes_lite` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-10 20:31:25
