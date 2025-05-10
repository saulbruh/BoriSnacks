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

-- (Sin datos insertados en esta tabla)

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

-- (Sin datos insertados en esta tabla)

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

-- (Sin datos insertados en esta tabla)

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

-- (Sin datos insertados en esta tabla)

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

-- (Sin datos insertados en esta tabla)

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

--
-- Se insertan los datos de la tabla`productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES
(1,'Pilón de coco ','Pilón de coco is a traditional Caribbean sweet, especially popular in Puerto Rico. It is made with grated coconut, sugar, and spices such as cinnamon and vanilla, cooked until it reaches a caramelized and compact texture. It is then shaped into individual portions and left to cool. Its flavor is sweet and intense, with a characteristic tropical touch from the coconut.',1.49,'Dulce','images/imagen1.webp',15),
(2,'Pilón de piña ','Pilón de piña is a traditional Puerto Rican sweet made from caramelized pineapple and sugar, shaped into small cylinders or cones. Its texture is firm yet chewy, and its flavor is a combination of intense sweetness with the characteristic tartness of pineapple.',1.49,'Dulce','images/imagen2.webp',14),
(3,'Pilón rojo','Pilón rojo is a traditional Puerto Rican sweet made from sugar, red coloring, and essences such as vanilla or cinnamon. Its preparation involves caramelizing the sugar until it reaches a hard and crunchy texture, then pouring it into molds or shaping it by hand. It is popular for its intense red color and sweet, caramelized flavor.',1.49,'Dulce','images/imagen3.webp',13),
(4,'Pilón de ajonjolí ','Pilón de ajonjolí is a traditional Puerto Rican sweet made with sesame seeds, sugar, and either honey or molasses. Its preparation involves caramelizing the sugar and mixing it with toasted seeds before shaping it into small portions. It has a crunchy texture and a sweet flavor with a distinct toasted and aromatic touch from the sesame.',1.49,'Dulce','images/imagen4.webp',14),
(5,'Pasta de guayaba ','Pasta de Guayaba is a traditional sweet made from guava pulp cooked with sugar until it reaches a firm and jelly-like consistency. It has a bright red color and a sweet, slightly tart flavor, with a smooth and dense texture. It is often enjoyed on its own or paired with cheese.',2.49,'Dulce','images/imagen5.webp',14),
(6,'Besitos de coco ','Besitos de coco are small sweets made primarily from grated coconut, sugar, and egg whites, baked until they achieve a crispy exterior and a soft interior. They have a sweet and delicious flavor with the distinctive tropical touch of coconut. They are perfect as bite-sized treats or as an accompaniment to drinks.',2.49,'Dulce','images/imagen6.webp',12),
(7,'Turrón de coco ','Turrón de coco is a traditional sweet made with grated coconut, sugar, and, in some versions, condensed milk or honey. It has a soft and slightly sticky texture, with a sweet and intense coconut flavor. It is popular in the Caribbean and Latin America, especially during festive celebrations.',3.49,'Dulce','images/imagen7.webp',12),
(8,'Dulce de coco ','Dulce de coco is a traditional Puerto Rican treat, highly cherished on the island, especially during celebrations and festivities. It is primarily made with grated coconut and sugar, with some variations including ingredients like milk or cinnamon to enhance its flavor. Its texture can be soft or slightly firm, and its sweet taste makes it a popular delight in Puerto Rican cuisine.',1.39,'Dulce','images/imagen8.webp',12),
(9,'Panky','Panky is a traditional Puerto Rican sweet, primarily made with flour, sugar, and butter. It has a soft texture and a sweet, buttery flavor. It is often served in small portions or cut into bar shapes. It is very popular during celebrations and as a snack on the island.',0.89,'Dulce','images/imagen9.webp',12),
(10,'Gofio de maíz ','Gofio de maíz is a traditional Puerto Rican sweet made from toasted corn and sugar. It has a soft texture and a sweet flavor, with a toasted taste characteristic of corn. It is a popular snack, especially enjoyed during festive occasions and as an afternoon treat.',1.49,'Dulce','images/imagen10.webp',8),
(11,'Marallo ','Marallo is a traditional Puerto Rican sweet made primarily from guava and sugar. It has a thick texture and a sweet flavor, with a fruity touch from the guava. It is very popular as a dessert or snack on the island.',4.89,'Dulce','images/imagen11.webp',8),
(12,'Galletas de Jengibre ','Galletas de jengibre orocobeñas are a traditional sweet from Orocovis, a municipality located in the center of Puerto Rico. These cookies, especially popular during Christmas, are characterized by their spiced and crunchy flavor, with a hint of ginger, cinnamon, and clove. They are known for their light texture and unique aroma, making them a typical treat during festive occasions and family celebrations in the region.',4.49,'Dulce','images/imagen12.webp',8),
(13,'Polvorones ','Polvorones are a traditional Puerto Rican sweet, known for their crumbly and soft texture. They are made with lard, sugar, flour, and sometimes almonds or peanuts, giving them a sweet and slightly buttery flavor. They are especially popular during the holiday season and family celebrations.',2.50,'Dulce','images/imagen13.webp',12),
(14,'Mini Grajeas','Mini grajeas are a traditional Puerto Rican sweet, small sugar balls coated with a crunchy and colorful layer. They are similar to candy-coated treats but in a smaller size. They have a sweet flavor and are commonly enjoyed during holidays and celebrations. They are especially popular among children due to their size and vibrant colors.',1.49,'Dulce','images/imagen14.webp',8),
(15,'Merenguitos ','Merenguitos are a traditional Puerto Rican sweet, known for their light and crunchy texture. They are made primarily from egg whites and sugar, whipped until airy and then baked until firm. Their flavor is sweet and delicate, and they are typically white, although they can also be found in various colors. Meringues are popular during celebrations, especially at Christmas.',2.99,'Dulce','images/imagen15.webp',22),
(16,'Ajonjolí ','Dulce de ajonjolí is a traditional snack made with toasted sesame seeds and a caramelized sugar syrup, which is compacted to form blocks or bars. Its flavor is sweet and slightly toasted, with a crunchy texture that highlights the characteristic taste of sesame seeds. It is a popular sweet in Puerto Rico.',1.39,'Merienda','images/imagen16.webp',11),
(17,'Carmela Bites ','Carmela Bites are small sausages typically served in easy-to-eat bite-sized pieces. They are soft and juicy, with a savory flavor and tender texture. They are ideal as appetizers or snacks at gatherings and celebrations. They come in various varieties, such as chicken, pork, or beef, and are seasoned with a blend of spices that enhance their flavor. They can be enjoyed on their own or paired with sauces for an extra burst of taste.',0.99,'Merienda','images/imagen17.webp',2),
(18,'Platanutres ','Platanutres are a popular fried plantain snack, widely consumed in Puerto Rico. They are made from green plantains, which are sliced thin and then fried until crispy. The result is a salty and crunchy snack with a mild but delicious flavor. They are typically packaged in bags, and sometimes seasoned with spices or seasonings for an extra burst of flavor. They are perfect as a snack, side dish, or for munching between meals.',2.49,'Merienda','images/imagen18.webp',13),
(19,'Cheese balls snackman ','Cheese Balls Snackman are a type of crunchy snack with a cheese flavor, shaped into small balls. They are very popular for their strong and delicious cheese taste, and their light, airy texture. These snacks are perfect for munching at any time, especially at gatherings or as part of a snack. Additionally, their small size makes them easy to eat in one bite, and their cheese flavor makes them a favorite among fans of savory snacks.',0.50,'Merienda','images/imagen19.webp',12),
(20,'Chicharrones jukiao','Chicharrones Jukiao are a crunchy and flavorful snack, popular in Puerto Rico. They are made from fried pork skin, which gives them a very crispy texture and an intense, salty flavor. They are usually served in small portions, perfect for snacking between meals or accompanying a drink. These chicharrones can come with different seasonings, such as chili or lime, to add an extra layer of flavor. They are a traditionally enjoyed snack, known for their authentic taste and crispy consistency.',2.99,'Merienda','images/imagen20.webp',19),
(21,'Export Sodas Rovira','Export Sodas Rovira are a traditional snack from Puerto Rico, known for their crunchy texture and versatile flavor. These crackers are made with enriched wheat flour, palm oil, salt, baking soda, malt syrup, corn syrup, and yeast, ingredients that contribute to their distinctive taste.',5.19,'Merienda','images/imagen21.webp',21),
(22,'Florecitas ','Florecitas are small, traditional sweet cookies from Puerto Rico, known for their distinctive shape and vanilla frosting. These cookies evoke childhood memories and are highly appreciated for their crunchy texture and sweet flavor.',2.99,'Merienda','images/imagen22.webp',14),
(23,'Galletas Duende ','Galletas Duende are a well-known type of cookie in Puerto Rico, recognized for their sweet flavor and crispy texture. These cookies are small and round in shape, characterized by their delicious vanilla flavor, although some versions may also have other flavors. They are perfect for pairing with a beverage such as coffee, milk, or tea, or simply for enjoying as a snack at any time of the day. Duende Cookies are a beloved option for their classic taste and versatility.',3.49,'Merienda','images/imagen23.webp',27),
(24,'Galletas Favoritas ','Galletas Favoritas are a well-known brand of cookies, especially recognized for their sweet flavor and crispy texture. These cookies typically have a classic recipe that includes ingredients like flour, sugar, butter, and a hint of vanilla. They are perfect for pairing with a beverage, such as coffee or milk, and are enjoyed both as a snack and at breakfast. Their popularity lies in their simple yet delicious flavor, making them an ideal snack for any occasion.',0.40,'Merienda','images/imagen24.webp',20),
(25,'Holsum Poundcake','Holsum Poundcake is known for its dense, soft, and moist texture. This cake has a classic, sweet flavor with a buttery base, making it perfect for pairing with a cup of coffee or tea. It is often enjoyed on its own or can be served with fresh fruit, ice cream, or frosting. Holsum Poundcake is appreciated for its fluffy consistency and comforting flavor, making it a popular choice for gatherings and as a dessert for special occasions.',5.68,'Merienda','images/imagen25.webp',16),
(26,'Holsum Sugar Donuts','Holsum Sugar Donuts are a delicious snack or breakfast treat, known for their sweet flavor and soft texture. These donuts are coated with a layer of sugar, giving them an extra touch of sweetness. They are perfect for pairing with a hot beverage like coffee or milk, or simply for enjoying as a snack at any time of the day. The Holsum brand is known for offering quality products, and their sugar donuts are appreciated for their classic flavor and freshness.',3.99,'Merienda','images/imagen26.webp',24),
(27,'Malta India','Malta India is a non-alcoholic malt beverage, very popular in Puerto Rico. It has a dark color, a sweet flavor, and a light caramel-like touch, with a thick and bubbly texture. It is made from malted barley and hops, similar to beer, but without alcoholic fermentation. It is an energizing and refreshing option, commonly enjoyed cold and, in some regions, mixed with condensed milk for a sweeter taste. Malta India is appreciated for its distinctive flavor profile and nutritional value.',0.99,'Bebida','images/imagen27.webp',8),
(28,'Chocolate Cortés en polvo ','Chocolate Cortés en Polvo Molido is a powdered version of the traditional Cortés Chocolate, ideal for quickly and conveniently preparing hot chocolate. It is made with high-quality cocoa and has a rich, authentic flavor. Its powdery texture allows it to dissolve easily in hot milk or water, creating a thick and delicious drink. It is perfect for accompanying breakfasts or snacks and can be sweetened to taste. Additionally, its ground format makes it easy to use in baking recipes and desserts.',3.33,'Bebida','images/imagen28.webp',30),
(29,'Chocolate Cortés sugar free ','El Chocolate Cortés Sugar Free is the sugar-free version of the classic Cortés Chocolate, ideal for those who want to enjoy its rich flavor without adding sugar. It is made with high-quality cocoa and sweetened with sugar-free alternatives, maintaining its creamy texture and intense flavor. It is perfect for preparing hot chocolate without worrying about excess sugar, and it can also be used in baking recipes or desserts. Its powdered format allows for easy dissolution in milk or water, offering a delicious and healthier option for chocolate lovers.',3.33,'Bebida','images/imagen29.webp',26),
(30,'Old Colony ','Old Colony is a popular soft drink in Puerto Rico, known for its distinctive sweet and fruity flavor. Its most famous variant is the grape flavor, with a vibrant purple hue and a refreshing touch. It is a classic soda that is enjoyed cold, either on its own or paired with meals.',0.99,'Bebida','images/imagen30.webp',19),
(31,'Piña Buena','Piña Buena is a soft drink with an intense pineapple flavor, popular in Puerto Rico. It is distinguished by its balanced sweetness and bubbly texture, offering a tropical and refreshing alternative for any occasion.',1.29,'Bebida','images/imagen31.webp',21),
(32,'Ok Kola Champagne ','OK Kola Champagne is a soft drink with a sweet and smooth flavor, characterized by hints of vanilla and caramel. Its golden color and distinctive flavor profile make it one of the most popular sodas in the Caribbean and Latin America. It is a refreshing and versatile beverage, perfect for pairing with meals or enjoying on its own at any time. Its effervescence and sweetness make it a classic choice for gatherings and celebrations.',0.99,'Bebida','images/imagen32.webp',9),
(33,'Café lareño','Café Lareño is a high-quality Puerto Rican coffee, known for its strong flavor and intense aroma. It is made from carefully selected and roasted beans to offer a cup with a robust body and slightly chocolaty notes. It is an ideal choice for coffee lovers seeking a rich and authentic experience. It can be enjoyed in various preparations, such as black coffee, espresso, or with milk, always highlighting its deep and balanced profile.',6.49,'Bebida','images/imagen33.webp',15),
(34,'Café Lareño especial','Café Lareño Especial is a premium version of the traditional Café Lareño, made with a selection of high-quality beans and a special roast that enhances its more refined and balanced flavor. It has an intense aroma and a smoother, more complex flavor profile, with subtle notes that make it ideal for coffee enthusiasts. Its well-balanced body and silky texture make it an excellent choice to enjoy on its own or with milk, offering a more sophisticated and delicious experience.',8.99,'Bebida','images/imagen34.webp',27),
(35,'Café oro ','Café Oro is a 100% Puerto Rican coffee, recognized for its robust flavor and intense aroma. It is grown in the mountains of Puerto Rico and made with high-quality beans, artisanally roasted to enhance its flavor profile with slightly chocolaty notes and a well-balanced body. It is an ideal option for those seeking a strong and authentic coffee, perfect for enjoying at any time of the day, whether black, with milk, or as espresso.',4.45,'Bebida','images/imagen35.webp',13),
(36,'Coco rico ','Coco Rico is a soft drink with a distinctive coconut flavor, very popular in the Caribbean and Latin America. Its combination of sweetness and effervescence makes it a refreshing and unique beverage, perfect to enjoy on its own or as an ingredient in tropical cocktails. With its natural coconut aroma and bubbly texture, Coco Rico is an ideal option for those looking for an exotic and different soft drink.',1.12,'Bebida','images/imagen36.webp',16);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;



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

-- (Sin datos insertados en esta tabla)



