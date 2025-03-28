

# BoriSnacks

BoriSnacks es una plataforma de comercio local que permite a los usuarios explorar productos y realizar compras en línea.

Muchas personas de otros países no conocen de la cultura culinaria de Puerto Rico o no es bien accesible para gente de lugares lejanos que deseen probar un poco del sabor Boricua, por eso queremos crear un servicio que ofrezca, de manera accesible y costo-efectiva, una variedad de productos típicos como dulces, meriendas y bebidas.


- ### ¿Qué problema resuelve su proyecto?
    - El acceso simple a productos locales para personas que se encuentran fuera de la isla.

 - ### Inegrantes:
    - Saúl J. Medina Vega
    - Janiel O. Rodríguez Velázquez
    - Ricardo A. Adorno Pérez
    - Yael F. Maldonado Díaz

---

###  PDF
[Ver presentación sobre el proyecto](docs/borisnacksInfo.pdf)

## Instalación
1. Clona el repositorio.
2. Crear entorno virtual con `virtualenv` o directamente con python.
3. Instala dependencias con `pip install -r requirements.txt`.
4. Ejecuta el servidor con `python app.py`.

### Base de datos:
- La base de datos de este proyecto está despliégada en https://railway.com , para ver el diagrama de entidad - relación favor de observar el pdf del proyecto (ver arriba).

## Características
- Registro e inicio de sesión seguro.
- Carrito de compras integrado.
- Sistema de autenticación con Flask y MariaDB.

## Implementación de Carrito de Compras

El sistema de carrito de compras permite a los usuarios agregar productos a su carrito, visualizar los artículos agregados y proceder con la compra. Para esto, se utilizan las siguientes funciones:

- **Verificación de sesión**: Se requiere que el usuario inicie sesión para acceder a su carrito.
- **Manejo de carritos**: Si un usuario no tiene un carrito activo, se le asigna uno nuevo al acceder a la página.
- **Gestión de productos**: Se pueden agregar productos al carrito y se mantiene un registro de la cantidad seleccionada.
- **Redirección inteligente**: Si un usuario no ha iniciado sesión y accede al carrito, se le redirige al login y luego se le devuelve a la página del carrito.
- **Eliminación de cuenta**: Se incluye una opción para que los usuarios puedan eliminar su cuenta, previa confirmación de contraseña.

Para modificar o extender la funcionalidad del carrito, revisa el archivo `app.py` y edita las rutas relacionadas con `/carrito`.


## Tecnologías Utilizadas

| Tecnología  | Descripción |
|-------------|------------|
| **Flask**  | Framework de desarrollo web para Python. |
| **MariaDB**  | Base de datos SQL utilizada para almacenar usuarios, productos y pedidos. |
| **SQLAlchemy**  | Manejo de la base de datos (aunque en el código principal se usa conexión directa). |
| **Werkzeug**  | Seguridad y autenticación de contraseñas con hashing. |
| **Jinja2**  | Motor de plantillas para la generación dinámica de HTML. |

## Endpoints Principales

### 📍 Página de Inicio
**Ruta:** `/`  
**Descripción:** Muestra la lista de productos disponibles.  

### 📍 Registro de Usuarios
**Ruta:** `/registro`  
**Método:** `POST`  
**Descripción:** Permite a nuevos usuarios registrarse en la plataforma.

### 📍 Inicio de Sesión
**Ruta:** `/login`  
**Método:** `POST`  
**Descripción:** Inicia sesión y almacena los datos en la sesión del usuario.

### 📍 Cierre de Sesión
**Ruta:** `/logout`  
**Descripción:** Cierra sesión y limpia la sesión activa del usuario.

### 📍 Perfil del Usuario
**Ruta:** `/perfil`  
**Descripción:** Muestra la información del usuario autenticado.

### 📍 Carrito de Compras
**Ruta:** `/carrito`  
**Descripción:** Permite a los usuarios ver y gestionar su carrito de compras.

### 📍 Eliminar Cuenta
**Ruta:** `/delete_account`  
**Método:** `POST`  
**Descripción:** Elimina la cuenta del usuario autenticado tras confirmar su contraseña.

## Seguridad Implementada

- 🔒 **Contraseñas cifradas:** Se usa `bcrypt` para almacenar contraseñas de forma segura.
- 🔑 **Tokens de sesión:** Se utiliza `Flask-Session` para manejar sesiones de usuario.
- ❌ **Protección contra SQL Injection:** Se evita la interpolación de consultas directas usando `?` en consultas SQL.