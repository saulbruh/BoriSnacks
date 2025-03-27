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
            return "Error: El correo ya está registrado."
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
                flash("Inicio de sesión exitoso", "success")
                next_page = session.pop('next', url_for('index'))  # Obtener la página almacenada o redirigir a index
                return redirect(next_page)
            else:
                flash("Error: Contraseña incorrecta", "danger")
        else:
            flash("Error: Usuario no encontrado", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # Limpia toda la sesión
    flash("Has cerrado sesión exitosamente", "info")  # Mensaje de confirmación
    return redirect(url_for('index'))  # Redirigir a la página de inicio

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/perfil')
def usuario():
    if 'user_name' in session:
        return render_template('user.html', usuario=session['user_name'])
    else:
        session['next'] = request.path  # Guardar la URL actual antes de redirigir
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('login'))

@app.route('/carrito')
def carrito():
    if 'user_name' in session:
        return render_template('carrito.html', usuario=session['user_name'])
    else:
        session['next'] = request.path  # Guardar la URL actual antes de redirigir
        flash("Debes iniciar sesión para acceder al carrito.", "warning")
        return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para realizar esta acción.", "warning")
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
        flash("Cuenta eliminada exitosamente.", "success")
        return redirect(url_for('index'))
    else:
        conn.close()
        flash("Contraseña incorrecta. No se eliminó la cuenta.", "danger")
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

if __name__ == "__main__":
    app.run(debug=True)