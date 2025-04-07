from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
import mariadb  # type: ignore
import hashlib
from dotenv import load_dotenv
from country_list import countries_for_language
import os

load_dotenv()  # Cargar variables de entorno desde .env

app = Flask(__name__)
app.secret_key = "1234"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def check_logged_in():
    if 'user_id' in session:
        return redirect(url_for('usuario'))
    return None

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, categoria, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()

    productos_json = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": p[3], "categoria": p[4], "imagen": p[5], "stock": p[6]}
        for p in productos
    ]

    return render_template('index.html', productos=productos_json)

@app.route('/producto/<int:id>')
def producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, categoria, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()

    productos_json = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": p[3], "categoria": p[4], "imagen": p[5], "stock": p[6]}
        for p in productos
    ]

    producto = next((item for item in productos_json if item['id'] == id), None)
    if producto is None:
        return "Producto no encontrado", 404

    return render_template('product.html', producto=producto)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    redirect_if_logged_in = check_logged_in()
    if redirect_if_logged_in:
        return redirect_if_logged_in

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo']
        hashed_password = request.form['contraseña']

        # Hashear la contraseña antes de almacenarla
        hashed_password = generate_password_hash(hashed_password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (nombre, apellido, correo_electronico, hashed_password) VALUES (?, ?, ?, ?)", 
                           (nombre, apellido, correo_electronico, hashed_password))
            conn.commit()
        except mariadb.IntegrityError:
            return "Error: Email already registered."
        finally:
            conn.close()

        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    redirect_if_logged_in = check_logged_in()
    if redirect_if_logged_in:
        return redirect_if_logged_in

    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, hashed_password FROM usuarios WHERE correo_electronico = ?", (correo,))
        user = cursor.fetchone()
        conn.close()

        if user:
            usuario_id, usuario_nombre, hashed_password = user
            if check_password_hash(hashed_password, contraseña):
                session['user_id'] = usuario_id
                session['user_name'] = usuario_nombre
                flash("Successfuly logged in", "success")
                # Si el usuario intentó agregar un producto al carrito antes de iniciar sesión
                if session.get('post_login_add_to_cart'):
                    producto_id = session.pop('post_login_add_to_cart')
                    carrito_id = get_or_create_cart(usuario_id)

                    conn = get_db_connection()
                    cursor = conn.cursor()

                    cursor.execute("SELECT id FROM carro_de_compra_items WHERE carro_de_compra_id = ? AND product_item_id = ?", (carrito_id, producto_id))
                    item = cursor.fetchone()

                    if item:
                        cursor.execute("UPDATE carro_de_compra_items SET cantidad = cantidad + 1 WHERE id = ?", (item[0],))
                    else:
                        cursor.execute("INSERT INTO carro_de_compra_items (carro_de_compra_id, product_item_id, cantidad) VALUES (?, ?, 1)", (carrito_id, producto_id))

                    conn.commit()
                    conn.close()
                next_page = session.pop('next', url_for('index'))  # Obtener la página almacenada o redirigir a index
                return redirect(next_page)
            else:
                flash("Error: Wrong password", "danger")
        else:
            flash("Error: User not found", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # Limpia toda la sesión
    flash("Successfully logged out", "info")  # Mensaje de confirmación
    return redirect(url_for('index'))  # Redirigir a la página de inicio

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/carrito')
def carrito():
    if 'user_id' not in session:
        session['next'] = request.path  
        flash("You must log in to access the cart.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener el ID del carrito del usuario
    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (session['user_id'],))
    carrito = cursor.fetchone()

    if not carrito:
        conn.close()
        return render_template('carrito.html', usuario=session['user_name'], carrito_vacio=True, productos=[])

    carrito_id = carrito[0]

    # Obtener productos en el carrito
    cursor.execute("""
        SELECT p.id, p.nombre, p.precio, p.imagen, ci.cantidad 
        FROM carro_de_compra_items ci
        JOIN productos p ON ci.product_item_id = p.id
        WHERE ci.carro_de_compra_id = ?
    """, (carrito_id,))
    productos_carrito = cursor.fetchall()

    productos = [
        {"id": p[0], "nombre": p[1], "precio": p[2], "imagen": p[3], "cantidad": p[4]}
        for p in productos_carrito
    ]

    carrito_vacio = len(productos) == 0

    conn.close()

    return render_template('carrito.html', usuario=session['user_name'], carrito_vacio=carrito_vacio, productos=productos)

@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    if 'user_id' not in session:
        session['next'] = request.referrer or url_for('index')
        session['post_login_add_to_cart'] = request.form.get('producto_id')
        flash("You must log in to add products to your cart.", "warning")
        return jsonify(success=False, redirect_to_login=url_for('login'))

    producto_id = request.form.get('producto_id')

    if not producto_id:
        return jsonify({"error": "Producto no válido"}), 400

    user_id = session['user_id']
    carrito_id = get_or_create_cart(user_id)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM carro_de_compra_items WHERE carro_de_compra_id = ? AND product_item_id = ?", (carrito_id, producto_id))
    item = cursor.fetchone()

    if item:
        cursor.execute("UPDATE carro_de_compra_items SET cantidad = cantidad + 1 WHERE id = ?", (item[0],))
    else:
        cursor.execute("INSERT INTO carro_de_compra_items (carro_de_compra_id, product_item_id, cantidad) VALUES (?, ?, 1)", (carrito_id, producto_id))

    conn.commit()
    conn.close()

    return jsonify(success=True)

@app.route('/eliminar_del_carrito', methods=['POST'])
def eliminar_del_carrito():
    if 'user_id' not in session:
        return jsonify({"error": "Debes iniciar sesión para modificar el carrito"}), 401

    producto_id = request.form.get('producto_id')

    if not producto_id:
        return jsonify({"error": "Producto no válido"}), 400

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener el ID del carrito del usuario
    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (user_id,))
    carrito = cursor.fetchone()

    if not carrito:
        conn.close()
        return jsonify({"error": "Carrito no encontrado"}), 404

    carrito_id = carrito[0]

    # Eliminar el producto del carrito
    cursor.execute("DELETE FROM carro_de_compra_items WHERE carro_de_compra_id = ? AND product_item_id = ?", (carrito_id, producto_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/profile')
def usuario():
    if 'user_name' in session:
        return render_template('home.html', usuario=session['user_name'])
    else:
        session['next'] = request.path  # Guardar la URL actual antes de redirigir
        flash("Log in requiered in order to proceed.", "warning")
        return redirect(url_for('login'))

# Ruta para la página de inicio
@app.route('/profile/home')
def home():
    if 'user_id' not in session:
        session['next'] = request.path  
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

# Ruta para la página de órdenes
@app.route('/profile/orders')
def orders():
    if 'user_id' not in session:
        session['next'] = request.path  
        return redirect(url_for('login'))
    else:
        return render_template('orders.html')

@app.route('/profile/address', methods=['GET', 'POST'])
def address():
    if 'user_id' not in session:
        session['next'] = request.path  
        return redirect(url_for('login'))
    
    # Obtener lista de países en inglés
    countries = list(countries_for_language('en'))  

    if request.method == 'POST':
        selected_country = request.form.get('country')
        flash(f"País seleccionado: {selected_country}", "success")  # Solo muestra un mensaje, no lo guarda aún.

    return render_template('address.html', countries=countries)

# Ruta para la página de ajustes
@app.route('/profile/settings')
def settings():
    if 'user_id' not in session:
        session['next'] = request.path  
        return redirect(url_for('login'))
    else:
        return render_template('settings.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash("You need to log in before performing this action.", "warning")
        return redirect(url_for('login'))

    contraseña = request.form['contraseña']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT hashed_password FROM usuarios WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()

    if user and check_password_hash(user[0], contraseña):
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (session['user_id'],))
        conn.commit()
        conn.close()
        session.clear()
        flash("Account deleted successfully.", "success")
        return redirect(url_for('index'))
    else:
        conn.close()
        flash("Wrong password. Account not deleted", "danger")
        return redirect(url_for('usuario'))

@app.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    email = request.form.get('correo')
    if not email:
        flash("The email is required", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE correo_electronico = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        token = serializer.dumps(email, salt="reset-password")
        reset_link = url_for('reset_password', token=token, _external=True)

        msg = Message("Password Recovery",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f"To reset your password, click on the following link: {reset_link}"
        mail.send(msg)

        flash("An email has been sent with instructions on how to recover your password.", "success")
        return redirect(url_for('login'))

    flash("Email not found", "danger")
    return redirect(url_for('login'))

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="reset-password", max_age=3600)  # Expira en 1 hora
    except:
        flash("Expired or invalid token", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        nueva_contraseña = request.form['nueva_contraseña']
        hashed_password = generate_password_hash(nueva_contraseña)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET hashed_password = ? WHERE correo_electronico = ?", 
                       (hashed_password, email))
        conn.commit()
        conn.close()

        flash("Your password has been reset successfuly.", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)

#Conexion a MariaDB sin ORM
def get_db_connection():
    return mariadb.connect(
        user="railway",
        password="Amdwzi-JlqxbQAzQFP~i-zZWK5L1J0P8",
        host="switchyard.proxy.rlwy.net",
        port=35476,
        database="railway"
    )

#Se crea el carro de compra y se le asigna a un usuario.
def get_or_create_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (user_id,))
    carrito = cursor.fetchone()

    if not carrito:
        cursor.execute("INSERT INTO carro_de_compra (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (user_id,))
        carrito = cursor.fetchone()

    conn.close()
    return carrito[0]

@app.route('/snacks')
def snacks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, categoria, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()

    productos_json = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": p[3], "categoria": p[4], "imagen": p[5], "stock": p[6]}
        for p in productos
    ]

    return render_template('snacks.html', productos=productos_json)

@app.route('/drinks')
def drinks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, categoria, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()

    productos_json = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": p[3], "categoria": p[4], "imagen": p[5], "stock": p[6]}
        for p in productos
    ]

    return render_template('drinks.html', productos=productos_json)

@app.route('/candy')
def candy():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, categoria, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()

    productos_json = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": p[3], "categoria": p[4], "imagen": p[5], "stock": p[6]}
        for p in productos
    ]

    return render_template('candy.html', productos=productos_json)

@app.route('/all_products')
def all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, categoria, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()

    productos_json = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": p[3], "categoria": p[4], "imagen": p[5], "stock": p[6]}
        for p in productos
    ]

    return render_template('all_products.html', productos=productos_json)

if __name__ == "__main__":
    app.run(debug=True)