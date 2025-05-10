-- Dump de la base de datos `railway` (MariaDB 11.7.2)
-- Host: switchyard.proxy.rlwy.net

-- Configuración inicial
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

-- Tabla: carro_de_compra
DROP TABLE IF EXISTS `carro_de_compra`;
CREATE TABLE `carro_de_compra` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user` (`user_id`),
  CONSTRAINT `carro_de_compra_ibfk_1` 
    FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `carro_de_compra` (`id`, `user_id`) VALUES
  (11, 32),
  (12, 36),
  (13, 37);

-- Tabla: carro_de_compra_items
DROP TABLE IF EXISTS `carro_de_compra_items`;
CREATE TABLE `carro_de_compra_items` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `carro_de_compra_id` INT(11) NOT NULL,
  `product_item_id` INT(11) NOT NULL,
  `cantidad` INT(10) UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  CONSTRAINT `carro_de_compra_items_ibfk_1`
    FOREIGN KEY (`carro_de_compra_id`) REFERENCES `carro_de_compra` (`id`) ON DELETE CASCADE,
  CONSTRAINT `carro_de_compra_items_ibfk_2`
    FOREIGN KEY (`product_item_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- (Sin datos insertados en esta tabla)

-- Tabla: direcciones
DROP TABLE IF EXISTS `direcciones`;
CREATE TABLE `direcciones` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `calle1` VARCHAR(50) NOT NULL,
  `calle2` VARCHAR(50),
  `ciudad` VARCHAR(35) NOT NULL,
  `pais` VARCHAR(50),
  `codigo_postal` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `direcciones_ibfk_1` 
    FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `direcciones` VALUES
  (42, 32, 'Hc 2333', 'Box 17161333', 'Arecibo', 'PR', '00615'),
  (43, 37, 'Hc 2', 'Box 1716164t', 'Arecibo', 'PR', '004665'),
  (44, 37, 'Prueba', '12', 'Milán', 'IT', '87654332'),
  (46, 36, '123', '0000', 'nbvcxdfg', 'PR', 'ghkkkkkk');

-- Tabla: direcciones_ordenes
DROP TABLE IF EXISTS `direcciones_ordenes`;
CREATE TABLE `direcciones_ordenes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `calle1` VARCHAR(255),
  `calle2` VARCHAR(255),
  `ciudad` VARCHAR(100),
  `pais` VARCHAR(100),
  `codigo_postal` VARCHAR(20),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `direcciones_ordenes` VALUES
  (1, 'Prueba direccion regular', 'lol', 'Arecibo', 'PR', '00615'),
  (2, 'goofy ahh', '12345', 'Arecibooouu', 'AF', '00945'),
  (3, 'goofy ahh', '12345', 'Arecibooouu', 'AF', '00945'),
  (4, 'goofy ahh', '12345', 'Camuy', 'AF', '12345'),
  (5, 'goofy ahh', '12345', 'Camuy', 'AF', '12345'),
  (6, 'goofy ahh', '12345', 'Camuy', 'AF', '00945'),
  (7, 'Hc 2', 'Box 17161', 'Arecibo', 'PR', '00612'),
  (8, 'Hc 2333', 'Box 17161333', 'Arecibo', 'PR', '00615'),
  (9, 'Hc 2', 'Box 1716164t', 'Arecibo', 'PR', '004665'),
  (10, 'Hc 2', 'Box 1716164t', 'Arecibo', 'PR', '004665'),
  (11, 'Urb Del Carmen E101', '', 'Camuy', 'PR', '00627'),
  (12, 'Urb Del Carmen E101', '', 'Camuy', 'PR', '00627'),
  (13, '123', '0000', 'nbvcxdfg', 'PR', 'ghkkkkkk'),
  (14, 'Urb Del Carmen E101', '', 'Camuy', 'PR', '00627');

-- Tabla: orden_items
DROP TABLE IF EXISTS `orden_items`;
CREATE TABLE `orden_items` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `orden_id` INT(11) NOT NULL,
  `product_id` INT(11) NOT NULL,
  `cantidad` INT(10) UNSIGNED NOT NULL DEFAULT 1,
  `precio_unitario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `orden_items_ibfk_1`
    FOREIGN KEY (`orden_id`) REFERENCES `ordenes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `orden_items_ibfk_2`
    FOREIGN KEY (`product_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- (Aquí irían los INSERT, si deseas los ordeno también)

-- Tabla: ordenes
DROP TABLE IF EXISTS `ordenes`;
CREATE TABLE `ordenes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `fecha_orden` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  `metodo_pago` VARCHAR(20) NOT NULL,
  `total` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `direccion_id` INT(11),
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_direccion_orden`
    FOREIGN KEY (`direccion_id`) REFERENCES `direcciones_ordenes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: productos
DROP TABLE IF EXISTS `productos`;
CREATE TABLE `productos` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50),
  `descripcion` VARCHAR(1000),
  `precio` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `categoria` VARCHAR(25) NOT NULL,
  `imagen` VARCHAR(255),
  `stock` INT(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: usuarios
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(40) DEFAULT NULL,
  `correo_electronico` varchar(50) DEFAULT NULL,
  `hashed_password` varchar(255) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo_electronico` (`correo_electronico`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



