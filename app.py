from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import mariadb  # type: ignore
import hashlib

app = Flask(__name__)
app.secret_key = "1234"

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


@app.route('/registro', methods=['GET', 'POST'])
def registro():
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

@app.route('/profile')
def usuario():
    if 'user_name' in session:
        return render_template('home.html', usuario=session['user_name'])
    else:
        session['next'] = request.path  # Guardar la URL actual antes de redirigir
        flash("Log in requiered in order to proceed.", "warning")
        return redirect(url_for('login'))

@app.route('/carrito')
def carrito():
    if 'user_id' not in session:
        session['next'] = request.path  
        flash("Debes iniciar sesión para acceder al carrito.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si el usuario ya tiene un carrito
    cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (session['user_id'],))
    carrito = cursor.fetchone()

    if not carrito:
        # Si no tiene carrito, crearlo
        cursor.execute("INSERT INTO carro_de_compra (user_id) VALUES (?)", (session['user_id'],))
        conn.commit()
        cursor.execute("SELECT id FROM carro_de_compra WHERE user_id = ?", (session['user_id'],))
        carrito = cursor.fetchone()

    carrito_id = carrito[0]

    # Contar cuántos productos hay en el carrito
    cursor.execute("SELECT COUNT(*) FROM carro_de_compra_items WHERE carro_de_compra_id = ?", (carrito_id,))
    cantidad_productos = cursor.fetchone()[0]
    carrito_vacio = cantidad_productos == 0  

    conn.close()

    return render_template('carrito.html', usuario=session['user_name'], carrito_vacio=carrito_vacio)

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

if __name__ == "__main__":
    app.run(debug=True)