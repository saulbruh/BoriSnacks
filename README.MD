# BoriSnacks

BoriSnacks es una página e-commerce de meriendas típicas puertorriqueñas, dirigidas al público fuera de Puerto Rico. Muchas personas de otros países no conocen de la cultura culinaria de Puerto Rico o no es bien accesible para gente de lugares lejanos que deseen probar un poco del sabor Boricua, por eso queremos crear un servicio que ofrezca, de manera accesible y costo-efectiva, una variedad de productos típicos como dulces, comestibles y bebidas. La página cuenta con varias funcionalidades que son necesarias para las tareas que normalmente se realizan en páginas como estas, tal como log in, carrito de compras, crear una orden, entre otras.

La aplicación cuenta con un sistema de base de datos para poder cargar los artículos y poder almacenar los usuarios cuando se registren, entre otras cosas. La misma también cuenta con una interfaz moderna e intuitiva que es fácil de navegar y utilizar.

Este proyecto es dirigido a la clase de Software Engineering (COMP3402) por el Prof. Javier 

Dastas. Los integrantes del grupo BoriSnacks son:

    - Saúl J. Medina Vega
    - Janiel O. Rodríguez Velázquez
    - Ricardo A. Adorno Pérez
    - Yael F. Maldonado Díaz

---

###  PDF
[Ver más a detalle información sobre el proyecto](docs/borisnacksInfo.pdf)

### Ver video
[Ver más a detalle información sobre el proyecto](https://youtu.be/JyQ1JRU56aM)

## Características
- Registro e inicio de sesión seguro.
- Carrito de compras integrado.
- Sistema de autenticación con Flask y MariaDB.

## Endpoints Principales

### 📍 Página de Inicio
**Ruta:** `/`  
**Descripción:** Muestra la lista de productos disponibles.  

### 📍 Detalle de Producto
**Ruta:** `/producto/<int:id>`  
**Descripción:** Muestra los detalles de un producto específico y productos relacionados.

### 📍 Registro de Usuarios
**Ruta:** `/registro`  
**Método:** `GET, POST`  
**Descripción:** Permite a nuevos usuarios registrarse en la plataforma.

### 📍 Inicio de Sesión
**Ruta:** `/login`  
**Método:** `GET, POST`  
**Descripción:** Inicia sesión y almacena los datos en la sesión del usuario.

### 📍 Gestión de Direcciones
**Ruta:** `/register_address`  
**Método:** `GET, POST`  
**Descripción:** Permite a los usuarios registrar y gestionar sus direcciones de envío.

### 📍 Cierre de Sesión
**Ruta:** `/logout`  
**Descripción:** Cierra la sesión del usuario y lo redirige a la página de inicio.  

### 📍 Acerca de
**Ruta:** `/about`  
**Descripción:** Muestra información sobre la plataforma.

### 📍 Carrito de Compras
**Ruta:** `/carrito`  
**Descripción:** Permite a los usuarios ver y gestionar su carrito de compras.

### 📍 Gestión del Carrito
**Ruta:** `/modificar_cantidad`  
**Método:** `POST`  
**Descripción:** Modifica la cantidad de un producto en el carrito.

**Ruta:** `/agregar_al_carrito`  
**Método:** `POST`  
**Descripción:** Agrega un producto al carrito de compras.

**Ruta:** `/eliminar_del_carrito`  
**Método:** `POST`  
**Descripción:** Elimina un producto del carrito de compras.

**Ruta:** `/vaciar_carrito`  
**Método:** `POST`  
**Descripción:** Vacía completamente el carrito de compras.

### 📍 Gestión de Órdenes
**Ruta:** `/crear_orden`  
**Método:** `GET`  
**Descripción:** Muestra el formulario para crear una nueva orden con los productos del carrito.

**Ruta:** `/procesar_orden`  
**Método:** `POST`  
**Descripción:** Procesa la orden del usuario y actualiza el inventario.

### 📍 Perfil y Gestión de Usuario
**Ruta:** `/profile`  
**Descripción:** Muestra la información del usuario autenticado.

**Ruta:** `/profile/home`  
**Método:** `GET, POST`  
**Descripción:** Página principal del perfil del usuario.

**Ruta:** `/profile/orders`  
**Descripción:** Muestra el historial de órdenes del usuario.

**Ruta:** `/orden/<int:orden_id>`  
**Descripción:** Muestra los detalles de una orden específica.

**Ruta:** `/delete_account`  
**Método:** `GET, POST`  
**Descripción:** Permite a los usuarios eliminar su cuenta de la plataforma previa confirmación de contraseña.  

### 📍 Recuperación de Contraseña
**Ruta:** `/reset_password_request`  
**Método:** `POST`  
**Descripción:** Permite a los usuarios solicitar un enlace para restablecer su contraseña.  

**Ruta:** `/reset_password/<token>`  
**Método:** `GET, POST`  
**Descripción:** Permite a los usuarios restablecer su contraseña utilizando un token enviado por correo electrónico.  

### 📍 Categorías de Productos
**Ruta:** `/snacks`  
**Descripción:** Muestra los productos de la categoría snacks.

**Ruta:** `/drinks`  
**Descripción:** Muestra los productos de la categoría bebidas.

**Ruta:** `/candy`  
**Descripción:** Muestra los productos de la categoría dulces.

**Ruta:** `/all_products`  
**Descripción:** Muestra todos los productos disponibles.