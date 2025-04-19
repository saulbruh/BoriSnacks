from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
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

    relacionados = [
        p for p in productos_json if p['categoria'] == producto['categoria'] and p['id'] != id
    ][:6]

    return render_template('product.html', producto=producto, relacionados=relacionados)

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
        fecha_registro = date.today()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (nombre, apellido, correo_electronico, hashed_password, fecha_registro) VALUES (?, ?, ?, ?, ?)", 
                           (nombre, apellido, correo_electronico, hashed_password, fecha_registro))
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

        cursor.execute("SELECT id, nombre, apellido, correo_electronico, hashed_password FROM usuarios WHERE correo_electronico = ?", (correo,))
        user = cursor.fetchone()
        conn.close()

        if user:
            usuario_id, usuario_nombre, usuario_apellido, usuario_email, hashed_password = user
            if check_password_hash(hashed_password, contraseña):
                session['user_id'] = usuario_id
                session['user_name'] = usuario_nombre
                session['user_email'] = usuario_email
                session['user_lastname'] = usuario_apellido
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

@app.route('/register_address', methods=['GET', 'POST'])
def register_address():
    if 'user_id' not in session:
        flash("You must be logged in to add an address.", "warning")
        session['next'] = request.path
        return redirect(url_for('login'))

    countries = list(countries_for_language('en'))

    if request.method == 'POST':
        calle1 = request.form['calle1']
        calle2 = request.form.get('calle2', '')
        ciudad = request.form['ciudad']
        pais = request.form['pais']
        codigo_postal = request.form['codigo_postal']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO direcciones (user_id, calle1, calle2, ciudad, pais, codigo_postal) VALUES (?, ?, ?, ?, ?, ?)",
                       (session['user_id'], calle1, calle2, ciudad, pais, codigo_postal))
        conn.commit()
        conn.close()

        flash("Dirección guardada exitosamente.", "success")
        return redirect(url_for('home'))

    return render_template('register_address.html', countries=countries)

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

@app.route('/modificar_cantidad', methods=['POST'])
def modificar_cantidad():
    if 'user_id' not in session:
        return jsonify(success=False, error="No autorizado")

    producto_id = request.form.get('producto_id')
    accion = request.form.get('accion')  # puede ser "sumar" o "restar"

    if not producto_id or accion not in ['sumar', 'restar']:
        return jsonify(success=False, error="Parámetros inválidos")

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (user_id,))
    carrito = cursor.fetchone()

    if not carrito:
        conn.close()
        return jsonify(success=False, error="Carrito no encontrado")

    carrito_id = carrito[0]
    cursor.execute("SELECT id, cantidad FROM carro_de_compra_items WHERE carro_de_compra_id = ? AND product_item_id = ?", (carrito_id, producto_id))
    item = cursor.fetchone()

    if not item:
        conn.close()
        return jsonify(success=False, error="Producto no encontrado en el carrito")

    item_id, cantidad = item

    if accion == 'sumar':
        cursor.execute("UPDATE carro_de_compra_items SET cantidad = cantidad + 1 WHERE id = ?", (item_id,))
    elif accion == 'restar' and cantidad > 1:
        cursor.execute("UPDATE carro_de_compra_items SET cantidad = cantidad - 1 WHERE id = ?", (item_id,))
    elif accion == 'restar' and cantidad <= 1:
        cursor.execute("DELETE FROM carro_de_compra_items WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()

    return jsonify(success=True)

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

@app.route('/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    if 'user_id' not in session:
        return jsonify(success=False, error="No autorizado")

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (user_id,))
    carrito = cursor.fetchone()

    if not carrito:
        conn.close()
        return jsonify(success=False, error="Carrito no encontrado")

    carrito_id = carrito[0]
    cursor.execute("DELETE FROM carro_de_compra_items WHERE carro_de_compra_id = ?", (carrito_id,))
    conn.commit()
    conn.close()

    return jsonify(success=True)

@app.route('/crear_orden', methods=['GET'])
def crear_orden():
    if 'user_id' not in session:
        session['next'] = request.path
        flash("You must be logged in to complete your order.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener ID del carrito
    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (session['user_id'],))
    carrito = cursor.fetchone()
    if not carrito:
        conn.close()
        flash("Your cart is empty.", "warning")
        return redirect(url_for('carrito'))

    carrito_id = carrito[0]

    # Obtener productos del carrito
    cursor.execute("""
          SELECT p.id, p.nombre, p.precio, p.imagen, ci.cantidad 
          FROM carro_de_compra_items ci
          JOIN productos p ON ci.product_item_id = p.id
          WHERE ci.carro_de_compra_id = ?
      """, (carrito_id,))
    productos_carrito = cursor.fetchall()

    productos = [
          {"id": p[0], "nombre": p[1], "precio": p[2], "imagen": p[3], "cantidad": p[4], "subtotal": p[2] * p[4]}
          for p in productos_carrito
      ]
    total = sum(p["subtotal"] for p in productos)

    # Obtener direcciones del usuario
    cursor.execute("SELECT id, calle1, calle2, ciudad, pais, codigo_postal FROM direcciones WHERE user_id = ?", (session['user_id'],))
    direcciones_db = cursor.fetchall()
    direcciones = [
          {
              "id": d[0],
              "calle1": d[1],
              "calle2": d[2],
              "ciudad": d[3],
              "pais": d[4],
              "codigo_postal": d[5]
          } for d in direcciones_db
      ]
    conn.close()
    countries = list(countries_for_language('en'))
    from datetime import datetime
    return render_template('crear_orden.html', productos=productos, total=total, direcciones=direcciones, countries=countries, now=datetime.now)

@app.route('/procesar_orden', methods=['POST'])
def procesar_orden():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para completar tu orden.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Validar dirección
    direccion_id = request.form.get('direccion_id')
    if not direccion_id:
        # Intentar crear una nueva dirección
        calle1 = request.form.get('calle1')
        ciudad = request.form.get('ciudad')
        pais = request.form.get('pais')
        codigo_postal = request.form.get('codigo_postal')

        if not all([calle1, ciudad, pais, codigo_postal]):
            flash("Todos los campos de dirección son obligatorios.", "danger")
            return redirect(url_for('crear_orden'))

        cursor.execute("""
            INSERT INTO direcciones_ordenes (calle1, calle2, ciudad, pais, codigo_postal)
            VALUES (?, ?, ?, ?, ?)
        """, (
            calle1,
            request.form.get('calle2'),
            ciudad,
            pais,
            codigo_postal
        ))
        conn.commit()
        direccion_id = cursor.lastrowid
    else:
        # Copiar dirección existente del usuario a direcciones_ordenes
        cursor.execute("SELECT calle1, calle2, ciudad, pais, codigo_postal FROM direcciones WHERE id = ? AND user_id = ?", (direccion_id, user_id))
        direccion = cursor.fetchone()
        if not direccion:
            flash("Dirección no encontrada o no válida.", "danger")
            return redirect(url_for('crear_orden'))

        cursor.execute("""
            INSERT INTO direcciones_ordenes (calle1, calle2, ciudad, pais, codigo_postal)
            VALUES (?, ?, ?, ?, ?)
        """, direccion)
        conn.commit()
        direccion_id = cursor.lastrowid

    # Validar campos de pago solo si se selecciona Card
    metodo_pago = request.form.get('metodo_pago')
    if not metodo_pago:
        flash("Please select a payment method.", "danger")
        return redirect(url_for('crear_orden'))

    if metodo_pago == 'Card':
        campos_pago = ['nombre_tarjeta', 'numero_tarjeta', 'expiracion', 'cvc']
        for campo in campos_pago:
            if not request.form.get(campo):
                flash("All card fields are required.", "danger")
                return redirect(url_for('crear_orden'))
            if campo == 'numero_tarjeta' and not request.form.get(campo).isdigit():
                flash("Card number must be numeric.", "danger")
                return redirect(url_for('crear_orden'))
            if campo == 'numero_tarjeta' and len(request.form.get(campo)) != 16:
                flash("Card number must be 16 digits.", "danger")
                return redirect(url_for('crear_orden'))
            if campo == 'cvc' and (not request.form.get(campo).isdigit() or len(request.form.get(campo)) != 3):
                flash("CVC must be 3 numeric digits.", "danger")
                return redirect(url_for('crear_orden'))

    # Obtener carrito
    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (user_id,))
    carrito = cursor.fetchone()
    if not carrito:
        flash("Tu carrito está vacío.", "danger")
        return redirect(url_for('carrito'))

    carrito_id = carrito[0]
    cursor.execute("""
        SELECT product_item_id, cantidad 
        FROM carro_de_compra_items 
        WHERE carro_de_compra_id = ?
    """, (carrito_id,))
    items = cursor.fetchall()

    if not items:
        flash("Tu carrito está vacío.", "danger")
        return redirect(url_for('carrito'))

    # Crear orden
    # metodo_pago ya se extrajo arriba
    
    # Calcular el total sumando los subtotales de los productos
    total = 0
    for item in items:
        producto_id, cantidad = item
        cursor.execute("SELECT precio FROM productos WHERE id = ?", (producto_id,))
        precio = cursor.fetchone()[0]
        total += precio * cantidad

    cursor.execute("""
        INSERT INTO ordenes (user_id, direccion_id, metodo_pago, total, fecha_orden)
        VALUES (?, ?, ?, ?, NOW())
    """, (user_id, direccion_id, metodo_pago, total))
    orden_id = cursor.lastrowid

    for item in items:
        producto_id, cantidad = item
        cursor.execute("SELECT precio FROM productos WHERE id = ?", (producto_id,))
        precio = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO orden_items (orden_id, product_id, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (orden_id, producto_id, cantidad, precio))

        # Restar del stock
        cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))

    # Vaciar carrito
    cursor.execute("DELETE FROM carro_de_compra_items WHERE carro_de_compra_id = ?", (carrito_id,))
    conn.commit()
    conn.close()

    flash("Orden procesada exitosamente.", "success")
    return redirect(url_for('orders'))

@app.route('/profile')
def usuario():
    if 'user_name' in session:
        return render_template('home.html', usuario=session['user_name'])
    else:
        session['next'] = request.path  # Guardar la URL actual antes de redirigir
        flash("Log in requiered in order to proceed.", "warning")
        return redirect(url_for('login'))

# Ruta para la página de inicio
@app.route('/profile/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        session['next'] = request.path  
        return redirect(url_for('login'))
 
    conn = get_db_connection()
    cursor = conn.cursor()
 
    if request.method == 'POST':
        if 'direccion_id' in request.form:
            # Eliminar dirección
            direccion_id = request.form['direccion_id']
            cursor.execute("DELETE FROM direcciones WHERE id = ? AND user_id = ?", (direccion_id, session['user_id']))
            conn.commit()
            flash("Dirección eliminada con éxito.", "success")
        else:
            # Agregar nueva dirección
            calle1 = request.form['calle1']
            calle2 = request.form['calle2']
            ciudad = request.form['ciudad']
            pais = request.form['pais']
            codigo_postal = request.form['codigo_postal']
            cursor.execute("INSERT INTO direcciones (user_id, calle1, calle2, ciudad, pais, codigo_postal) VALUES (?, ?, ?, ?, ?, ?)", 
                           (session['user_id'], calle1, calle2, ciudad, pais, codigo_postal))
            conn.commit()
            flash("Dirección guardada con éxito.", "success")
        conn.close()
        return redirect(url_for('home'))

 
    cursor.execute("SELECT id, user_id, calle1, calle2, ciudad, pais, codigo_postal FROM direcciones WHERE user_id = ?", (session['user_id'],))
    direcciones_db = cursor.fetchall()
    direcciones = [
        {
            "id": d[0],
            "user_id": d[1],
            "calle1": d[2],
            "calle2": d[3],
            "ciudad": d[4],
            "pais": d[5],
            "codigo_postal": d[6]
        } for d in direcciones_db
    ]
    cursor.execute("""
        SELECT o.id, o.fecha_orden, o.total,
               d.calle1, d.ciudad, d.pais
        FROM ordenes o
        JOIN direcciones_ordenes d ON o.direccion_id = d.id
        WHERE o.user_id = ?
        ORDER BY o.fecha_orden DESC
        LIMIT 2
    """, (session['user_id'],))
    ordenes_db = cursor.fetchall()
    ordenes_recientes = [
        {
            "id": o[0],
            "fecha": o[1],
            "total": o[2],
            "direccion": f"{o[3]}, {o[4]}, {o[5]}"
        } for o in ordenes_db
    ]
    cursor.execute("SELECT COUNT(*) FROM ordenes WHERE user_id = ?", (session['user_id'],))
    total_ordenes = cursor.fetchone()[0]
    cursor.execute("SELECT fecha_registro FROM usuarios WHERE id = ?", (session['user_id'],))
    fecha_registro = cursor.fetchone()[0]
    conn.close()
    countries = list(countries_for_language('en'))
    return render_template('home.html', direcciones=direcciones, countries=countries, ordenes_recientes=ordenes_recientes, total_ordenes=total_ordenes, session=session, fecha_registro=fecha_registro)

# Ruta para la página de órdenes
@app.route('/profile/orders')
def orders():
    if 'user_id' not in session:
        session['next'] = request.path  
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
          SELECT o.id, o.fecha_orden, o.metodo_pago, o.total, 
                 d.calle1, d.ciudad, d.pais
          FROM ordenes o
          JOIN direcciones_ordenes d ON o.direccion_id = d.id
          WHERE o.user_id = ?
          ORDER BY o.fecha_orden DESC
      """, (user_id,))
    ordenes_db = cursor.fetchall()
    
    ordenes = []
    for orden in ordenes_db:
        ordenes.append({
            "id": orden[0],
            "fecha": orden[1],
            "metodo_pago": orden[2],
            "total": orden[3],
            "direccion": f"{orden[4]}, {orden[5]}, {orden[6]}"
        })
    
    conn.close()
    return render_template('orders.html', ordenes=ordenes)


@app.route('/orden/<int:orden_id>')
def orden_detalle(orden_id):
    if 'user_id' not in session:
        flash("You must be logged in to view an order.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener datos de la orden (asegurándonos que pertenezca al usuario)
    cursor.execute("""
        SELECT o.id, o.fecha_orden, o.total, o.metodo_pago,
               d.calle1, d.calle2, d.ciudad, d.pais, d.codigo_postal
        FROM ordenes o
        JOIN direcciones_ordenes d ON o.direccion_id = d.id
        WHERE o.id = ? AND o.user_id = ?
    """, (orden_id, session['user_id']))
    orden = cursor.fetchone()

    if not orden:
        flash("Order not found.", "danger")
        conn.close()
        return redirect(url_for('orders'))

    # Obtener items de la orden
    cursor.execute("""
        SELECT p.id, p.nombre, p.imagen, oi.cantidad, oi.precio_unitario
        FROM orden_items oi
        JOIN productos p ON oi.product_id = p.id
        WHERE oi.orden_id = ?
    """, (orden_id,))
    items = cursor.fetchall()
    conn.close()

    orden_info = {
        "id": orden[0],
        "fecha": orden[1],
        "total": orden[2],
        "metodo_pago": orden[3],
        "direccion": f"{orden[4]} {orden[5]}, {orden[6]}, {orden[7]}, {orden[8]}"
    }

    productos = [
        {
            "id": item[0],
            "nombre": item[1],
            "imagen": item[2],
            "cantidad": item[3],
            "precio_unitario": item[4],
            "subtotal": item[3] * item[4]
        } for item in items
    ]

    return render_template('order_page.html', orden=orden_info, productos=productos)


@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' not in session:
        flash("You need to log in before performing this action.", "warning")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('delete_account.html')

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
        return redirect(url_for('delete_account'))

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

# Conexion a MariaDB usando variables de entorno
def get_db_connection():
    return mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
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