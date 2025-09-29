CREATE DATABASE  IF NOT EXISTS `customer_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `customer_db`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: customer_db
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `membership` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Alice Updated','alice.johnson@example.com','Mumbai',25,'9876543210','Silver'),(3,'Charlie Brown','charlie.brown@example.com','Delhi',28,'9988776655','Silver'),(4,'David Wilson','david.wilson@example.com','Bangalore',35,'9876501234','Platinum'),(5,'Eva Davis','eva.davis@example.com','Hyderabad',22,'9123409876','Silver'),(6,'Frank Miller','frank.miller@example.com','Pune',40,'9012345678','Gold'),(7,'Grace Lee','grace.lee@example.com','Mumbai',29,'9876123456','Silver'),(8,'Henry Clark','henry.clark@example.com','Chennai',33,'9123987654','Gold'),(9,'Ivy Lewis','ivy.lewis@example.com','Kolkata',26,'9988112233','Silver'),(10,'Jack Walker','jack.walker@example.com','Pune',31,'9876541122','Gold'),(11,'Kathy Hall','kathy.hall@example.com','Delhi',27,'9123459876','Silver'),(12,'Leo Young','leo.young@example.com','Mumbai',34,'9988771234','Gold'),(13,'Mona Allen','mona.allen@example.com','Bangalore',23,'9876509876','Silver'),(14,'Nina Scott','nina.scott@example.com','Hyderabad',36,'9123498765','Platinum'),(22,'Ravi Kumar','ravi.k@example.com','Hyderabad',27,'9999911111','Platinum'),(23,'Raju Shet','raju.s@example.com','kolkata',29,'9123334432','Gold'),(25,'John Doe','john@example.com','Delhi',30,'9999999999','Gold'),(27,'sameer khan','samirkhan1@example.com','Kolhapur',30,'9561239999','Gold'),(28,'Sahil Kumar','sahilkumar@example.com','Kolhapur',30,'9991239999','Silver'),(29,'Sahil Kumar','sahilkumar@example.com','Kolhapur',30,'9991239999','Silver'),(30,'Sahil Kumar','sahilkumar@example.com','Kolhapur',30,'9991239999','Silver'),(31,'Sahil Kumar','sahilkumar@example.com','Kolhapur',30,'9991239999','Silver');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-28 11:58:50
